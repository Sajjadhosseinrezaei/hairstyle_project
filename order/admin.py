from datetime import datetime

from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.urls import path

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "admin/order/order/change_list.html"

    list_display = (
        "id",
        "user",
        "service",
        "slot_time",
        "price",
        "status",
        "authority",
        "ref_id",
        "created",
    )

    list_filter = (
        "status",
        "created",
    )

    search_fields = (
        "user__username",
        "user__email",
        "service__name",
        "authority",
        "ref_id",
    )

    readonly_fields = (
        "user",
        "service",
        "slot_time",
        "price",
        "status",
        "authority",
        "ref_id",
        "created",
        "updated",
    )

    ordering = (
        "-created",
    )

    # ==================================================
    # فقط سفارش‌های مربوط به آرایشگر
    # ==================================================

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.role == "hairstyler":
            qs = qs.filter(
                service__user=request.user
            )

        return qs

    # ==================================================
    # آرایشگر نمی‌تواند سفارش جدید بسازد
    # ==================================================

    def has_add_permission(self, request):

        if request.user.role == "hairstyler":
            return False

        return super().has_add_permission(request)

    # ==================================================
    # آرایشگر نمی‌تواند سفارش حذف کند
    # ==================================================

    def has_delete_permission(self, request, obj=None):

        if request.user.role == "hairstyler":
            return False

        return super().has_delete_permission(
            request,
            obj,
        )

    # ==================================================
    # URL گزارش
    # ==================================================

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "reports/",
                self.admin_site.admin_view(
                    self.order_report_view
                ),
                name="order_report",
            ),
        ]

        return custom_urls + urls

    # ==================================================
    # گزارش سفارش‌ها
    # ==================================================

    def order_report_view(self, request):

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        orders = Order.objects.none()
        report = None

        # Query اولیه
        queryset = Order.objects.select_related(
            "user",
            "service",
            "slot_time",
        )

        # آرایشگر فقط گزارش سفارش‌های خودش را ببیند
        if request.user.role == "hairstyler":
            queryset = queryset.filter(
                service__user=request.user
            )

        # اگر تاریخ‌ها انتخاب شده باشند
        if start_date and end_date:

            try:

                start = datetime.strptime(
                    start_date,
                    "%Y-%m-%d",
                ).date()

                end = datetime.strptime(
                    end_date,
                    "%Y-%m-%d",
                ).date()

                # جلوگیری از وارد کردن بازه اشتباه
                if start <= end:

                    orders = (
                        queryset
                        .filter(
                            created__date__gte=start,
                            created__date__lte=end,
                        )
                        .order_by("-created")
                    )

                    # گزارش کلی
                    report = orders.aggregate(

                        # تعداد کل سفارش‌ها
                        total_orders=Count("id"),

                        # سفارش‌های پرداخت شده
                        total_paid=Count(
                            "id",
                            filter=Q(
                                status=Order.StatusChoices.PAID
                            ),
                        ),

                        # سفارش‌های پرداخت نشده
                        total_unpaid=Count(
                            "id",
                            filter=Q(
                                status=Order.StatusChoices.PENDING
                            ),
                        ),

                        # سفارش‌های لغو شده
                        total_canceled=Count(
                            "id",
                            filter=Q(
                                status=Order.StatusChoices.CANCELED
                            ),
                        ),

                        # مجموع مبلغ سفارش‌ها
                        total_price=Sum("price"),

                    )

            except ValueError:

                orders = Order.objects.none()
                report = None

        context = {
            **self.admin_site.each_context(request),

            "title": "گزارش سفارش‌ها",

            "orders": orders,

            "report": report,

            "start_date": start_date,

            "end_date": end_date,
        }

        return render(
            request,
            "admin/order/order_report.html",
            context,
        )
