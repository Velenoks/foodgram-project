from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IngredientSerializer
from ..models import Favorite, Follow, Ingredient, PurchaseItem


class AddToFavorites(APIView):
    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    def delete(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToSubscriptions(APIView):
    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            author_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromSubscriptions(APIView):
    def delete(self, request, pk, format=None):
        Follow.objects.filter(author_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddPurchaseItem(APIView):
    def post(self, request, format=None):
        PurchaseItem.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemovePurchaseItem(APIView):
    def delete(self, request, pk, format=None):
        PurchaseItem.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query or len(query) >= 3:
            return super().get(request, *args, **kwargs)
        return Response([{'warning': 'Введите минимум 3 символа'}, ])

    def get_queryset(self):
        query = self.request.query_params.get('query')
        if query:
            words = self.request.query_params.get('query').split(' ')
            db_query = Q()
            for word in words:
                db_query &= Q(title__contains=word[:-1].lower())
            return Ingredient.objects.all().filter(db_query)[:30]
        return Ingredient.objects.all()
