import json
import os
import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

try:
    import openai
except ImportError:
    openai = None

try:
    import requests
except ImportError:
    requests = None

try:
    import joblib
    import numpy as np
    import os
    # Load ML model
    model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'crop_model.pkl')
    if os.path.exists(model_path):
        ml_model = joblib.load(model_path)
        model_features = ['rainfall', 'temperature', 'humidity', 'soil_ph']
    else:
        ml_model = None
except ImportError:
    ml_model = None

from .models import QueryHistory, CropPrediction, Conversation
from .serializers import QueryHistorySerializer, CropPredictionSerializer, ConversationSerializer


def home(request):
    return JsonResponse({"message": "AgriVoice API running 🚀"})


def _openai_response(question, language='en'):
    if openai is None:
        return None

    api_key = os.environ.get("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)
    if not api_key or api_key == "your-api-key-here":
        return None

    try:
        client = openai.OpenAI(api_key=api_key)
        lang_instruction = "in Kannada" if language == 'kn' else "in English"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an intelligent farming assistant providing concise, practical advice {lang_instruction}."},
                {"role": "user", "content": question},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def _sarvam_response(question, language='en'):
    if requests is None:
        return None

    api_key = os.environ.get("SARVAM_API_KEY") or getattr(settings, "SARVAM_API_KEY", None)
    if not api_key or api_key == "your-api-key-here":
        return None

    try:
        lang_instruction = "in Kannada" if language == 'kn' else "in English"
        url = "https://api.sarvam.ai/text-to-text"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "sarvam-2b-v0.5",
            "messages": [
                {"role": "system", "content": f"You are an intelligent farming assistant providing concise, practical advice {lang_instruction}."},
                {"role": "user", "content": question}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception:
        return None


def _format_prediction(query):
    """Enhanced prediction using ML model with fallback to rule-based system"""
    if ml_model is None:
        # Fallback to rule-based prediction
        return _rule_based_prediction(query)

    # Extract features from query
    features = _extract_features_from_query(query)

    if features is None:
        # If we can't extract features, use rule-based
        return _rule_based_prediction(query)

    try:
        # Make prediction using ML model
        prediction = ml_model.predict([features])[0]
        return f"🌾 {prediction} (ML prediction based on conditions)"
    except Exception as e:
        print(f"ML prediction error: {e}")
        return _rule_based_prediction(query)


def _extract_features_from_query(query):
    """Extract numerical features from natural language query"""
    text = query.lower()

    # Default values
    rainfall = 100  # mm
    temperature = 25  # Celsius
    humidity = 70  # %
    soil_ph = 6.5

    # Extract rainfall information
    if "rain" in text or "wet" in text:
        rainfall = 150
    elif "dry" in text or "drought" in text:
        rainfall = 50
    elif "moderate" in text:
        rainfall = 100

    # Extract temperature information
    if "hot" in text or "warm" in text:
        temperature = 30
    elif "cold" in text or "cool" in text:
        temperature = 18
    elif "temperate" in text:
        temperature = 22

    # Extract humidity information
    if "humid" in text or "moist" in text:
        humidity = 80
    elif "dry" in text:
        humidity = 40

    # Extract soil pH information
    if "acidic" in text:
        soil_ph = 5.5
    elif "alkaline" in text:
        soil_ph = 7.5

    return [rainfall, temperature, humidity, soil_ph]


def _rule_based_prediction(query):
    """Fallback rule-based prediction system"""
    condition = query.lower()

    if "rain" in condition or "wet" in condition:
        return "🌾 Rice (good for rainy season)"
    if "hot" in condition or "dry" in condition:
        return "🌻 Sorghum (heat and drought tolerant)"
    if "cold" in condition or "frost" in condition:
        return "🥔 Potato (cool climate crop)"
    if "nutrient" in condition or "soil" in condition:
        return "🌿 Legumes (help restore soil nitrogen)"
    if "low" in condition and "water" in condition:
        return "🌿 Pearl millet (very water efficient crop)"

    return "🌽 Maize (general-purpose crop recommendation)"


def _smart_answer(question, model="openai", language='en'):
    if model == "sarvam":
        answer = _sarvam_response(question, language)
        if answer:
            return answer
    else:
        # Default to OpenAI
        answer = _openai_response(question, language)
        if answer:
            return answer

    # Fallback to rule-based responses
    text = question.lower()
    if "water" in text or "irrigat" in text:
        return "💧 Keep soil evenly moist and avoid overwatering during the heat of the day." if language == 'en' else "💧 ಬೆಳೆಗಳನ್ನು ಹೆಚ್ಚಾಗಿ ನೀರಾಳೆಗೊಳಿಸಬೇಡಿ, ಮಣ್ಣು ಸಮತೋಲನವಾಗಿ ತೇವದಾಯಕವಾಗಿರಲಿ."
    if "fertil" in text or "nutrient" in text:
        return "🌱 Apply a balanced NPK fertilizer and test soil pH for best results." if language == 'en' else "🌱 ಸಮತೋಲನವಾಗಿರುವ NPK ರಸಗೊಬ್ಬರವನ್ನು ಬಳಸಿ ಮತ್ತು ಉತ್ತಮ ಫಲಿತಾಂಶಕ್ಕಾಗಿ ಮಣ್ಣು pH ಪರೀಕ್ಷಿಸಿ."
    if "pest" in text or "disease" in text:
        return "🛡 Use natural predators or organic sprays and remove affected plants quickly." if language == 'en' else "🛡 ಸಹಜ ಶತ್ರುಗಳನ್ನು ಬಳಸಿ ಅಥವಾ ಆರ್ಗ್ಯಾನಿಕ್ ಸ್ಫ್ರೇಗಳನ್ನು ಬಳಸಿ ಮತ್ತು ಸೋಂಕಿತರ ಪ್ಲಾಂಟ್ಗಳನ್ನು ಬೇಗತೆಗೆ ತೆಗೆದುಹಾಕಿ."
    if "weather" in text or "forecast" in text:
        return "🌦 Check local weather daily and prepare drainage for heavy rain." if language == 'en' else "🌦 ದೈನಂದಿನ ಹವಾಮಾನವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಭಾರೀ ಮಳೆಯ ಸಮಯದಲ್ಲಿ ನೀರಿನ ನಿರ್ಗಮನ ವ್ಯವಸ್ಥೆಯನ್ನು ಸಿದ್ಧಗೊಳಿಸಿ."

    fallback_answers = [
        "🌾 Rotate crops each season to keep soil healthy." if language == 'en' else "🌾 ಭೂಮಿಯನ್ನು ಆರೋಗ್ಯಕರವಾಗಿಡಲು ಪ್ರತಿಮಾವು ಬೆಳೆಗಳನ್ನು ಬದಲಾಯಿಸಿ.",
        "🧑‍🌾 Monitor your field daily and act quickly when you see stress signs." if language == 'en' else "🧑‍🌾 ನಿಮ್ಮ ಭೂಮಿಯನ್ನು ದಿನನಿತ್ಯ ಮನ್ನಿಸಿ ಮತ್ತು ಮರುಳು ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದರೆ ತಕ್ಷಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ.",
        "☀️ Use shade nets on hot days and mulch to conserve soil moisture." if language == 'en' else "☀️ ಬಿಸಿಯ ದಿನಗಳಲ್ಲಿ ಛಾಯೆ ಜಾಲಗಳನ್ನು ಬಳಸಿ ಮತ್ತು ಮಣ್ಣಿನ ತೇವವನ್ನು ಉಳಿಸಲು ಮಲ್ಚ್ ಬಳಸಿ.",
        "🌱 Add compost and organic matter to improve soil structure." if language == 'en' else "🌱 ಮಣ್ಣಿನ ರಚನೆಯನ್ನು ಸುಧಾರಿಸಲು ಕಂಪೋಸ್ಟ್ ಮತ್ತು ಸಸ್ಯ ಪದಾರ್ಥಗಳನ್ನು ಸೇರಿಸಿ.",
    ]
    return random.choice(fallback_answers)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "username": request.user.username,
        "email": request.user.email,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password', '')
    new_password = request.data.get('new_password', '')
    confirm_password = request.data.get('confirm_password', '')

    if not current_password or not new_password or not confirm_password:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({"error": "New password and confirm password do not match."}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 6:
        return Response({"error": "Password must be at least 6 characters."}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    try:
        send_mail(
            subject='Your AgriVoice password has changed',
            message='Your password was successfully updated. If you did not make this change, please contact support immediately.',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@agrivoice.local'),
            recipient_list=[user.email] if user.email else [],
            fail_silently=True,
        )
    except Exception:
        pass

    return Response({"message": "Password updated successfully."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict(request):
    query = request.data.get("query", "")

    if not query:
        return Response({"error": "Missing query field"}, status=status.HTTP_400_BAD_REQUEST)

    result = _format_prediction(query)

    # Save prediction
    CropPrediction.objects.create(user=request.user, query=query, result=result)

    return Response({"result": result})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ask(request):
    question = request.data.get("question", "")
    model = request.data.get("model", "openai")
    language = request.data.get("language", "en")

    if not question:
        return Response({"error": "Missing question field"}, status=status.HTTP_400_BAD_REQUEST)

    answer = _smart_answer(question, model, language)

    # Save query history
    QueryHistory.objects.create(user=request.user, question=question, answer=answer)

    # Save conversation for memory
    Conversation.objects.create(user=request.user, message=question, response=answer)

    return Response({"answer": answer})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crops(request):
    crop_list = [
        {"name": "Rice", "best_for": "Rainy season", "notes": "Needs rich soil and standing water."},
        {"name": "Sorghum", "best_for": "Hot, dry weather", "notes": "Drought tolerant and low maintenance."},
        {"name": "Potato", "best_for": "Cool weather", "notes": "Requires loose soil and consistent moisture."},
        {"name": "Maize", "best_for": "General conditions", "notes": "Good for mixed crop rotations."},
        {"name": "Legumes", "best_for": "Soil recovery", "notes": "Restore nitrogen and improve soil health."},
    ]
    return Response({"crops": crop_list})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def soil(request):
    soil_type = request.data.get("soil_type", "").lower()
    moisture = request.data.get("moisture", "")

    if not soil_type:
        return Response({"error": "Missing soil_type field"}, status=status.HTTP_400_BAD_REQUEST)

    if "clay" in soil_type:
        advice = "Clay soil drains slowly; add compost and avoid overwatering."
    elif "sand" in soil_type:
        advice = "Sandy soil dries quickly; use mulch and frequent light watering."
    elif "loam" in soil_type:
        advice = "Loam is ideal; keep it fertile with compost and maintain moisture."
    else:
        advice = "Use organic compost and monitor moisture often."

    if moisture:
        advice += f" Current moisture: {moisture}."

    return Response({"soil_advice": advice})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def forecast(request):
    days = int(request.data.get("days", 3))

    if days < 1:
        days = 3

    forecast_data = []
    for i in range(days):
        forecast_data.append({
            "day": f"Day {i + 1}",
            "temperature": random.randint(20, 32),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy"]),
        })

    return Response({"forecast": forecast_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    queries = QueryHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
    serializer = QueryHistorySerializer(queries, many=True)
    return Response({"history": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predictions(request):
    preds = CropPrediction.objects.filter(user=request.user).order_by('-timestamp')[:10]
    serializer = CropPredictionSerializer(preds, many=True)
    return Response({"predictions": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation(request):
    convs = Conversation.objects.filter(user=request.user).order_by('-timestamp')[:20]
    serializer = ConversationSerializer(convs, many=True)
    return Response({"conversation": serializer.data})
