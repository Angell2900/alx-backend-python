from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from .models import Message 
@login_required
def delete_user(request):
    user = request.user
    user.delete()  # Deletes the user
    return redirect('home')  # Redirect to home page after deletion

@cache_page(60)  # 60-second cache
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    return render(request, 'messaging/conversation.html', {'messages': messages})