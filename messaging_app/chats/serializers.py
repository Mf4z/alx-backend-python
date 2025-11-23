# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # keep it simple but useful
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at', 'sender']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at', 'messages']


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    For creating a conversation with a list of participant IDs.
    """
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source='participants',
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participant_ids', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    For creating messages — we set sender from request.user in the view.
    """
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at']
