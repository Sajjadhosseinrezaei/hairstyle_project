from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import SlotTime, Service


class PaymentView(LoginRequiredMixin, View):
    template_name = "order/payment.html"

    def get(self, request, service_id, slot_id):

        service = get_object_or_404(Service, id=service_id)

        slot = get_object_or_404(
            SlotTime,
            id=slot_id,
            user=service.user,
            is_booked=False
        )

        context = {
            "service": service,
            "slot": slot,
            "amount": service.price,
        }

        return render(request, self.template_name, context)