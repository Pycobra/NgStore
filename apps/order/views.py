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

def payment_confirmation(data):
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