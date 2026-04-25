from rest_framework import serializers
from .models import QueryHistory, CropPrediction, Conversation

class QueryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryHistory
        fields = '__all__'

class CropPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropPrediction
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'