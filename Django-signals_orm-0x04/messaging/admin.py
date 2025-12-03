from django.contrib import admin
from .models import Message, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'edited_by', 'edited_at', 'timestamp', 'sender', 'receiver', 'edited')

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'edited_by', 'edited_at')
