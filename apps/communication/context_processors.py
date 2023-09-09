from .models import Messages

def messages_number(request):
    recieved_by_user=0
    if request.user.is_authenticated:
        unique_id=request.user.unique_id
        recieved_by_user = Messages.objects.filter(reciever_id_unique=unique_id, is_seen=False).count()
    return {'chats':recieved_by_user}


