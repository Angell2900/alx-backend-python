import pytest
from django.contrib.auth.models import User
from messaging.models import Message, MessageHistory, Notification


@pytest.mark.django_db
class TestMessage:
    def setup_method(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        assert message.sender == self.user1
        assert message.receiver == self.user2
        assert message.content == 'Test message'
        assert message.read is False

    def test_message_str(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message content'
        )
        assert str(message) == f"{self.user1} -> {self.user2}: Test message conte"

    def test_message_reply(self):
        parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent_message
        )
        assert reply.parent_message == parent_message
        assert parent_message.replies.count() == 1


@pytest.mark.django_db
class TestMessageHistory:
    def setup_method(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )

    def test_message_history_creation(self):
        history = MessageHistory.objects.create(
            message=self.message,
            old_content='Old content',
            edited_by=self.user1
        )
        assert history.message == self.message
        assert history.old_content == 'Old content'
        assert history.edited_by == self.user1


@pytest.mark.django_db
class TestNotification:
    def setup_method(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user2,
            message=self.message
        )
        assert notification.user == self.user2
        assert notification.message == self.message
        assert notification.is_read is False

    def test_notification_str(self):
        notification = Notification.objects.create(
            user=self.user2,
            message=self.message
        )
        expected = f"Notification for {self.user2.username} about message {self.message.id}"
        assert str(notification) == expected
