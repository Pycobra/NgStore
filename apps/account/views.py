from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import smtplib

from .forms import RegistrationForm, ProfileEditForm, UserLoginForm
from .models import UserBase
from .token import account_activation_token

from apps.communication.models import Messages
from apps.order.forms import UserAddressForm, UserEditAddressForm
from apps.order.views import user_succesful_orders, vendor_succesful_orders
from apps.product.models import Product, Category
from apps.vendor.models import Vendor, Follow
from apps.order.models import OrderReciept, Address
from apps.checkout.models import DeliveryOptions



def new_user(request):
    users = UserBase.objects.all()
    return render(request, 'new_user.html', {'users': users})

import re
def registration_check2(request):
    content = request.GET.get('content')
    if request.GET.get('action') == 'check_username':
        it_exists = UserBase.objects.filter(user_name__exact=content).exists()
        response = JsonResponse({'exists': it_exists})
    if request.GET.get('action') == 'check_email':
        it_exists = UserBase.objects.filter(email__exact=content).exists()
        ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', content)
        print(f'correctly ends_with ({ends_with})')
        if ends_with != None:
            result2 = content.split('@')
            stri1 = ''
            stri2 = ''
            for i in result2:
                stri1 += i
            stri1 = stri1.split('.')
            for i in stri1:
                stri2 += i
            print(f'stripped result ({stri2})')
            contains_non_alpha_num = re.search(r"\W[-_/]", stri2)
            print('===============alpha & number container----------------------------')
            print(contains_non_alpha_num)
            if contains_non_alpha_num != None:
                print('===============yes contains non alpha & digit---------------------')

                unwanted_characterz = ['~', '@', '#', '$', '%', '^', '&', '*', '(', ')', \
                                       '_', '-', '+', '=', '[', ']', '{', '}', '|', '', ":", \
                                       ";", '"', "'", '<', ",", '>', ".", "/", "?"]
                contain_unwanted_characterz = False

                contains_the_required_chars = re.search(r"[-_/]", stri2)
                print(f'chars_container is ({contains_the_required_chars})')
                for i in stri2:
                    if i in unwanted_characterz:
                        print('===============it contains the required char---------------------')
                        contain_unwanted_characterz = True
                        return JsonResponse({'exists': it_exists})
                    break
                if contains_the_required_chars != None and not contain_unwanted_characterz:
                    print('===============it contains the required char---------------------')
                    return JsonResponse({'exists': it_exists})
        else:
            return JsonResponse({'exists': it_exists})
    if request.GET.get('action') == 'check_password':
        it_exists = UserBase.objects.filter(password__exact=content).exists()
        if ends_with != None:
            result2 = content.split('@')
            stri1 = ''
            stri2 = ''
            for i in result2:
                stri1 += i
            stri1 = stri1.split('.')
            for i in stri1:
                stri2 += i
            print(f'stripped result ({stri2})')
            contains_non_alpha_num = re.search(r"\W[-_/]", stri2)
            print('===============alpha & number container----------------------------')
            print(contains_non_alpha_num)
            if contains_non_alpha_num != None:
                print('===============yes contains non alpha & digit---------------------')

                unwanted_characterz = ['~', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                                       '_', '-', '+', '=', '[', ']', '{', '}', '|', '', ":",
                                       ";", '"', "'", '<', ",", '>', ".", "/", "?"]
                contain_unwanted_characterz = False

                contains_the_required_chars = re.search(r"[-_/]", stri2)
                print(f'chars_container is ({contains_the_required_chars})')
                for i in stri2:
                    if i in unwanted_characterz:
                        print('===============it contains the required char---------------------')
                        contain_unwanted_characterz = True
                        return JsonResponse({'exists': it_exists})
                    break
                if contains_the_required_chars != None and not contain_unwanted_characterz:
                    print('===============it contains the required char---------------------')
                    return JsonResponse({'exists': it_exists})
        else:
            return JsonResponse({'exists': it_exists})

        response = JsonResponse({'exists': it_exists})
    if request.GET.get('action') == 'check_password2':
        it_exists = UserBase.objects.filter(password2__exact=content).exists()
        response = JsonResponse({'exists': it_exists})
        char = ["/", '.', '-', '_']
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    return response

def registration_check(request):
    content = request.GET.get('content')
    if request.GET.get('action') == 'check_username':
        it_exists = UserBase.objects.filter(user_name__exact=content).exists()
        contains_characters = re.search(r"\W", content)
        if not it_exists:
            if len(content) >= 4:
                if contains_characters != None:
                    return JsonResponse({'msg_type':False, 'msg': 'Username must not include characters'})
                else:
                    return JsonResponse({'msg_type': True, 'msg': ''})
            else:
                return JsonResponse({'msg_type': False, 'msg': 'Username must be 4 or more characters'})
        else:
            return JsonResponse({'msg_type':False, 'msg': 'Username is already in use'})


    contain_unwanted_characterz = False
    if request.GET.get('action') == 'check_email':
        it_exists = UserBase.objects.filter(email__exact=content).exists()
        if not it_exists:
            contain_unwanted_characterz =False
            #checks & executes if it contains characters
            contains_non_characters = re.search(r"\W", content)
            if contains_non_characters != None:
                unwanted_characterz = ['~', '!', '#', '$', '%', '^', '&', '*', '(', ')', \
                             '+', '=', '[', ']', '{', '}', '|', '', ":", ";", '"', "'", \
                               '<', ",", '>', "?"]

                for i in content:
                    if i in unwanted_characterz:
                        contain_unwanted_characterz =True
                        break
            if contain_unwanted_characterz == True:
                return JsonResponse({'msg_type':False, 'msg': 'Email contain unwanted character'})

            # checks & executes if it doesnt contains characters at all / bad character
            elif contain_unwanted_characterz == False:
                ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', content)
                if ends_with != None:
                    return JsonResponse({'msg_type':True, 'msg': ''})
                else:
                    return JsonResponse({'msg_type':False, 'msg': "Email end contains wrong pattern, use ('gmail.com' etc)"})

        else:
            return JsonResponse({'msg_type':False, 'msg': 'Email is already in use'})


    if request.GET.get('action') == 'check_password':
        it_exists = UserBase.objects.filter(password__exact=content).exists()
        contains_characters = re.search(r"\W", content)
        contains_digit = re.search(r"\d", content)
        contains_white_space = re.search(r"\s", content)
        if len(content) >= 8:
            if contains_characters == None:
                return JsonResponse({'msg_type':False, 'msg': 'Password must include characters'})
            if contains_digit != None:
                print('cyyyyyyyyyyyyyyyyyyyyyyy')
            if contains_digit == None:
                return JsonResponse({'msg_type':False, 'msg': 'Password must include digits'})
            if contains_white_space != None:
                return JsonResponse({'msg_type':False, 'msg': 'Password allows no white space'})
            else:
                return JsonResponse({'msg_type':True, 'msg': ''})
        else:
            return JsonResponse({'msg_type':False,'msg': 'password must be longer than 8 characters'})
    if request.GET.get('action') == 'check_password2':
        it_exists = UserBase.objects.filter(password2__exact=content).exists()
        response = JsonResponse({'exists': it_exists})
        char = ["/",'.','-','_']
        num = [1,2,3,4,5,6,7,8,9,0]

    return JsonResponse({'exists': it_exists})


@login_required
def dashboard(request):
    user = UserBase.objects.get(unique_id=request.user.unique_id)
    all_account = UserBase.objects.all().exclude(unique_id=request.user.unique_id).order_by('-created_at')[:5]
    am_following = Follow.objects.filter(follower=user)
    unread_account_msg = Messages.objects.filter(reciever_id_unique=request.user.unique_id, is_seen=False).count()
    my_followers = {}
    unread_store_msg = {}
    if user.is_vendor:
        vendor = user.which_vendor
        unread_store_msg = Messages.objects.filter(reciever_id_unique=user.which_vendor.unique_id,
                                                   is_seen=False).count()
        my_followers = Follow.objects.filter(following=user.which_vendor)
    else:
        vendor = "no_vendor"

    return render(request, 'account/user/dashboard.html', {'account': user, 'my_followers': my_followers,
                                                           'all_account': all_account,
                                                           'vendor': vendor,
                                                           'unread_account_msg': unread_account_msg,
                                                           'unread_store_msg': unread_store_msg,
                                                           'am_following': am_following})
@login_required
def users_dashboard(request, id):
    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

    users = UserBase.objects.get(unique_id=id)
    all_account = UserBase.objects.all().exclude(id=users.id).order_by('-created_at')[:5]
    am_following = Follow.objects.filter(follower=users)
    unread_account_msg = Messages.objects.filter(reciever_id_unique=users.unique_id, is_seen=False).count()
    my_followers = {}
    unread_store_msg = {}

    if users.is_vendor:
        vendor = users.which_vendor
        unread_store_msg = Messages.objects.filter(reciever_id_unique=users.which_vendor.unique_id, is_seen=False).count()
        my_followers = Follow.objects.filter(following=users.which_vendor)
    else:
        vendor = "no_vendor"
    return render(request, 'account/user/dashboard.html', {'account':users, 'my_followers':my_followers,
                                    'all_account':all_account, 'vendor':vendor, 'unread_account_msg':unread_account_msg,
                                                           'unread_store_msg':unread_store_msg, 'am_following':am_following})
    #return render(request, 'account/user/dashboard.html', {user_order:user_order})


def search_account(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        account = UserBase.objects.get(user_name=request.user)
        all_account = UserBase.objects.all().order_by('-created_at')[:5]
        search_account = UserBase.objects.filter(Q(user_name__icontains=query))
        vendor = Vendor.objects.get(created_by=request.user)

        searches="""{% for i in searches %}
          <div class="other-accounts">
              <img class="" src="{{ i.user_image.url }}" alt="top-buyers-image">
              <div class="text">
                  <div class="name">{{ i.user_name }}</div>
                  <div><span style="font-weight:normal;font-size:14px;">Order</span> <span>N180</span></div>
              </div>
          </div>
          {% endfor %}
        """
        response = JsonResponse({'searches':searches})
        return response



@login_required
def dashboard_ajax(request):
    if request.POST.get('action') == 'get':
        query = request.POST.get('query')
        stores_user_follow = []
        if request.POST.get('mode') == 'user':
            account = UserBase.objects.filter(Q(user_name__icontains=query)).exclude(unique_id=request.user.unique_id).order_by('-created_at')[:5]
            if query == '':
                account = UserBase.objects.all().order_by('-created_at').exclude(unique_id=request.user.unique_id)[:5]
            serialized_queryset = serializers.serialize('python', account)

            #this block is to get tags(followers & non followers) of all users
            my_followers = {}
            if request.user.is_vendor:
                my_followers = Follow.objects.filter(following=request.user.which_vendor)

            all_account = UserBase.objects.all().exclude(unique_id=request.user.unique_id).order_by('-created_at')[:5]
            for user in all_account:
                for followers in my_followers:
                    if followers.follower == user:
                        stores_user_follow.append(followers.follower.user_name)

        elif request.POST.get('mode') == 'vendor':
            account = Vendor.objects.filter(Q(store_name__icontains=query)).exclude(unique_id=request.user.which_vendor.unique_id).order_by('-created_at')[:5]
            if query == '':
                account = Vendor.objects.all().order_by('-created_at').exclude(unique_id=request.user.which_vendor.unique_id)[:5]
            serialized_queryset = serializers.serialize('python', account)

            # this block is to get tags(followers & non followers) of all vendors
            all_vendor = Vendor.objects.all()
            am_following = Follow.objects.filter(follower=request.user)
            for store in all_vendor:
                for followers in am_following:
                    if followers.following == store:
                        stores_user_follow.append(followers.following.store_name)
        item = {}
        item['table'] = serialized_queryset

        #this block is just to pick out a vendorimg & inject it into his serialized vendor fields
        for i in item['table']:
            img_holder = VendorImageValue.objects.filter(vendor__id = i['pk'])
            for img in img_holder:
                img = VendorImages.objects.filter(alt_text = img.image_value)
                serialized_ = serializers.serialize('python', img)
                for s in serialized_:
                    i['fields']['images']= s['fields']['images']

        response = JsonResponse({'item': item, 'stores_user_follow':stores_user_follow})
    return response


@login_required
def dashboard_ajax2(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        account = UserBase.objects.filter(Q(user_name__icontains=query))
        if request.user.is_vendor:
            my_followers = Follow.objects.filter(following=request.user.which_vendor)

        serialized_queryset = serializers.serialize('python', account)

        for i in account:
            image = i.user_image.url

        item = {}
        item['my_followers'] = False
        for followers in my_followers:
            if followers.follower == account:
                item['my_followers'] = True
        item['table'] = serialized_queryset

        response = JsonResponse({'item': item, 'image': image})
    return response




def search_account_AJAX(request):
    if request.GET.get('action') == 'post':
        query = request.GET.get('productID')
        print(query)
        search_account = Product.objects.filter(Q(title__icontains=query) |
                                                Q(description__icontains=query) | Q(id__icontains=query)).values()
        response = JsonResponse({'all_account':search_account})
        return response

@login_required
def vendor_dashboard(request):
    vendor_order=vendor_succesful_orders(request)
    return render(request, 'account/user/dashboard.html', {vendor_order:vendor_order})

@login_required
def edit_profile(request):
    user=request.user
    if request.method == "POST":
        user_form = VendorEditForm(request.POST or None, request.FILES or None, instance=vendor)
        if user_form.is_valid():
            user=user_form.save(commit=False)
            user.email=user_form.cleaned_data['firstname']
            user.email=user_form.cleaned_data['surname']
            user.email=user_form.cleaned_data['mobile']
            user.save()
            return redirect('account_:dashboard')
    else:
        user_form = ProfileEditForm(instance=user)

    return render(request, 'account/user/edit_profile.html', {'form':user_form})
@login_required
def delete_account(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account_:delete_confirmation')

@csrf_exempt
def account_registration(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        registrationform = RegistrationForm(request.POST)
        if registrationform.is_valid():
            user=registrationform.save(commit=False)
            user.email=registrationform.cleaned_data['email']
            user.set_password(registrationform.cleaned_data['password'])
            user.is_active=False
            user.save()

            current_site=get_current_site(request)
            subject = "Activate your Account"
            msg = render_to_string('account/registration/account_activation_email.html', {
                      'user':user,
                      'domain': current_site.domain,
                      'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                      'token': account_activation_token.make_token(user),
            })
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                email_address = settings.EMAIL_HOST_USER
                email_password = settings.EMAIL_HOST_PASSWORD
                reciever_email_address = registrationform.cleaned_data['email']

                connection.login(email_address, email_password)
                connection.sendmail(
                    from_addr=email_address,
                    to_addrs=reciever_email_address,
                    msg=msg
                )
                # connection.quit()
            messages.success(request, "You successfully created an account, a mail was sent for confirmation")
            return redirect("/account/login/")
    else:
        registrationform=RegistrationForm()
        print('yes3')
    return render(request, 'account/registration/register.html', {'form':registrationform})

def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user=UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request, user)
        return redirect('account_:dashboard')
    else:
        return render(request, 'account/registration/account_activation_invalid.html')

@login_required
def likes_and_wishlist(request):
    wishlist = Product.objects.filter(users_wishlist=request.user)
    likes = Product.objects.filter(likes=request.user)
    return render(request, "account/user/user_wish_list.html", {"wishlist": wishlist, "likes": likes})

@login_required
def wishlist_add_and_remove(request, id):
    if request.GET.get('action') == 'get':
        product = get_object_or_404(Product, id=id)
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            product_exist = True
            action_text='<i class="fa fa-shopping-bag" id="icon1" style="color:var(--lightblue);"> Add</i>'
        else:
            product.users_wishlist.add(request.user)
            product_exist = False
            action_text='<i class="fa fa-shopping-bag" id="icon1" style="color:var(--lightblue);"> Remove</i>'
        users_wishlist = product.users_wishlist.all().count()
        response = JsonResponse({'wishlist_no': str(users_wishlist), 'action_text':action_text, 'product_exist':product_exist})
        return response
        
@login_required
def remove_from_wishlist(request):
    if request.GET.get('action') == 'get':
        id = request.GET.get('productID')
        product = get_object_or_404(Product, id=id)
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            messages.success(request, product.title + " has been removed from your WishList")
            wishlist_cnt = Product.objects.filter(users_wishlist=request.user).count()
            print(wishlist_cnt)
        response = JsonResponse({'wishlist_cnt':wishlist_cnt})
        return response

@login_required
def remove_from_likes(request):
    if request.GET.get('action') == 'get':
        id = request.GET.get('productID')
        product = get_object_or_404(Product, id=id)
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            messages.success(request, "you have unliked " + product.title)
            likes_cnt = Product.objects.filter(likes=request.user).count()
            print(likes_cnt)
        response = JsonResponse({'likes_cnt': likes_cnt})
        return response

@login_required
def view_address(request):
    address = Address.objects.filter(customer=request.user)
    return render(request, "account/user/addresses.html", {"address": address})


@login_required
def view_address2(request):
    if request.method == "POST":
        address_form = UserEditAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account_:addresses"))
    else:
        address_form = UserAddressForm(instance=request.user)
    return render(request, "account/user/addresses.html", {"form": address_form})

@login_required
def add_address(request):
    session = request.session
    if request.method == "POST":
        address_form = UserEditAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            if "address" not in session:
                session["address"] = {"address_id": str(address_form.pk)}
            address_form.save()
            return redirect('cart_:cart_detail')
        return redirect('.')
    else:
        address_form = UserAddressForm()
    return render(request,  "account/user/add_address.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("cart_:cart_details"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserEditAddressForm(instance=address)
    return render(request, "account/user/edit_address.html", {"form": address_form})


@login_required
def set_default(request):
    if request.POST.get('action') == 'post':
        address_id = request.POST.get('address_id')
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)

    response = JsonResponse({'address_id':address_id})
    return response

@login_required
def user_orders(request):
    user_id = request.user.id
    orders = OrderReciept.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})