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


class FlashcardGetSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(many=False,
                                          read_only=True,
                                          slug_field='name')
    user = serializers.SlugRelatedField(many=False,
                                        read_only=True,
                                        slug_field='username')
    category = serializers.SlugRelatedField(many=False,
                                            read_only=True,
                                            slug_field='name')

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


class FlashcardPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flashcard
        fields = [
            'id', 'user', 'category', 'code', 'description', 'hashtag',
            'status'
        ]
