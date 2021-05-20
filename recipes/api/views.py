from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Favorite, Follow


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
