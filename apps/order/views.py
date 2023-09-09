from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect

from apps.cart.cart import Cart
from apps.checkout.models import PaymentSelections

from  .models import OrderReciept, OrderedItemDetail, Address, Checkout
from .forms import UserAddressForm, UserEditAddressForm




def user_orders(request, user_name, unique_id):
    order_reciept = OrderReciept.objects.filter(user__id=request.user.id).order_by("-created")
    checkout = Checkout.objects.filter(order__in=order_reciept)
    ordered_item_detail = OrderedItemDetail.objects.filter(order__in=order_reciept)
    album = []
    for order in order_reciept:
        pics = []
        for ordered_item in ordered_item_detail:
            if ordered_item.order.order_key == order.order_key:
                pics.append(ordered_item)
        album.append(pics)


    return render(request, 'order/user_order.html', {'order_reciept': order_reciept, 'ordered_item_detail': ordered_item_detail,
                                                     'album':album})

def vendor_orders(request, store_name, unique_id):
    vendor = request.user.which_vendor
    ordered_item_detail = OrderedItemDetail.objects.filter(vendor=vendor)
    order_key = set()
    for i in ordered_item_detail:
        order_key.add(i.order.order_key)
    order_reciept = OrderReciept.objects.filter(order_key__in=order_key).order_by("-created")

    album = []
    for order in order_reciept:
        pics = []
        for ordered_item in ordered_item_detail:
            if ordered_item.order.order_key == order.order_key:
                pics.append(ordered_item)
        album.append(pics)


    return render(request, 'order/user_order.html', {'order_reciept': order_reciept, 'ordered_item_detail': ordered_item_detail,
                                                     'album':album})
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect

from apps.chats.chats import Cart
from apps.checkout.models import PaymentSelections

from  .models import OrderReciept, OrderedItemDetail, Address
from .forms import UserAddressForm, UserEditAddressForm






def add_checkout(request):
    chats = Cart(request)
    # user, first_name, last_name, email, address1, address2, post_code, city, phone, total_paid, order_key, payment_option
    if request.POST.get("action") == "post":
        user = request.user
        # order_key = request.POST.get("order_key")
        user_address = Address.objects.filter(customer=request.user, default=True)
        baskettotal = chats.get_total_price()
        #payment_option = PaymentSelections.objects.get(default=True)
        if request.user.is_authenticated:
            order = OrderReciept.objects.create(user=user, full_name=user_address.full_name, email=user_address.email,
                                                address1=user_address.address1, address2=user_address.address2,
                                                post_code=user_address.post_code, city=user_address.city,
                                               phone=user_address.phone, total_paid=baskettotal,
                                                payment_option=user_address.payment_option)
        else:
            if chats['address']:
                for item in chats:
                    order = OrderReciept.objects.create(full_name=item['address'].full_name,
                                                        email=item['address'].email,
                                                        address1=item['address'].address1, address2=item['address'].address2,
                                                        post_code=item['address'].post_code, city=item['address'].city,
                                                        phone=item['address'].phone, total_paid=baskettotal,
                                                        payment_option=item['address'].payment_option)
        for item in chats:
            OrderedItemDetail.objects.create(order=order, product=item['product'],
                                             vendor=item['product'].vendors_related_name, price=item['price'],
                                             quantity=item['quantity'], )

    response = JsonResponse({'success': 'yahoo yahoo yahoo com '})
    return response



@login_required
def view_address(request):
    address = Address.objects.filter(customer=request.user)
    return render(request, "order/addresses.html", {"address": address})


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
    #addresses = Address.objects.filter(customer=request.user)
    return render(request, "order/addresses.html", {"form": address_form})


@login_required
def add_address(request):
    session = request.session
    if "purchase" in request.session:
        if request.method == "POST":
            address_form = UserEditAddressForm(data=request.POST)
            if address_form.is_valid():
                address_form = address_form.save(commit=False)
                address_form.customer = request.user
                address_form.save()
                return HttpResponseRedirect(reverse("cart_:cart_details"))
        else:
            address_form = UserEditAddressForm()
            print(('zigggggggggggy'))
            return render(request, "order/user_order.html", {"form": address_form})
    else:
        response = JsonResponse({None:None})
        return response


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account_:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserEditAddressForm(instance=address)
    return render(request, "order/edit_address.html", {"form": address_form})


@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("orders_:addresses")


@login_required
def set_default(request):
    if request.POST.get('action') == 'post':
        address_id = request.POST.get('address_id')
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)

    response = JsonResponse({'address_id':address_id})
    return response
"""
def set_default(request):
    if request.POST.get('action') == 'post':
        address_id = request.POST.get('address_id')
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    response = JsonResponse({'address_id':address_id})
    return response
"""




@login_required
def user_orders(request):
    user_id = request.user.id
    orders = OrderReciept.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

"""




def payment_confirmation(data):
    #OrderReciept.objects.filter(order_key=data).update(billing_status=True)
    bill = OrderedItemDetail.objects.filter(ref=data)
    bill.order.objects.update(billing_status=True)

def user_succesful_orders(request):
    user=request.user
    order=OrderReciept.objects.filter(user=user).filter(billing_status=True)
    return order
def vendor_succesful_orders(request):
    vendor = request.user.which_vendor
    order = vendor.orderReciept.filter(billing_status=True)
    return order