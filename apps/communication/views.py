import datetime
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers

import random
from apps.cart.cart import Cart
from apps.product.forms import AddToCartForm, AddCategoryForm, ColorSearchForm
from apps.product.models import Category, Product, ProductType, ProductSpecificationValue, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.communication.forms import NewCommentForm


from apps.product.models import Product, Comments
from apps.vendor.models import Vendor, Subscriptions
from apps.account.models import UserBase
from .forms import MessageForm
from .models import Messages





@login_required
def messages_history(request, user_or_vendor_unique_id):
    for i in request.user.which_vendor.vendor_follower.all():
        print(i.follower.user_name)
    all_sender_list = []
    msg_sender_data = []
    unread_msg = Messages.objects.filter(reciever_id_unique=user_or_vendor_unique_id, is_seen=False).order_by('-created_at')
    read_msg = Messages.objects.filter(reciever_id_unique=user_or_vendor_unique_id, is_seen=True).order_by('-created_at')
    try:
        user = UserBase.objects.get(unique_id=user_or_vendor_unique_id)
    except:
        user = Vendor.objects.get(unique_id=user_or_vendor_unique_id)

    for i in unread_msg:
        vendor_messages = Messages.objects.filter(sender_id_unique=i.sender_id_unique, reciever_id_unique=user_or_vendor_unique_id,
                                                  is_seen=False)
        msg_count = vendor_messages.count()
        # this line will append that users every msg
        print(i.sender_id_unique)
        if i.sender_id_unique not in all_sender_list:
            all_sender_list.append(i.sender_id_unique)
            try:
                sender = UserBase.objects.get(unique_id=i.sender_id_unique)
                print('place--------1')
                print(sender.is_authenticated)
                msg_sender_data.append([sender, sender.unique_id, sender.user_name, sender.user_image, i.content, i.get_date, msg_count, 'a_vendor'])
            except:
                sender = Vendor.objects.get(unique_id=i.sender_id_unique)
                online = sender.created_by.is_authenticated
                print('place--------2')
                print(online)
                msg_sender_data.append([sender, sender.unique_id, sender.store_name, sender.vendor_image.all(), i.content, i.get_date, msg_count, 'a_user'])

    for i in read_msg:
        if i.sender_id_unique not in all_sender_list:
            all_sender_list.append(i.sender_id_unique)
            try:
                sender = UserBase.objects.get(unique_id=i.sender_id_unique)
                print('place--------3')
                print(sender.is_authenticated)
                msg_sender_data.append([sender, sender.unique_id, sender.user_name, sender.user_image, i.content, i.get_date, 0, 'a_vendor'])

            except:
                sender = Vendor.objects.get(unique_id=i.sender_id_unique)
                online = sender.created_by.is_authenticated
                print('place--------4')
                print(online)
                msg_sender_data.append([sender, sender.unique_id, sender.store_name, sender.vendor_image.all(), i.content, i.get_date, 0, 'a_user'])
    form = MessageForm()
    print(msg_sender_data)

    return render(request, 'communication/chat_platform.html', {"msg_sender_data": msg_sender_data, 'user':user, 'form': form})


@login_required
def get_message(request, user_unique_id, logged_in_user_unique_id):
    messages = Messages.objects.filter(sender_id_unique=user_unique_id, reciever_id_unique=logged_in_user_unique_id, is_seen=False)
    for status in messages:
        status.is_seen = True
        status.save()
    all_sender_list = []
    msg_sender_data = []
    unread_msg = Messages.objects.filter(reciever_id_unique=logged_in_user_unique_id, is_seen=False).order_by('-created_at')
    read_msg = Messages.objects.filter(reciever_id_unique=logged_in_user_unique_id, is_seen=True).order_by('-created_at')
    for i in unread_msg:
        vendor_messages = Messages.objects.filter(sender_id_unique=i.sender_id_unique, reciever_id_unique=logged_in_user_unique_id,
                                                  is_seen=False)
        msg_count = vendor_messages.count()
        # this line will append that users every msg
        if i.sender_id_unique not in all_sender_list:
            all_sender_list.append(i.sender_id_unique)
            try:
                sender = UserBase.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender.unique_id, sender.user_name, sender.user_image, i.content, i.get_date, msg_count, 'a_vendor'])
            except:
                sender = Vendor.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender.unique_id, sender.store_name, sender.vendor_image.all(), i.content, i.get_date, msg_count, 'a_user'])


    for i in read_msg:
        if i.sender_id_unique not in all_sender_list:
            all_sender_list.append(i.sender_id_unique)
            try:
                sender = UserBase.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender, sender.unique_id, sender.user_name, sender.user_image, i.content, i.get_date, 0, 'a_vendor'])

            except:
                sender = Vendor.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender, sender.unique_id, sender.store_name, sender.vendor_image.all(), i.content, i.get_date, 0, 'a_user'])

    user_or_vendor_id = [user_unique_id, logged_in_user_unique_id]
    our_chat = Messages.objects.filter(sender_id_unique__in=user_or_vendor_id, reciever_id_unique__in=user_or_vendor_id).values(
        "sender_id_unique", 'content', 'created_at').order_by('-created_at')
    try:
        user_unique_id = UserBase.objects.get(unique_id=user_unique_id)
    except:
        user_unique_id = Vendor.objects.get(unique_id=user_unique_id)
    form = MessageForm()
    return render(request, 'communication/chat_platform2.html', {"our_chat":our_chat, "user_id":[user_unique_id, logged_in_user_unique_id],
                                                                "msg_sender_data": msg_sender_data, 'form': form})

@login_required
def send_message(request, user_unique_id, logged_in_user_unique_id):
    all_sender_list = []
    msg_sender_data = []

    if request.method == "POST":
        sent_message = request.POST.get('sent_message', '')
        Messages.objects.create(sender_id_unique=logged_in_user_unique_id,content=sent_message,
                                reciever_id_unique=user_unique_id)
    unread_msg = Messages.objects.filter(reciever_id_unique=logged_in_user_unique_id, is_seen=False).order_by('-created_at')
    read_msg = Messages.objects.filter(reciever_id_unique=logged_in_user_unique_id, is_seen=True).order_by('-created_at')
    for i in unread_msg:
        vendor_messages = Messages.objects.filter(sender_id_unique=i.sender_id_unique, reciever_id_unique=logged_in_user_unique_id,
                                                  is_seen=False)
        msg_count = vendor_messages.count()
        # this line will append that users every msg
        if i.sender_id_unique not in all_sender_list:
            all_sender_list.append(i.sender_id_unique)
            try:
                sender = UserBase.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender, sender.unique_id, sender.user_name, sender.user_image, i.content, i.get_date, msg_count, 'a_vendor'])
            except:
                sender = Vendor.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender, sender.unique_id, sender.store_name, sender.vendor_image.all(), i.content, i.get_date, msg_count, 'a_user'])


    for i in read_msg:
        if i.sender_id_unique not in all_sender_list:
            all_sender_list.append(i.sender_id_unique)
            try:
                sender = UserBase.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender, sender.unique_id, sender.user_name, sender.user_image, i.content, i.get_date, 0, 'a_vendor'])
            except:
                sender = Vendor.objects.get(unique_id=i.sender_id_unique)
                msg_sender_data.append([sender, sender.unique_id, sender.store_name, sender.vendor_image.all(), i.content, i.get_date, 0, 'a_user'])

    user_or_vendor_id = [user_unique_id, logged_in_user_unique_id]
    our_chat = Messages.objects.filter(sender_id_unique__in=user_or_vendor_id, reciever_id_unique__in=user_or_vendor_id).values(
        "sender_id_unique", 'content', 'created_at').order_by('-created_at')
    try:
        user_unique_id = UserBase.objects.get(unique_id=user_unique_id)
    except:
        user_unique_id = Vendor.objects.get(unique_id=user_unique_id)
    form = MessageForm()
    return render(request, 'communication/chat_platform2.html', {"our_chat":our_chat, "user_id":[user_unique_id, logged_in_user_unique_id],
                                                                "msg_sender_data": msg_sender_data, 'form': form})



@login_required
def send_fleet_message(request):
    if request.POST.get('do_action') == 'post_it':
        unique_id_list = request.POST.getlist('unique_id_list[]')
        sent_fleet_msg = request.POST.get('sent_fleet_msg')
        for unique_id in unique_id_list:
            Messages.objects.create(sender_id_unique=request.user.which_vendor.unique_id,
                                reciever_id_unique=unique_id, content=sent_fleet_msg)
        print("BIG MESSA?Ge ?BOY")
        response = JsonResponse()
        return response



@login_required
def get_message_ajax(request, id):
    if request.POST.get('action') == 'get_msg':
        ids = []
        user_or_vendor_id = request.POST.get('ID')
        print(user_or_vendor_id)
        if Vendor.objects.filter(unique_id=user_or_vendor_id).exists():
            user_id = request.user.unique_id
            ids = [user_id, user_or_vendor_id]
        elif UserBase.objects.filter(unique_id=user_or_vendor_id).exists():
            user_id = request.user.which_vendor.unique_id
            ids = [user_id, user_or_vendor_id]
        all_chats = Messages.objects.filter(sender_id__in=ids, reciever_id__in=ids).values(
            'content', 'created_at').order_by('-created_at')
        for i in all_chats:
            print(i['content'])
            print(i['created_at'].second)

    #    response = JsonResponse({'all_chats': all_chats})
    #return response
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def make_comment2(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        product_id = request.POST.get('product_id')
        products = Product.objects.get(id=product_id)
        wishlist = products.users_wishlist.all().count()
        likes = products.likes.all().count()
        product_id = str(products.id)
        wishlist_boolean = False
        like_boolean = False
        product_spec = ProductSpecificationValue.objects.filter(product=products)

        # ------------------------------------------------------
        if request.user.is_authenticated:
            Comments.objects.create(made_by=request.user,
                                    name=request.user.firstname + " " + request.user.surname,
                                    email=request.user.email, default_image=request.user.user_image,
                                    made_on=products, parent=None, content=comment)
        else:
            if not request.user.is_authenticated and name != "" and email != "":
                Comments.objects.create(made_by=None, name=name, email=request.user.email,
                                        made_on=products, parent=None, content=comment)
            else:
                error = "e no follo"

                response = JsonResponse({'comments': error})
                return response

        allcomments = products.comments.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(allcomments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        if products.users_wishlist.filter(id=request.user.id).exists():
            wishlist_boolean = True
        if products.likes.filter(id=request.user.id).exists():
            like_boolean = True

        # ----------------------------------------------------
        similar_products = list(products.category.product_category.exclude(id=products.id))
        if len(similar_products) >= 4:
            similar_products = random.sample(similar_products, 4)
        # -------------------------------------------------
        breadcrumbs_link = products.get_cat_list()
        category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
        breadcrumbs = zip(breadcrumbs_link, category_name)


        comment_form = NewCommentForm()
        form = AddToCartForm()

        return render(request, 'product/product.html',
                      {'comment_form': comment_form, 'product': products, 'product_id': product_id,
                       'wishlist': str(wishlist), 'wishlist_boolean': wishlist_boolean,
                       'likes': str(likes), 'like_boolean': like_boolean, 'allcomments': allcomments,
                       'comments': comments,
                       'product_spec': product_spec, 'breadcrumbs': breadcrumbs})

def make_comment(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        parent = request.POST.get('parent')
        print(parent)
        if parent == "":
            parent = None
        else:
            parent = Comments.objects.get(id=parent)

        if request.user.is_authenticated:
            cmt = Comments.objects.create(made_by=request.user, name=request.user.firstname + " " + request.user.surname,
                         email=request.user.email, default_image=request.user.user_image, made_on=product, parent=parent, content=comment)
        else:
            if not request.user.is_authenticated and name != "" and email != "":
                cmt = Comments.objects.create(name=name, email=email,
                             made_on=product, parent=parent, content=comment)

            else:
                if not request.user.is_authenticated and name == "":
                    pass
                if not request.user.is_authenticated and email == "":
                    pass
                error = "pls enter your name & email address"

                response = JsonResponse({'error':False})
                return response

        comments = Comments.objects.filter(id=cmt.id, made_on=cmt.made_on)
        for i in comments:
            image = i.default_image.url
            made_by = i.made_by

        serialized_queryset = serializers.serialize('python', comments)
        comments = {}
        comments['result'] = 'Comment made successfully!'
        comments['table'] = serialized_queryset
        """{'model': 'product.comments', 'pk': '854edb04-8388-4b64-920d-82fab08eac7d',
         'fields': {'made_by': 1, 'name': 'bright orji', 'email': '1@1.com',
         'default_image': 'images/uploads/ian-dooley-TT-ROxWj9nA-unsplash.png', 'made_on': 41,
         'parent': None, 'content': 'qwerrtr',
                    'made_at': datetime.datetime(2022, 1, 12, 22, 14, 41, 39362,
                                                 tzinfo= < UTC >), 'lft': 1, 'rght': 2, 'tree_id': 3, 'level': 0}}"""
        response = JsonResponse({'error':True,'comments': comments, 'image':image, 'made_by':str(made_by)})
        return response


"""
{% load index %}
{{my_list|index:x}}

templatetags/index.py

from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]
if my_list = [[],[]]
use {{my_list|index:x|index:y}} in template to get  my_list[x][y]
"""