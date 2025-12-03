from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
  
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        instance.edited = True  

        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.edited_by
        )


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming the Message model has a 'recipient' field
        if hasattr(instance, 'recipient') and instance.recipient:
            Notification.objects.create(
                user=instance.recipient,
                message=instance
            )
