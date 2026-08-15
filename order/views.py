import requests

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from home.models import Service, SlotTime
from .models import Order


ZARINPAL_REQUEST_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
)

ZARINPAL_VERIFY_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
)

ZARINPAL_STARTPAY_URL = (
    "https://sandbox.zarinpal.com/pg/StartPay/"
)


# =========================================================
# Payment View
# =========================================================

class PaymentView(LoginRequiredMixin, View):

    template_name = "order/payment.html"

    def get(self, request, service_id, slot_id):

        service = get_object_or_404(
            Service,
            id=service_id,
        )

        slot = get_object_or_404(
            SlotTime,
            id=slot_id,
            user=service.user,
            is_booked=False,
        )

        context = {
            "service": service,
            "slot": slot,
            "amount": service.price,
        }

        return render(
            request,
            self.template_name,
            context,
        )

    def post(self, request, service_id, slot_id):

        service = get_object_or_404(
            Service,
            id=service_id,
        )

        slot = get_object_or_404(
            SlotTime,
            id=slot_id,
            user=service.user,
            is_booked=False,
        )

        # =================================================
        # پیدا کردن سفارش قبلی
        # =================================================

        order = Order.objects.filter(
            slot_time=slot,
            user=request.user,
            status=Order.StatusChoices.PENDING,
        ).first()

        # =================================================
        # اگر سفارش قبلی وجود نداشت، ایجاد کن
        # =================================================

        if not order:

            try:

                with transaction.atomic():

                    order = Order.objects.create(
                        user=request.user,
                        service=service,
                        slot_time=slot,
                        price=service.price,
                        status=Order.StatusChoices.PENDING,
                    )

            except Exception as e:

                print("ORDER CREATE ERROR:", e)

                return render(
                    request,
                    "order/payment_failed.html",
                    {
                        "message": "خطا در ایجاد سفارش."
                    },
                )

        # =================================================
        # Callback URL
        # =================================================

        callback_url = request.build_absolute_uri(
            reverse("order:callback")
        )

        # =================================================
        # اطلاعات درخواست زرین پال
        # =================================================

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,

            # قیمت مدل به تومان است
            # زرین پال مبلغ را ریال می‌خواهد
            "amount": int(order.price) * 10,

            "callback_url": callback_url,

            "description": (
                f"پرداخت سفارش شماره {order.id}"
            ),

            "metadata": {
                "email": request.user.email,
            },
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        # =================================================
        # ارسال درخواست به زرین پال
        # =================================================

        try:

            response = requests.post(
                ZARINPAL_REQUEST_URL,
                json=data,
                headers=headers,
                timeout=15,
            )

            result = response.json()

            print("========== ZARINPAL REQUEST ==========")
            print("Response:", result)

        except requests.RequestException as e:

            print("ZARINPAL REQUEST ERROR:", e)

            return render(
                request,
                "order/payment_failed.html",
                {
                    "message": (
                        "ارتباط با درگاه پرداخت برقرار نشد."
                    )
                },
            )

        # =================================================
        # بررسی پاسخ زرین پال
        # =================================================

        code = result.get(
            "data",
            {}
        ).get(
            "code"
        )

        if (
            response.status_code == 200
            and code == 100
        ):

            authority = result["data"]["authority"]

            # ذخیره Authority
            order.authority = authority

            order.save(
                update_fields=[
                    "authority"
                ]
            )

            print("ORDER ID:", order.id)
            print("AUTHORITY:", authority)

            # =================================================
            # انتقال به درگاه
            # =================================================

            payment_url = (
                ZARINPAL_STARTPAY_URL
                + authority
            )

            return redirect(payment_url)

        # =================================================
        # ایجاد پرداخت ناموفق
        # =================================================

        print("PAYMENT REQUEST FAILED")
        print("CODE:", code)

        order.status = Order.StatusChoices.CANCELED

        order.save(
            update_fields=[
                "status"
            ]
        )

        return render(
            request,
            "order/payment_failed.html",
            {
                "message": (
                    "خطا در ایجاد درخواست پرداخت."
                )
            },
        )


# =========================================================
# Payment Callback
# =========================================================

class PaymentCallbackView(LoginRequiredMixin, View):

    def get(self, request):

        print()
        print("========================================")
        print("       ZARINPAL CALLBACK")
        print("========================================")

        # =================================================
        # دریافت اطلاعات از زرین پال
        # =================================================

        authority = request.GET.get(
            "Authority"
        )

        status = request.GET.get(
            "Status"
        )

        print("Authority:", authority)
        print("Status:", status)

        # =================================================
        # بررسی Authority
        # =================================================

        if not authority:

            return render(
                request,
                "order/payment_failed.html",
                {
                    "message": (
                        "اطلاعات پرداخت دریافت نشد."
                    )
                },
            )

        # =================================================
        # پیدا کردن Order
        # =================================================

        try:

            order = Order.objects.get(
                authority=authority,
                user=request.user,
            )

        except Order.DoesNotExist:

            return render(
                request,
                "order/payment_failed.html",
                {
                    "message": (
                        "سفارش مربوط به این پرداخت پیدا نشد."
                    )
                },
            )

        print("Order ID:", order.id)
        print("Order Status:", order.status)
        print("Order Price:", order.price)

        # =================================================
        # اگر قبلاً پرداخت شده
        # =================================================

        if order.status == Order.StatusChoices.PAID:

            return redirect(
                "order:payment_success",
                order_id=order.id,
            )

        # =================================================
        # اگر پرداخت توسط کاربر لغو شده
        # =================================================

        # اگر قبلاً پرداخت شده
        if order.status == Order.StatusChoices.PAID:

            return redirect(
                "order:payment_success",
                order_id=order.id,
            )

        # حتی اگر Status=NOK باشد،
        # فعلاً پرداخت را شکست‌خورده اعلام نکن.

        # =================================================
        # VERIFY
        # =================================================

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,

            # تومان -> ریال
            "amount": int(order.price) * 10,

            "authority": authority,
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        print()
        print("========================================")
        print("       ZARINPAL VERIFY")
        print("========================================")

        print("Verify data:", data)

        try:

            response = requests.post(
                ZARINPAL_VERIFY_URL,
                json=data,
                headers=headers,
                timeout=15,
            )

            result = response.json()

        except requests.RequestException as e:

            print("VERIFY ERROR:", e)

            return render(
                request,
                "order/payment_failed.html",
                {
                    "message": (
                        "ارتباط با زرین پال برقرار نشد."
                    )
                },
            )

        print("Verify HTTP status:", response.status_code)
        print("Verify response:", result)

        # =================================================
        # دریافت کد Verify
        # =================================================

        code = result.get(
            "data",
            {}
        ).get(
            "code"
        )

        print("VERIFY CODE:", code)

        # =================================================
        # پرداخت موفق
        # =================================================

        if code in [100, 101]:

            ref_id = result.get(
                "data",
                {}
            ).get(
                "ref_id"
            )

            print("REF ID:", ref_id)

            # =================================================
            # تراکنش اتمیک
            # =================================================

            with transaction.atomic():

                # قفل کردن Order
                order = (
                    Order.objects
                    .select_for_update()
                    .select_related("slot_time")
                    .get(
                        id=order.id
                    )
                )

                # اگر قبلاً پرداخت شده
                if order.status == Order.StatusChoices.PAID:

                    return redirect(
                        "order:payment_success",
                        order_id=order.id,
                    )

                # گرفتن Slot
                slot = order.slot_time

                # =================================================
                # بررسی رزرو بودن Slot
                # =================================================

                if slot.is_booked:

                    order.status = (
                        Order.StatusChoices.CANCELED
                    )

                    order.save(
                        update_fields=[
                            "status"
                        ]
                    )

                    return render(
                        request,
                        "order/payment_failed.html",
                        {
                            "message": (
                                "این زمان قبلاً رزرو شده است."
                            )
                        },
                    )

                # =================================================
                # تغییر وضعیت Order
                # =================================================

                order.status = (
                    Order.StatusChoices.PAID
                )

                order.ref_id = ref_id

                order.save(
                    update_fields=[
                        "status",
                        "ref_id",
                    ]
                )

                # =================================================
                # رزرو Slot
                # =================================================

                slot.is_booked = True

                slot.save(
                    update_fields=[
                        "is_booked"
                    ]
                )

            print()
            print("========================================")
            print("       PAYMENT SUCCESS")
            print("========================================")

            print("Order:", order.id)
            print("Ref ID:", ref_id)

            # =================================================
            # صفحه موفقیت
            # =================================================

            return redirect(
                "order:payment_success",
                order_id=order.id,
            )

        # =================================================
        # Verify ناموفق
        # =================================================

        print()
        print("========================================")
        print("       PAYMENT VERIFY FAILED")
        print("========================================")

        print("VERIFY CODE:", code)

        order.status = (
            Order.StatusChoices.CANCELED
        )

        order.save(
            update_fields=[
                "status"
            ]
        )

        return render(
            request,
            "order/payment_failed.html",
            {
                "message": (
                    "پرداخت توسط زرین پال تأیید نشد."
                )
            },
        )


# =========================================================
# Payment Success
# =========================================================

class PaymentSuccessView(LoginRequiredMixin, View):

    template_name = "order/payment_success.html"

    def get(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
            status=Order.StatusChoices.PAID,
        )

        return render(
            request,
            self.template_name,
            {
                "order": order,
            },
        )