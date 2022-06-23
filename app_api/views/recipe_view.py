"""View module for handling recipe requests """

from django.http import HttpResponseServerError
from app_api.models import Recipes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db import connection
from app_api.views.helpers import dict_fetch_all


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
    def find_duplicate_ingredients(self, request, recipe_id):
        with connection.cursor() as db_cursor:
            
            user = request.auth.user

            db_cursor.execute("""
                SELECT *
                FROM (
                    SELECT
                        r.*,
                        ri.ingredient_id,
                        i.name recipe_ingredient_name,
                        SUM(ri.quantity) as recipe_quantity
                    FROM app_api_recipes r
                    JOIN app_api_recipeingredients ri
                        ON r.id = ri.recipe_id
                    JOIN app_api_ingredients i 
                        ON i.id = ri.ingredient_id
                    WHERE r.id = %s
                    GROUP BY ri.ingredient_id
                ) as r
                LEFT JOIN (
                    SELECT
                        ui.ingredient_id,
                        i.name user_ingredient_name,
                        ui.quantity user_quantity
                    FROM auth_user u 
                    JOIN app_api_useringredients ui
                        ON u.id = ui.user_id
                    JOIN app_api_ingredients i 
                        ON i.id = ui.ingredient_id
                    WHERE u.id = %s
                ) as u 
                ON r.ingredient_id = u.ingredient_id
            """, (recipe_id, user.id,))
            
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            recipes = []

            for row in dataset:
                ingredient = {
                    "user_ingredient_name": row['user_ingredient_name'],
                    "recipe_ingredient_name": row['recipe_ingredient_name'],
                    "ingredient_id": row['ingredient_id'],
                    "recipe_quantity": row['recipe_quantity'],
                    "user_quantity": row['user_quantity'],
                }
                
                recipe_dict = None 
                for recipe_ingredient in recipes:
                    if recipe_ingredient['recipe_id'] == row['id']:
                        recipe_dict = recipe_ingredient
                        
                if recipe_dict:
                    recipe_dict['ingredient'].append(ingredient)
                
                else:
                    recipes.append({
                        "recipe_id": row['id'],
                        "ingredient": [ingredient]
                    })
            
            return recipes
            
    @action(methods=['get'], detail=False)
    def compare_ingredients(self, request):      
        
        recipes = Recipes.objects.all() 
        
        recipes_with_ingredients = []
        
        for recipe in recipes:
            
            #get list of compiled ingredients
            recipes_with_ingredients.append(self.find_duplicate_ingredients(request, recipe.id))
        
        available_recipes = []
        
        for recipe in recipes_with_ingredients:
            add_recipe = True
            
            for ingredient in recipe[0]['ingredient']:
                if ingredient['user_quantity'] is None or ingredient['user_quantity'] < ingredient['recipe_quantity']:
                    add_recipe = False
                    break
            if add_recipe is False:
                continue
            
            if add_recipe is True:
                available_recipes.append(recipe)
                
        recipes_to_list = []
                
        for recipe in available_recipes:
            recipe = Recipes.objects.get(pk=recipe[0]['recipe_id'])
            recipes_to_list.append(recipe)
            
        serializer = RecipeSerializer(recipes_to_list, many=True)
        return Response(serializer.data)
        
    @action(methods=['get'], detail=False)
    def retrieve_most_recent(self, request):
        
        #get all recipes            
        recipes = Recipes.objects.all()        
        
        recent_recipe_list = recipes.order_by('-id')
        
        recent_recipe = recent_recipe_list[0]
            
        serializer = RecipeSerializer(recent_recipe, many=False)
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
        fields = ('id', 'description', 'name', 'style', 'starting_gravity', 'final_gravity', 'abv', 'ibu', 'srm', 'mash_ph', 'batch_volume', 'pre_boil_volume', 'boil_time', 'user')
        depth = 3
        
class CreateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ['description', 'name', 'style', 'starting_gravity', 'final_gravity', 'abv', 'ibu', 'srm', 'mash_ph', 'batch_volume', 'pre_boil_volume', 'boil_time']
        
