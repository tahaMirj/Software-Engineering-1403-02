import copy

from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import views, generics
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlockSerializer
from group2_chat.models import Chat


class BlockView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        client = request.user

        serializer = BlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data["username"]
        if client.username == username:
            return Response(
                {"error": "can't block yourself"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        with transaction.atomic():
            chat = Chat.get_or_create_direct_chat(client, other_user)
            chat.blocked = True
            chat.blocked_by = client
            chat.save()

        return Response({"ok": True}, status=status.HTTP_200_OK)


class UnblockView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        client = request.user

        serializer = BlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data["username"]
        if client.username == username:
            return Response(
                {"error": "not blocked by you"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        chat = Chat.get_or_create_direct_chat(
            client, User.objects.get(username=username)
        )
        if not chat.blocked or chat.blocked_by != client:
            return Response(
                {"error": "not blocked by you"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        with transaction.atomic():
            chat.blocked = False
            chat.blocked_by = None
            chat.save()

        return Response({"ok": True}, status=status.HTTP_200_OK)
