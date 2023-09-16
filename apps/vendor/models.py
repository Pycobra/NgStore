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
    vendor_image = models.ImageField(verbose_name=_("store image"),
                                   help_text=_("Upload a your image"),
                                   upload_to="images/uploads/profile/",
                                   default="images/site-images/shop.png")
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

