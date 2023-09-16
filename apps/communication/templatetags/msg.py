from django import template
register = template.Library()
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.vendor.models import Vendor
from ..models import Messages




@register.filter
@login_required
def user_messages(request):
    all_chats = []
    user_unique_id=request.user.unique_id
    """a user should see all vendor in his chat history, whether or not d user is currently  suscribed to that vendor"""
    read_msg = Messages.objects.filter(reciever_id=user_unique_id, is_seen=True).values('sender_id').order_by('-created_at')
    unread_msg = Messages.objects.filter(reciever_id=user_unique_id, is_seen=False).values('sender_id').order_by('-created_at')
    for i in unread_msg:
        vendor = Vendor.objects.values('store_name').get(unique_id=i['sender_id'])
        vendor_messages = Messages.objects.filter(sender_id=i['sender_id'], reciever_id=user_unique_id,is_seen=False)
        msg_count=vendor_messages.count()
        if [i['sender_id'], msg_count, vendor['store_name']] not in all_chats:
            all_chats.append([i['sender_id'], msg_count, vendor['store_name']])
    for msg in read_msg:
        vendor = Vendor.objects.values('store_name').get(unique_id=msg['sender_id'])
        for data in all_chats:
            if msg['sender_id'] is data[0]:
                pass
            elif msg['sender_id'] is not data[0]:
                all_chats.append([msg['sender_id'], 0, vendor['store_name']])
                break
    return render(request, 'communication/chat_platform.html', {'all_chats',all_chats})