from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory
from django.utils import timezone

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, nothing to log
        return
    
    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    
    if old_instance.content != instance.content:
        # Save old content in history
        MessageHistory.objects.create(
            message=instance,
            old_content=old_instance.content,
            edited_at=timezone.now(),
            edited_by=instance.edited_by  # make sure your view sets this
        )
        # Update the edited timestamp
        instance.edited_at = timezone.now()
