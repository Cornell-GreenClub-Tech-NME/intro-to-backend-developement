from rest_framework import serializers

from .models import User
from .models import Transaction

class UserSerializer(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'date', 'description']
