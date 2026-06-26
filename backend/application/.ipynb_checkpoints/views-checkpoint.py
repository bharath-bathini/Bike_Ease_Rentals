from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import*
from .serializers import*
from rest_framework import generics, permissions
from rest_framework.views import APIView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff, 
            "is_superuser": user.is_superuser, 
        }
        return data
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    print("Incoming data:", request.data)

    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name', '')

    if not username or not password or not email:
        return Response({'message': 'Username, password, and email are required.'})

    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists'})

    try:
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name)
        user.save()
        return Response({'message': 'User registered successfully'}, status=201)
    except Exception as e:
        print("Error during user creation:", e)
        return Response({'message': 'Registration failed', 'error': str(e)}, status=500)
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import BikeInfo
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import status


@require_GET
def list_bikes(request):
    # Get all bikes associated with the logged-in user
    bikes = BikeInfo.objects.all()
    bike_data = []

    for bike in bikes:
        bike_data.append({
            'id': bike.id,
            'bike_name': bike.bike_name,
            'bike_model': bike.bike_model,
            'registration_number': bike.registration_number,
            'purchase_date': bike.purchase_date,
            'is_active': bike.is_active,
            'bike_image': bike.bike_image.url if bike.bike_image else None
        })

    return JsonResponse(bike_data, safe=False)
from .models import*
def add_bike(request):
    if request.method == 'POST':
        # Handle file upload using request.FILES
        bike_name = request.POST.get('bike_name')
        bike_model = request.POST.get('bike_model')
        registration_number = request.POST.get('registration_number')
        purchase_date = request.POST.get('purchase_date')
        is_active = request.POST.get('is_active') == 'true'
        bike_image = request.FILES.get('bike_image')
        bike = BikeInfo.objects.create(  # Assuming you want to associate the bike with the logged-in user
            bike_name=bike_name,
            bike_model=bike_model,
            registration_number=registration_number,
            purchase_date=purchase_date,
            is_active=is_active,
            bike_image=bike_image,  # Storing the uploaded file
        )
        bike.save()
        return JsonResponse({"message": "Bike added successfully!"}, status=200)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import*
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def book_bike(request):
    bike_id = request.data.get('bike')
    rent_start_date = request.data.get('rent_start_date')
    rent_end_date = request.data.get('rent_end_date')
    print("Booking data:", bike_id, rent_start_date, rent_end_date)
    if not bike_id or not rent_start_date or not rent_end_date:
        return Response({'error': 'bike_id, rent_start_date, and rent_end_date are required.'})

    try:
        bike = BikeInfo.objects.get(id=bike_id)
    except BikeInfo.DoesNotExist:
        return Response({'error': 'Bike not found'})

    rent_detail = Rent.objects.create(
        renter=request.user,
        bike=bike,
        rent_start_date=rent_start_date,
        rent_end_date=rent_end_date
    )
    rent_detail.save()

    return Response({'message': 'Bike booked successfully!'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bike_detail(request, bike_id):
    try:
        bike = BikeInfo.objects.get(id=bike_id)
    except BikeInfo.DoesNotExist:
        return Response({'error': 'Bike not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'bike_name': bike.bike_name,
        'bike_type': bike.bike_type,
        'price_per_day': bike.price_per_day,
        'description': bike.description
    })
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_rents(request):
    rents = Rent.objects.filter(renter=request.user)
    rent_data = []
    print(rents)
    for rent in rents:
        rent_data.append({
            'id': rent.id,
            'bike_name': rent.bike.bike_name,
            'rent_start_date': rent.rent_start_date,
            'rent_end_date': rent.rent_end_date,
            'price_per_day': rent.bike.price_per_day,
            'total_price': (rent.rent_end_date - rent.rent_start_date).days * rent.bike.price_per_day
        })

    return Response(rent_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_or_reject_rent(request):
    rent_id = request.data.get('rent_id')
    action = request.data.get('action')  # 'confirm' or 'reject'

    if not rent_id or action not in ['confirm', 'reject']:
        return Response({'error': 'rent_id and valid action (confirm/reject) are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rent = Rent.objects.get(id=rent_id)
    except Rent.DoesNotExist:
        return Response({'error': 'Rent not found'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'confirm':
        rent.status = 'confirmed'  # Assuming you have a status field in the Rent model
        rent.save()
        return Response({'message': 'Rent confirmed successfully!'}, status=status.HTTP_200_OK)
    elif action == 'reject':
        rent.status = 'rejected'  # Assuming you have a status field in the Rent model
        rent.save()
        return Response({'message': 'Rent rejected successfully!'}, status=status.HTTP_200_OK)