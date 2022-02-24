from rest_framework import serializers

from .models import Wallet, WalletTransaction
from .wallet import create_wallet


class WalletSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = ('id', 'user', 'public_key', 'balance', 'creation_date')
        
class WalletCreationSerializer(serializers.ModelSerializer):
    
    # public_key = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = ('id', 'user', 'public_key', 'balance', 'creation_date')
        
    

class WalletTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WalletTransaction
        fields = ('id', 'sender', 'receiver', 'amount', 'gas')