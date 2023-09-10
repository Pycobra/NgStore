import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from apps.order.models import OrderReciept, OrderedItemDetail, Address, Checkout
from apps.cart.cart import Cart

from .models import DeliveryOptions, PaymentSelections


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


def cart_update_delivery(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = cart.cart_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {"delivery_id": delivery_type.id}
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True
        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if addresses:
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].pk)}
        else:
            session["address"]["address_id"] = str(addresses[0].pk)
            session.modified = True
        return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    # print(request.COOKIES)
    session = request.session
    if "address" not in session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        id = session["address"]['address_id']
        address = Address.objects.get(id=id)

    return render(request, "checkout/payment_selection.html", {'address': address})


@login_required
@csrf_exempt
def complete_payment(request):
    # def complete_payment(request: HttpRequest, response: str) -> HttpResponse:
    cart = Cart(request)
    session = request.session
    if request.POST.get('action') == 'post':
        ref = request.POST.get('ref')
        amount = request.POST.get('amount')
        address_id = session["address"]["address_id"]
        delivery_id = session["purchase"]["delivery_id"]
        total_paid = request.POST.get('total_paid')
        address = request.user.user_address.get(id=address_id)
        payment_selection = PaymentSelections.objects.get(name='Paystack')
        delivery_instructions = DeliveryOptions.objects.get(id=delivery_id)
        order = OrderReciept.objects.create(
            user_id=request.user.id, 
            delivery_address=address, 
            delivery_instructions=delivery_instructions,
            total_paid=total_paid, 
            payment_option=payment_selection,
            total_quantity= cart.__len__()
        )
        for item in cart:
            OrderedItemDetail.objects.create(
                order=order, product=item['product'], 
                vendor=item['product'].vendor,
                amount=item['total_price'], 
                quantity=item['quantity'])
        verified = order.verify_payment(total_paid, ref)
        if verified:
            order.verified = True
            order.save()
            Checkout.objects.create(order=order, ref=ref)
            messages.success(request, "Payment verification was sucessfull")
        else:
            messages.success(request, "Your payment verification failed")
        # return redirect('.')
    response = JsonResponse({})
    return response

@login_required
@csrf_exempt
def user_details_authenticated(request):
    session = request.session
    cart = Cart(request)
    mydeliveryopt = False
    mydeliveryadd = False
    address={'email':'', 'phone':''}
    delivery = {'delivery_price': ""}
    key = settings.PAYSTACK_PUBLIC_KEY
    if request.GET:
        if "purchase" in request.session:
            delivery_id = session["purchase"]["delivery_id"]
            mydeliveryopt = True
            delivery = DeliveryOptions.objects.get(id=delivery_id)
            delivery = {'delivery_price': delivery.delivery_price}
        if "address" in request.session:
            address_id = session["address"]["address_id"]
            mydeliveryadd = True
            address = Address.objects.get(id=address_id)
            address = {'email': address.email, 'phone': address.phone}

    response = JsonResponse({
        "userHasdeliveryopt": mydeliveryopt, 
        "userHasdeliveryadd": mydeliveryadd, 
        'amt': cart.get_total_cost(), 
        "email": address["email"], 
        "delivery_price": delivery["delivery_price"],
        "phone": address["phone"],
        'key': key,
        'user_name': request.user.user_name,
    })
    return response







