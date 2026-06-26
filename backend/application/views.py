<<<<<<< HEAD
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
=======
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
    
    # application/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging
from .models import Order, Payment
from decimal import Decimal
import datetime

logger = logging.getLogger(__name__)

# You'll import your chosen payment gateway's SDK here
# import stripe
# import razorpay

# For Razorpay (example)
# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def checkout_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # This is where you would typically create a payment intent/order with the gateway
        # and get details needed for the frontend.

        # Example for Razorpay (simplified):
        amount_in_paise = int(order.amount * 100) # Razorpay expects amount in smallest currency unit
        data = {
            "amount": amount_in_paise,
            "currency": order.currency,
            "receipt": f"order_rcptid_{order.id}",
            "notes": {
                "order_id": str(order.id),
                "customer_name": request.user.username if request.user.is_authenticated else "Guest",
            }
        }
        try:
            # Create Razorpay Order
            # razorpay_order = razorpay_client.order.create(data=data)
            # order.payment.razorpay_order_id = razorpay_order['id'] # Store gateway's order ID if applicable
            # order.save()

            context = {
                'order': order,
                'amount_in_paise': amount_in_paise,
                # 'razorpay_order_id': razorpay_order['id'], # Pass to template
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'customer_name': request.user.get_full_name() if request.user.is_authenticated else '',
                'customer_email': request.user.email if request.user.is_authenticated else '',
            }
            return render(request, 'application/checkout.html', context)

        except Exception as e:
            logger.error(f"Error creating payment gateway order: {e}")
            # Handle error (e.g., show error message to user)
            return render(request, 'application/checkout.html', {'order': order, 'error': 'Payment initiation failed.'})

    context = {
        'order': order,
    }
    return render(request, 'application/checkout.html', context)


@csrf_exempt # CSRF exemption is needed for webhook endpoints as they come from external sources
def payment_success_webhook(request):
    """
    This view handles webhooks from the payment gateway (e.g., Razorpay, Stripe)
    It's crucial for reliable payment processing as it confirms the payment
    independently of the user's browser.
    """
    if request.method == 'POST':
        payload = json.loads(request.body)
        logger.info(f"Received payment webhook: {payload}")

        # --- IMPORTANT: VERIFY THE WEBHOOK SIGNATURE ---
        # Each payment gateway has a specific way to verify the webhook signature.
        # This is CRITICAL for security to ensure the webhook is from the legitimate source.
        # If verification fails, return 400 or 403.

        # Example for Razorpay:
        # try:
        #     razorpay_client.utility.verify_webhook_signature(
        #         request.body.decode('utf-8'),
        #         request.headers['X-Razorpay-Signature'], # Header name might vary
        #         settings.RAZORPAY_WEBHOOK_SECRET # Your webhook secret from Razorpay dashboard
        #     )
        # except Exception as e:
        #     logger.error(f"Webhook signature verification failed: {e}")
        #     return JsonResponse({'status': 'failure', 'message': 'Signature verification failed'}, status=403)

        # Process the event based on its type
        event_type = payload.get('event')
        if event_type == 'payment.captured' or event_type == 'checkout.session.completed': # Example event names
            # Extract relevant details from the payload
            payment_gateway_id = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('id')
            order_id_from_gateway = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('notes', {}).get('order_id')
            amount = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('amount')
            currency = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('currency')

            try:
                order = Order.objects.get(id=order_id_from_gateway)
                # Create or update the Payment record
                payment, created = Payment.objects.get_or_create(
                    order=order,
                    defaults={
                        'payment_gateway_id': payment_gateway_id,
                        'status': 'success',
                        'amount_paid': Decimal(amount) / 100, # Convert back from smallest unit
                        'currency': currency,
                        'paid_at': datetime.datetime.now(),
                    }
                )
                if not created:
                    payment.status = 'success'
                    payment.amount_paid = Decimal(amount) / 100
                    payment.paid_at = datetime.datetime.now()
                    payment.save()

                order.status = 'complete'
                order.save()
                logger.info(f"Payment successful for Order {order.id}. Payment ID: {payment_gateway_id}")
                return JsonResponse({'status': 'success'})

            except Order.DoesNotExist:
                logger.error(f"Order {order_id_from_gateway} not found for payment {payment_gateway_id}")
                return JsonResponse({'status': 'failure', 'message': 'Order not found'}, status=404)
            except Exception as e:
                logger.error(f"Error processing payment webhook for payment {payment_gateway_id}: {e}")
                return JsonResponse({'status': 'failure', 'message': 'Internal server error'}, status=500)
        # Handle other events like 'payment.failed', 'refund.processed', etc.
        else:
            logger.info(f"Unhandled webhook event type: {event_type}")
            return JsonResponse({'status': 'ignored'})

    return JsonResponse({'status': 'invalid method'}, status=405)


def payment_successful_redirect_view(request):
    """
    This view handles the redirect from the payment gateway after a successful payment
    (for a good user experience, not for critical payment status updates).
    """
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id') # Your internal order ID, or from gateway
    # You might fetch the payment object to display details
    # payment = get_object_or_404(Payment, payment_gateway_id=payment_id)
    # order = payment.order if payment else None

    # IMPORTANT: Do NOT rely solely on this redirect for confirming payment.
    # The webhook is the reliable source of truth.
    return render(request, 'application/payment_successful.html', {
        'payment_id': payment_id,
        'order_id': order_id,
        'message': 'Your payment was successful!'
    })

def payment_failed_redirect_view(request):
    """
    This view handles the redirect from the payment gateway after a failed payment.
    """
    error_code = request.GET.get('code')
    error_description = request.GET.get('description')
    return render(request, 'application/payment_failed.html', {
        'error_code': error_code,
        'error_description': error_description,
        'message': 'Your payment failed. Please try again.'
    })
>>>>>>> e2bf320907d220dd96f146c20bc537caecd30fd4
