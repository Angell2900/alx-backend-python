from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')  # Redirect to homepage after deletion
    return render(request, 'messaging/delete_user.html', {'user': user})


def get_threaded_replies(message):
    """Recursively fetch replies for a message."""
    thread = []
    for reply in message.replies.all():
        thread.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return thread

@login_required
@cache_page(60)  # Cache page for 60 seconds
def conversation_messages(request, user_id):
    """View to fetch messages between the logged-in user and another user."""
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender=request.user,
        receiver=other_user
    ).select_related('sender', 'receiver').prefetch_related('replies')

    # Build threaded messages
    threads = []
    for msg in messages:
        if msg.parent_message is None:  # Only top-level messages
            threads.append({
                'message': msg,
                'replies': get_threaded_replies(msg)
            })

    return render(request, 'messaging/conversation.html', {
        'threads': threads,
        'other_user': other_user
    })
