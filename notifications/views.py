from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        notification_id = request.POST.get('notification_id')
        notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'success': True})
    
    context = {'notifications': notifications}
    return render(request, 'notifications/notification_list.html', context)