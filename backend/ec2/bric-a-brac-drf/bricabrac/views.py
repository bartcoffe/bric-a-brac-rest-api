from .models import Category, Status, Flashcard
from django.contrib.auth.models import User
from .serializers import CategorySerializer, StatusSerializer, FlashcardGetSerializer, FlashcardPostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def statuses(request):
    if request.method == 'GET':
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def flashcards(request):
    if request.method == 'GET':
        flashcards = Flashcard.objects.all()
        serializer = FlashcardGetSerializer(flashcards, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        category_dict = {
        'python':1,
        'sql':2,
        'javascript':3,
        'java':4,
        'c++':5,
        'go':6,
        }

        status_dict = {
            'new':1,
            'easy':2,
            'moderate':3,
            'ratherHard':4,
            'hard':5,
        }
        data = request.data
        data['user'] = User.objects.get(username=data['user']).id
        data['category'] = Category.objects.get(name=data['category']).id
        data['status'] = Status.objects.get(name=data['status']).id
        serializer = FlashcardPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'DELETE'])
def flashcard(request, id):
    try:
        flashcard = Flashcard.objects.get(pk=id)
    except Flashcard.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FlashcardGetSerializer(flashcard)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)