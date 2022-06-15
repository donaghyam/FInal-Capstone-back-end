"""View module for handling recipe requests """

from argparse import Action
from django.http import HttpResponseServerError
from app_api.models import RecipeIngredients, Recipes, Steps
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status



class StepsView(ViewSet):
    """recipe views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single recipe ingredient

        Returns:
            Response -- JSON serialized recipe ingredient
        """
        try:
            steps = Steps.objects.get(pk=pk)
            serializer = StepsSerializer(steps)
            return Response(serializer.data)
        except Steps.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    
    def list(self, request):
        """Handle GET requests to get all recipe ingredients

        Returns:
            Response -- JSON serialized list of recipe ingredients
        """
        steps = Steps.objects.all()
        
        #query by recipe
        recipe = request.query_params.get('recipe', None)
        
        if recipe is not None:
            steps = steps.filter(recipe__id=recipe)
    
        serializer = StepsSerializer(steps, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized recipe instance
        """
        user = request.auth.user
        serializer = CreateStepsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a recipe

        Returns:
            Response -- Empty body with 204 status code
        """
        steps = Steps.objects.get(pk=pk)
        serializer = CreateStepsSerializer(steps, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        recipe = Steps.objects.get(pk=pk)
        recipe.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class StepsSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes
    """
    class Meta:
        model = Steps
        fields = ('id', 'description', 'recipe', 'temperature', 'amount', 'time')
        depth = 3
        
class CreateStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = ['description', 'recipe', 'temperature', 'amount', 'time']
        
