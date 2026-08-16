from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

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

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        # آرایشگر فقط رزروهای مربوط به خودش را ببیند
        if request.user.role == "hairstyler":
            qs = qs.filter(
                service__user=request.user
            )

        return qs

    def has_add_permission(self, request):

        # آرایشگر نمی‌تواند از پنل Admin رزرو ایجاد کند
        if request.user.role == "hairstyler":
            return False

        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):

        # آرایشگر نمی‌تواند رزرو را حذف کند
        if request.user.role == "hairstyler":
            return False

        return super().has_delete_permission(
            request,
            obj,
        )