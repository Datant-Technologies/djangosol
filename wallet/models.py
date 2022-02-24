import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()
# now = datetime.datetime.now()

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    public_key = models.CharField(max_length=200, unique=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    creation_date = models.DateTimeField(default=now)
    
    

class WalletTransaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    gas = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    