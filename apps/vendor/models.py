#from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.account.models import UserBase
import datetime
import secrets



class Vendor(models.Model):
    store_name = models.CharField(max_length=255, unique=True)
    unique_id =  models.CharField(max_length=50, unique=True)
    """vendor_image = models.ImageField(verbose_name=_("profile image"),
                                   help_text=_("Upload a your image"),
                                   upload_to="images/uploads/profile/",
                                   default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")"""
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='which_vendor', on_delete=models.CASCADE)# video used vendor

    class Meta:
        verbose_name_plural = 'List of Vendors'
        ordering=['store_name']

    def save(self, *args, **kwargs) -> None:
        while not self.unique_id:
            unique_id = secrets.token_urlsafe(33)
            object_with_similar_order_key = Vendor.objects.filter(unique_id=unique_id).exists()
            if not object_with_similar_order_key:
                self.unique_id = unique_id
        super().save(*args, **kwargs)

    #dunder
    #to make this the models name at admin area || and how to reference this model

    def __str__(self):
        return self.store_name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.price * item.quantity) for item in items)
        verbose_name_plural = 'List of Vendors'

class Follow(models.Model):
    follower = models.ForeignKey(UserBase, related_name='user_following', on_delete=models.CASCADE, null=True)
    following = models.ForeignKey(Vendor, related_name='vendor_follower', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Followers'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.follower} is following {self.following}"

    def get_date(self):
        time = datetime.datetime.now()
        if self.created_at.day == time.day:
            if self.created_at.hour == time.hour:
                return str(time.min - self.created_at.min) + " mins ago"
            else:
                return str(time.hour - self.created_at.hour) + " hours ago"
        else:
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " days ago"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " months ago"
                else:
                    return str() + str(self.created_at.day) + "/" +str(self.created_at.month) + "/" +str(self.created_at.year)
        return self.created_at



class VendorImages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='which_user', on_delete=models.CASCADE, null=True)
    images = models.ImageField(verbose_name=_("image"),help_text=_("Upload a product image"),
                               upload_to="images/uploads/store/", default="images/site-images/shop.png")
    alt_text = models.CharField(verbose_name=_("Alternative text"),
                             help_text=_("Please add alternative text"),max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name =_("Vendor Image")
        verbose_name_plural = _("Vendor Images")

    def __str__(self):
        return self.alt_text

class VendorImageValue(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_image')
    image_value = models.ForeignKey(VendorImages, on_delete=models.RESTRICT)
    #created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    #updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name =_("Image Value")
        verbose_name_plural = _("Images Values")
    def __str__(self):
        return self.vendor.store_name

class SubscriptionType(models.Model):
    DURATION_CHOICES = [
        ("A", "30days"),
        ("B", "90days"),
        ("C", "1year"),
    ]
    PLAN_CHOICES = [
        ("A", "PLATINUM"),
        ("B", "GOLD"),
        ("C", "SILVER"),
    ]

    vendor = models.ForeignKey(Vendor, related_name='vendor_subscription_type', on_delete=models.CASCADE)
    duration = models.CharField(choices=DURATION_CHOICES, max_length=255)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    title = models.CharField(choices=PLAN_CHOICES, max_length=255)

    def __str__(self):
        return self.title

class Subscriptions(models.Model):
    suscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='suscribee', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='vendor_suscribed', on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionType, on_delete=models.RESTRICT, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Subscriptions'
        verbose_name = 'Subscription'
        ordering=['-created_at']

    def __str__(self):
        return self.suscriber.user_name


