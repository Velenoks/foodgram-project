from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .api.views import *


views_patterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('favorite/', views.favorite, name='favorite'),
    path('<str:username>/', views.user_recipe, name='user_recipe'),
    path('follow', views.follow, name='follow')
]

api_patterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('subscriptions/', AddToSubscriptions.as_view()),
    path('subscriptions/<int:pk>/', RemoveFromSubscriptions.as_view()),
    path('ingredients/', IngredientList.as_view()),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
]