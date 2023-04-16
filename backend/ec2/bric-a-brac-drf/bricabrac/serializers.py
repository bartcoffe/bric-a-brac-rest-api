from rest_framework import serializers
from .models import Category, Status, Flashcard


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['id', 'name']


class FlashcardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flashcard
        fields = [
            'id',
            'user',
            'category',
            'code',
            'description',
            'hashtag',
            'status',
        ]
