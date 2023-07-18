from django.db import models
from datetime import datetime
from django.utils import timezone

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    Contact_date = models.DateTimeField(default=timezone.now(), blank=True)

    def __str__(self) -> str:
        return self.email