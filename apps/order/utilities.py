from apps.cart.cart import Cart
from  .models import OrderReciept, OrderedItemDetail

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse


def checkout(request, first_name ,last_name ,email ,address ,zipcode , place ,phone , paid_amount):
    orderReciept = OrderReciept.objects.create(first_name=first_name, last_name=last_name,
                                               email=email, address=address, zipcode=zipcode, place=place,
                                               phone=phone, paid_amount=paid_amount)

    for item in Cart(request):
        OrderedItemDetail.objects.create(order=orderReciept, product=item['product'],
                                         vendor=item['product'].vendor, price=item['product'].price,
                                         quantity=item['product'].quantity,)
        orderReciept.vendors.add(item['product'].vendor)

    return orderReciept

def add_checkout(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        user_id = request.user.id
        cart_total = cart.get_total_price()
        order_key = request.POST.get('order_key')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        phone = request.POST.get('phone')


        if OrderReciept.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = OrderReciept.objects.create(user_id=user_id, first_name=first_name, last_name=last_name, city=city,
                                               email=email, address1=address1, address2=address2, zipcode=zipcode, country=country,
                                               phone=phone, paid_amount=cart_total, order_key=order_key)
            order_id = order.pk
            for item in cart:
                OrderedItemDetail.objects.create(order=order_id, product=item['product'],
                                                 vendor=item['product'].vendor, price=item['product'].price,
                                                 quantity=item['product'].quantity, )

        response = JsonResponse({'success': 'qqqqqqqqqqqqqqqq'})
        return response



def payment_confirmation(data):
    OrderReciept.objects.filter(order_key=data).update(billing_status=True)



def email_notify_vendor(orderReciept):
    from_email = settings.DEFAULT_EMAIL_FROM

    for vendor in orderReciept.which_vendor.all():
        to_email = vendor.created_by.email
        subject = "New order"
        text_content = "You have a new order"
        html_content = render_to_string('order/email_notify_vendor.html', {'order_email_vendor':orderReciept, 'vendor_email':vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def email_notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = "Order Confirmation"
    text_content = "Thank you for the order"
    html_content = render_to_string('order/email_notify_customer.html', {'order_email_customer':order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

