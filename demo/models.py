from django.conf import settings
from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.TextField()
    username = models.TextField()
    balance = models.FloatField()
    
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return f"{self.sender.name} to {self.receiver.name} - ${self.amount} - {self.date}"
    
    