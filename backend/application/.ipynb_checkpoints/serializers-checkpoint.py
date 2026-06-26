from rest_framework import serializers
from django.contrib.auth.models import User
from .models import*


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        class RentSerializer(serializers.ModelSerializer):
            class Meta:
                model = Rent
                fields = ['id', 'property_name', 'rent_amount', 'start_date', 'end_date']
                
class RentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rent
        fields = ['id', 'property_name', 'rent_amount', 'start_date', 'end_date', 'user']
