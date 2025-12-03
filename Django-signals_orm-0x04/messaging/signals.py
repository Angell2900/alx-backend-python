from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, nothing to log
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        instance.edited = True  # mark as edited
        # Save old content to history
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.edited_by
        )
