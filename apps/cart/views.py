from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from decimal  import Decimal

from .cart import Cart
from .forms import CheckoutForm
from apps.order.utilities import checkout, email_notify_vendor, email_notify_customer
from apps.vendor.models import Vendor
from apps.product.models import Product


from apps.checkout.models import DeliveryOptions
from apps.order.models import Address

#import stripe
@login_required
def complete_payment(request):
    print('allaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
def shopping_cart(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        """if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']
            
            try:
                charge = stripe.Charge.create(
                    amount=int(account.get_total_cost() * 100),
                    currency='USD',
                    description='Charge from eCommerce',
                    source=stripe_token
                )
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']
    
                orderReciept = checkout(request, first_name, last_name, email, address, zipcode, place, phone, account.get_total_cost())
                account.clear()

                email_notify_vendor(orderReciept)
                email_notify_customer(orderReciept)
                
                return redirect('cart_:success_')

            except Exception:
                messages.error(request, 'There was something wrong with the payment')"""

    else:
        form = CheckoutForm()
    return render(request, 'cart/cart.html', {'form':form})#, 'stripe_pub_key':settings.STRIPE_PUB_KEY})

def success(request):
    return render(request, 'cart/index.html')

def cart_detail(request):
    cart = Cart(request)
    if request.POST:
        subAction = request.POST.get('subAction')
        productID = request.POST.get('productID')
        productQTY = 1
        if subAction == "delete":
            #item_quantity, item_total_cost, sub_total, total, delivery_price = cart.remove(product_id=productID)
            item_quantity, item_total_cost, sub_total, total, delivery_price = cart.remove(product_id=str(productID))
            response = JsonResponse(
                {'cart_length': cart.__len__(), "get_total_cost":cart.get_total_cost(),
                 'item_quantity': item_quantity,  'item_total_cost':item_total_cost,
                 'sub_total':sub_total, 'total':total, 'delivery_price':delivery_price})
            return response
        if subAction == 'add':
            product = get_object_or_404(Product, id=productID)
            product_exist = cart.add(product_id=productID, product=product, quantity=productQTY, update_quantity=False)
            response = JsonResponse(
                {'cart_length': cart.__len__(),'cart_length2': cart.__len__(), 'product_exist':product_exist})
            return response

        if subAction == 'update':
            product = get_object_or_404(Product, id=productID)
            item_quantity, item_total_cost, sub_total, total, delivery_price = cart.update(
                product_id=productID, product=product, quantity=productQTY, update_quantity=True)
            messages.success(request, 'The item was successfully updated in cart')
            response = JsonResponse(
                {'cart_length': cart.__len__(), "get_total_cost":cart.get_total_cost(),
                 'item_quantity': item_quantity, 'item_total_cost': item_total_cost,
                 'sub_total': sub_total, 'total': total, 'delivery_price': delivery_price})
            return response

        if subAction == 'subtract':
            product = get_object_or_404(Product, id=productID)
            item_quantity, item_total_cost, sub_total, total, delivery_price = cart.subtract(product_id=productID, quantity=productQTY, update_quantity=True)
            messages.success(request, 'The account was successfully subtracted from account')
            response = JsonResponse(
                {'cart_length': cart.__len__(), "get_total_cost":cart.get_total_cost(),
                 'item_quantity': item_quantity, 'item_total_cost': item_total_cost,
                 'sub_total': sub_total, 'total': total, 'delivery_price': delivery_price})
            return response


    session = request.session
    mydeliveryopt = {}
    mydeliveryadd = {}
    deliveryaddressess = {}
    if "purchase" in request.session:
        delivery_id = session["purchase"]['delivery_id']
        mydeliveryopt = DeliveryOptions.objects.get(id=delivery_id)
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True).exclude(id=delivery_id)
    else:
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    if "address" in request.session:
        address_id = session["address"]['address_id']
        mydeliveryadd = Address.objects.get(id=address_id)
        if request.user.is_authenticated:
            deliveryaddressess = Address.objects.filter(customer=request.user).exclude(id=address_id)
    else:
        if request.user.is_authenticated:
            deliveryaddressess = Address.objects.filter(customer=request.user)

    print(deliveryoptions, "deliveryoptionsdeliveryoptions")
    return render(request, 'cart/cart.html', {
        'deliveryoptions':deliveryoptions, 'deliveryaddressess':deliveryaddressess,
        'mydeliveryopt':mydeliveryopt, 'mydeliveryadd':mydeliveryadd})


def cart_update_address(request):
    session = request.session
    if request.POST.get("action") == "post":
        address_id = str(request.POST.get("address_id"))
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)
        address_type = Address.objects.get(id=address_id)
        if "address" not in session:
            session["address"] = {"address_id": address_id}
        else:
            session["address"]["address_id"] = address_id
            session.modified = True

    if request.POST.get("action") == "delete_address":
        address_id = str(request.POST.get("address_id"))
        Address.objects.filter(customer=request.user, id=address_id).delete()
        if "address" in session:
            if address_id == str(session["address"]["address_id"]):
                del session["address"]
                response = JsonResponse({'address_in_session':'true'})
                return response
    response = JsonResponse({'address_in_session': 'false'})
    return response





