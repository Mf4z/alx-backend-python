from django.shortcuts import render

# chats/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving and creating conversations.
    """
    queryset = Conversation.objects.all()
    permission_classes = [permissions.AllowAny]  # adjust later if you add auth

    def get_serializer_class(self):
        if self.action in ['create']:
            return ConversationCreateSerializer
        return ConversationSerializer

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Optional extra route: /api/conversations/<id>/messages/
        """
        conversation = self.get_object()
        msgs = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(msgs, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    queryset = Message.objects.all().order_by('-sent_at')
    permission_classes = [permissions.AllowAny]  # adjust later if you add auth

    def get_serializer_class(self):
        if self.action in ['create']:
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        # in a real app, this should be request.user
        sender = getattr(self.request, 'user', None)
        serializer.save(sender=sender)

