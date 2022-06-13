"""View module for handling recipe requests """

from argparse import Action
from django.http import HttpResponseServerError
from app_api.models import Recipes, RecipeIngredients, UserIngredients
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db import connection
from app_api.views.helpers import dict_fetch_all
from django import template



class RecipeView(ViewSet):
    """recipe views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single recipe

        Returns:
            Response -- JSON serialized recipe
        """
        try:
            recipe = Recipes.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipes.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all recipes

        Returns:
            Response -- JSON serialized list of recipes
        """
        # The recipe variable is now a list of Recipes objects
        recipes = Recipes.objects.all()
    
        serializer = RecipeSerializer(recipes, many=True)

        return Response(serializer.data)
    
    #Write custom method to display a list of recipes where the current user's ingredients 
    #quantity exceed the amount required in the recipe
    def find_duplicate_ingredients(self):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT 
                    id,
                    use,
                    time,
                    ingredient_id,
                    recipe_id,
                    SUM(quantity) as quantity,
                    COUNT(*) as count
                FROM app_api_recipeingredients
                GROUP BY ingredient_id
                HAVING COUNT(*) > 0
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            compiled_ingredients = []

            for row in dataset:
                ingredient_list = {
                    "id": row['id'],
                    "use": row['use'],
                    "time": row['time'],
                    "ingredient_id": row['ingredient_id'],
                    "recipe_id": row['recipe_id'],
                    "quantity": row['quantity'],
                    "count": row['count'],
                }
                
                compiled_ingredients.append(ingredient_list)
                
            return compiled_ingredients
            
    @action(methods=['get'], detail=False)
    def compare_ingredients(self, request):        
            
            #get all recipes            
            recipes = Recipes.objects.all()
            
            #get all user_ingredients            
            user_ingredients = UserIngredients.objects.all()
            
            #get list of compiled ingredients
            compiled_ingredients = self.find_duplicate_ingredients()
            
            available_recipes = []
            
            for recipe in recipes:
                
                for ingredient in compiled_ingredients:
                
                    #if id on recipe matches recipe_id on compiled_ingredients list
                    if recipe.id == ingredient['recipe_id']:
                    
                        #iterate through user_ingredients
                        for u_ingredient in user_ingredients:
                            
                            passed = True
                            
                            found_ingredient = False
                        
                            #if user_ingredient ingredient_id matches compiled_ingredient ingredient_id
                            if u_ingredient.ingredient_id == ingredient['ingredient_id']:
                                
                                found_ingredient = True
                            
                                #if quantity of user_ingredient <= quantity on compiled_ingredient
                                if u_ingredient.quantity <= ingredient['quantity']:
                                
                                    passed = False
                                
                            if passed == True and found_ingredient == True:
                                
                                available_recipes.append(recipe)
            
            #convert to dictionary to remove duplicates
            recipes = list(dict.fromkeys(available_recipes))
            
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized recipe instance
        """
        user = request.auth.user
        serializer = CreateRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a recipe

        Returns:
            Response -- Empty body with 204 status code
        """
        recipe = Recipes.objects.get(pk=pk)
        serializer = CreateRecipeSerializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        recipe = Recipes.objects.get(pk=pk)
        recipe.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes
    """
    class Meta:
        model = Recipes
        fields = ('description', 'name', 'style', 'user', 'starting_gravity', 'final_gravity', 'abv', 'ibu', 'srm', 'mash_ph', 'batch_volume', 'pre_boil_volume', 'boil_time', 'user')
        depth = 3
        
class CreateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ['description', 'name', 'style', 'user', 'starting_gravity', 'final_gravity', 'abv', 'ibu', 'srm', 'mash_ph', 'batch_volume', 'pre_boil_volume', 'boil_time']
        
