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
    
