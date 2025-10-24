from django.contrib import admin

# Register your models here.
from .models import BikeInfo, Rent
admin.site.register(BikeInfo)
admin.site.register(Rent)
