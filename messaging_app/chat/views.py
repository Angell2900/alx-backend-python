from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import json

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = Message.objects.create(content=data.get('content', ''))
        return JsonResponse({'status': 'success', 'id': message.id})
    return JsonResponse({'status': 'error'})

def get_messages(request):
    messages = Message.objects.all().values('id', 'content', 'timestamp')
    return JsonResponse(list(messages), safe=False)

def health_check(request):
    return JsonResponse({'status': 'healthy', 'version': '1.0'})