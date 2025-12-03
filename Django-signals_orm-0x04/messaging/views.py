from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect

@login_required
@cache_page(60)
def conversation_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Fetch only necessary fields for optimization
    messages = Message.objects.filter(
        sender=request.user,
        receiver=other_user
    ).select_related('sender', 'receiver').prefetch_related('replies').only('id', 'content', 'timestamp', 'read', 'parent_message')

    threads = []
    def get_threaded_replies(message):
        thread = []
        for reply in message.replies.all().only('id', 'content', 'timestamp', 'read', 'parent_message'):
            thread.append({
                'message': reply,
                'replies': get_threaded_replies(reply)
            })
        return thread

    for msg in messages:
        if msg.parent_message is None:
            threads.append({
                'message': msg,
                'replies': get_threaded_replies(msg)
            })

    return render(request, 'messaging/conversation.html', {
        'threads': threads,
        'other_user': other_user
    })

@login_required
def inbox(request):
    """Show only unread messages using the custom manager."""
    unread_messages = Message.unread.unread_for_user(request.user).select_related('sender').only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})

@login_required
def delete_user(request):
    """Allow the logged-in user to delete their account."""
    user = request.user

    if request.method == "POST":
        user.delete()  # <-- this deletes the user from the database
        messages.success(request, "Your account has been deleted.")
        return redirect("home")  # or any landing page after deletion

    return render(request, "messaging/delete_user_confirm.html")
