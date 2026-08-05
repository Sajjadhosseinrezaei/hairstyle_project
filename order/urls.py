from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path(
        "payment/<int:service_id>/<int:slot_id>/",
        views.PaymentView.as_view(),
        name="payment",
    ),
]