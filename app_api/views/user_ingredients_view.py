"""View module for handling recipe requests """

from argparse import Action
from django.http import HttpResponseServerError
from app_api.models import UserIngredients, user_ingredients
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status



class UserIngredientsView(ViewSet):
    """user ingredient views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single user ingredient

        Returns:
            Response -- JSON serialized user ingredient
        """
        try:
            user_ingredients = UserIngredients.objects.get(pk=pk)
            serializer = UserIngredientsSerializer(user_ingredients)
            return Response(serializer.data)
        except UserIngredients.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all user ingredients

        Returns:
            Response -- JSON serialized list of user ingredients
        """
        user_ingredients = UserIngredients.objects.all()
    
        serializer = UserIngredientsSerializer(user_ingredients, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized user ingredients instance
        """
        user = request.auth.user
        serializer = CreateUserIngredientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a user ingredients

        Returns:
            Response -- Empty body with 204 status code
        """
        user_ingredients = UserIngredients.objects.get(pk=pk)
        serializer = CreateUserIngredientsSerializer(user_ingredients, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        user_ingredients = UserIngredients.objects.get(pk=pk)
        user_ingredients.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class UserIngredientsSerializer(serializers.ModelSerializer):
    """JSON serializer for user ingredients
    
    """
    class Meta:
        model = UserIngredients
        fields = ('id', 'ingredient', 'quantity', 'user')
        depth = 3
        
class CreateUserIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIngredients
        fields = ['ingredient', 'quantity', 'user']
        
