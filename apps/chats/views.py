from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

#@login_required
def index(request):
    return render(request, 'chats/index.html', {})


#@login_required
def room(request, room_name):
    return render(request, 'chats/room.html', {'room_name_json':mark_safe(json.dumps(room_name))})