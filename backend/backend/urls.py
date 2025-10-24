"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# main url routes developments 
from application.views import CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter
from application.views import*
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from django.conf import settings
from django.conf.urls.static import static
from application.views import*
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',CustomTokenObtainPairView.as_view(),name='get_token'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    #main path developments 
    path('api/signup/',register,name='register'),
    path('api/bikes/', list_bikes, name='list_bikes'),
    path('api/bikes/add/', add_bike, name='add_bike'),
    path('api/rents/', book_bike, name='book-bike'),
    path('api/bikes/<int:bike_id>/',bike_detail, name='bike-detail'),
    path('api/my-rents/',my_rents, name='rent-detail'),
    path('confirm_or_reject_rent', confirm_or_reject_rent, name='confirm_or_reject_rent'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
