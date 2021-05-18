from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/', views.user_recipe, name='user_recipe'),
    #path('api/favorites/', AddToFavorites.as_view()),
    #path('api/favorites/<int:pk>/', RemoveFromFavorites.as_view()),
]
