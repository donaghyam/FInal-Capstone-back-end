
from django.shortcuts import render
from django.db import connection
from django.views import View

from .helpers import dict_fetch_all


class FavoritedList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT 
                    u.username as username,
                    r.name as recipe_name
                FROM auth_user u
                JOIN app_api_favorite f
                    ON f.user_id = u.id 
                JOIN app_api_recipes r 
                    ON r.id = f.recipe_id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            favorites = []

            for row in dataset:
                recipe = {
                    "username": row['username'],
                    "recipe_name": row['recipe_name']
                }
                
                favorites.append(recipe)

        # The template string must match the file name of the html template
        template = 'list_favorites.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "favorites_list": favorites
        }

        return render(request, template, context)
