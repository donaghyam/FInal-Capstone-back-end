"""View module for handling recipe requests """

from argparse import Action
from django.http import HttpResponseServerError
from app_api.models import RecipeIngredients, Recipes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status



class RecipeIngredientsView(ViewSet):
    """recipe views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single recipe ingredient

        Returns:
            Response -- JSON serialized recipe ingredient
        """
        try:
            recipe_ingredients = RecipeIngredients.objects.get(pk=pk)
            serializer = RecipeIngredientsSerializer(recipe_ingredients)
            return Response(serializer.data)
        except RecipeIngredients.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    
    def list(self, request):
        """Handle GET requests to get all recipe ingredients

        Returns:
            Response -- JSON serialized list of recipe ingredients
        """
        recipe_ingredients = RecipeIngredients.objects.all()
        
        #query by recipe
        recipe = request.query_params.get('recipe', None)
        
        if recipe is not None:
            recipe_ingredients = recipe_ingredients.filter(recipe__id=recipe)
    
        serializer = RecipeIngredientsSerializer(recipe_ingredients, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized recipe instance
        """
        serializer = CreateRecipeIngredientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a recipe

        Returns:
            Response -- Empty body with 204 status code
        """
        recipe_ingredients = RecipeIngredients.objects.get(pk=pk)
        serializer = CreateRecipeIngredientsSerializer(recipe_ingredients, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        recipe = RecipeIngredients.objects.get(pk=pk)
        recipe.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes
    """
    class Meta:
        model = RecipeIngredients
        fields = ('id', 'ingredient', 'quantity', 'recipe', 'use', 'time')
        depth = 3
        
class CreateRecipeIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'quantity', 'recipe', 'use', 'time']
        
