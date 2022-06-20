"""View module for handling recipe requests """

from argparse import Action
from django.http import HttpResponseServerError
from app_api.models import Ingredients
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status



class IngredientsView(ViewSet):
    """ingredient views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single ingredient

        Returns:
            Response -- JSON serialized ingredient
        """
        try:
            ingredients = Ingredients.objects.get(pk=pk)
            serializer = IngredientsSerializer(ingredients)
            return Response(serializer.data)
        except Ingredients.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    
    def list(self, request):
        """Handle GET requests to get all ingredients

        Returns:
            Response -- JSON serialized list of ingredients
        """
        ingredients = Ingredients.objects.all()
    
        serializer = IngredientsSerializer(ingredients, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized recipe instance
        """
        user = request.auth.user
        serializer = CreateIngredientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for an ingredient

        Returns:
            Response -- Empty body with 204 status code
        """
        ingredients = Ingredients.objects.get(pk=pk)
        serializer = CreateIngredientsSerializer(ingredients, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        ingredient = Ingredients.objects.get(pk=pk)
        ingredient.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class IngredientsSerializer(serializers.ModelSerializer):
    """JSON serializer for ingredients
    """
    class Meta:
        model = Ingredients
        fields = ('id', 'type', 'name', 'alpha_acids')
        depth = 3
        
class CreateIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['type', 'name', 'alpha_acids']
        
