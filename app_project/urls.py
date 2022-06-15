"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from app_api.views import register_user, login_user
from app_api.views import RecipeView
from app_api.views.recipe_ingredients_view import RecipeIngredientsView
from app_api.views.steps_view import StepsView
from app_api.views.user_ingredients_view import UserIngredientsView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', RecipeView, 'recipe')
router.register(r'recipe_ingredients', RecipeIngredientsView, 'recipe_ingredient')
router.register(r'user_ingredients', UserIngredientsView, 'user_ingredient')
router.register(r'steps', StepsView, 'step')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]
