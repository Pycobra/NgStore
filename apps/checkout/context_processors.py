from apps.order.models import Address
from django.conf import settings


def get_address(request):
    session = request.session
    key = session.get(settings.PAYSTACK_SECRET_KEY)
    print(key)
    return {'key':key}


