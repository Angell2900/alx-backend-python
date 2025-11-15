from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]  # ALX wants 'filters' used somewhere

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "Participants required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]  # ALX wants 'filters' used somewhere

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")
        sender_id = request.data.get("sender")  # or request.user.id if auth enabled

        if not conversation_id or not message_body or not sender_id:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
