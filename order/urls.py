from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path(
        "payment/<int:service_id>/<int:slot_id>/",
        views.PaymentView.as_view(),
        name="payment",
    ),
    path(
        "payment/callback/",
        views.PaymentCallbackView.as_view(),
        name="callback",
    ),
    path(
        "payment/success/<int:order_id>/",
        views.PaymentSuccessView.as_view(),
        name="payment_success",
    ),
]
