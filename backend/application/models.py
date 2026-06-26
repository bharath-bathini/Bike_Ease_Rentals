<<<<<<< HEAD
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
class BikeInfo(models.Model):
    bike_name = models.CharField(max_length=100)
    bike_model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20, unique=True)
    purchase_date = models.DateField()
    is_active = models.BooleanField(default=True)
    bike_image = models.ImageField(upload_to='bike_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.bike_name} - {self.registration_number}"
    
class Rent(models.Model):
    bike = models.ForeignKey(BikeInfo, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    price_per_day = models.DecimalField(max_digits=10000, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('confirmed', 'Confirmed')], default='Pending')
    def __str__(self):
        return f"Rent: {self.bike.bike_name} by {self.renter.username} from {self.rent_start_date} to {self.rent_end_date}"
    
=======
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
class BikeInfo(models.Model):
    bike_name = models.CharField(max_length=100)
    bike_model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20, unique=True)
    purchase_date = models.DateField()
    is_active = models.BooleanField(default=True)
    bike_image = models.ImageField(upload_to='bike_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.bike_name} - {self.registration_number}"
    
class Rent(models.Model):
    bike = models.ForeignKey(BikeInfo, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    price_per_day = models.DecimalField(max_digits=10000, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('confirmed', 'Confirmed')], default='Pending')
    def __str__(self):
        return f"Rent: {self.bike.bike_name} by {self.renter.username} from {self.rent_start_date} to {self.rent_end_date}"
    
    # application/models.py

from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for custom user models

User = get_user_model() # Dynamically get the currently active user model

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR') # e.g., 'USD', 'EUR'
    status = models.CharField(max_length=20, default='pending') # pending, complete, failed, refunded
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add other order-specific fields like items, quantity, etc.

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'} - {self.status}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_gateway_id = models.CharField(max_length=100, unique=True, null=True, blank=True) # ID from payment gateway
    signature = models.CharField(max_length=255, null=True, blank=True) # For verification, e.g., Razorpay signature
    status = models.CharField(max_length=20, default='pending') # pending, success, failed
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    paid_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
    
>>>>>>> e2bf320907d220dd96f146c20bc537caecd30fd4
