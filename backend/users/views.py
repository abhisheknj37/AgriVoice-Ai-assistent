from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json


@csrf_exempt
def register(request):
    print(f"Register request: {request.method} from {request.META.get('REMOTE_ADDR')}")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"Register data: {data}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")
        print(f"Username: {username}, Password length: {len(password) if password else 0}")

        if not username or not password:
            print("Missing fields")
            return JsonResponse({"error": "Missing fields"}, status=400)

        if len(username) < 3:
            print("Username too short")
            return JsonResponse({"error": "Username must be at least 3 characters"}, status=400)

        if len(password) < 8:
            print("Password too short")
            return JsonResponse({"error": "Password must be at least 8 characters"}, status=400)

        if User.objects.filter(username=username).exists():
            print("User already exists")
            return JsonResponse({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        print(f"User created: {username}, token: {token.key[:10]}...")

        return JsonResponse({"message": "Registration successful", "token": token.key})

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Missing fields"}, status=400)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({"token": token.key})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
