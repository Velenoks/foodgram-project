from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .api.views import (AddPurchaseItem, RemovePurchaseItem, AddToFavorites,
                        RemoveFromFavorites, AddToSubscriptions,
                        RemoveFromSubscriptions, IngredientList)

views_patterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('recipe/<int:recipe_id>/edit/',
         views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/',
         views.delete_recipe, name='delete_recipe'),
    path('favorite/', views.favorite, name='favorite'),
    path('<str:username>/', views.user_recipe, name='user_recipe'),
    path('follow', views.follow, name='follow'),
    path('purchase', views.purchase_view, name='purchase'),
    path('purchase/download/',
         views.download_purchases, name='download_purchases'),
]

api_patterns = [
    path('purchases/', AddPurchaseItem.as_view()),
    path('purchases/<int:pk>/', RemovePurchaseItem.as_view()),
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
