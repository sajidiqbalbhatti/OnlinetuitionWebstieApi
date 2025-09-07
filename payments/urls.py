from django.urls import path
from .views import CreateCheckoutSession, PaymentSuccess, PaymentCancel, StripeWebhookView,PaymentListView

urlpatterns = [
    path('list/',PaymentListView.as_view()),
    path("create-checkout-session/", CreateCheckoutSession.as_view(), name="create-checkout-session"),
    path("success/", PaymentSuccess.as_view(), name="payment-success"),
    path("cancel/", PaymentCancel.as_view(), name="payment-cancel"),
    path("webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
]
