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
        "created",
        "updated",
    )

    ordering = (
        "-created",
    )