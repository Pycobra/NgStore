from django.db import models
from django.conf import settings

import datetime
import uuid

from apps.vendor.models import Vendor
from apps.account.models import UserBase


class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    #vendor = models.ForeignKey(Vendor, related_name='vendors_msg', on_delete=models.CASCADE)
    sender_id_unique = models.CharField(null=True, max_length=50)
    reciever_id_unique =  models.CharField(max_length=50)
    content =  models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering=['-created_at']

    def __str__(self):
        return f'from {self.sender_id_unique} to {self.reciever_id_unique}'

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

    #do this later
    def get_time(self):
        time = datetime.datetime.now()
        if self.created_at.hour == time.hour:
            return str(time.min - self.created_at.min) + " mins ago"
        else:
            if self.created_at.day == time.day:
                return str(time.hour - self.created_at.hour) + " hours ago"
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " days ago"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " months ago"
                else:
                    return str() + str(self.created_at.day) + "/" +str(self.created_at.month) + "/" +str(self.created_at.year)
        return self.created_at