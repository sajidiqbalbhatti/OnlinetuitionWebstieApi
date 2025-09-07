from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .models import Payment
from courses.models import Course
from .serializer import PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


# payments/views# Import Course model



class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()  # ✅ fix
    serializer_class = PaymentSerializer

class CreateCheckoutSession(APIView):
    def post(self, request):
        try:
            # client se course_id lena
            course_id = request.data.get("course_id")
            if not course_id:
                return Response({"error": "course_id is required"}, status=400)

            # course object fetch karo
            course = Course.objects.get(id=course_id)

            # Check karo agar user already payment kar chuka hai ya pending hai
            existing_payment = Payment.objects.filter(
                user=request.user,
                course=course,
                status__in=["pending", "completed"]
            ).first()

            if existing_payment:
                return Response(
                    {"error": "You have already made or have a pending payment for this course."},
                    status=400
                )

            # Stripe checkout session create karo with dynamic price
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': course.title,
                        },
                        'unit_amount': int(course.price * 100),  # price in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url="http://127.0.0.1:8000/api/payments/success/",
                cancel_url="http://127.0.0.1:8000/api/payments/cancel/",
            )

            # Save payment
            Payment.objects.create(
                user=request.user,
                course=course,
                stripe_session_id=checkout_session["id"],
                amount=course.price,
                currency="usd",
                status="pending"
            )

            return Response({"checkout_url": checkout_session.url})
        
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class PaymentSuccess(APIView):
    def get(self, request):
        return Response({"message": "Payment successful!"})


class PaymentCancel(APIView):
    def get(self, request):
        return Response({"message": "Payment canceled!"})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        # Handle event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            print("Payment was successful:", session)

        return HttpResponse(status=200)
