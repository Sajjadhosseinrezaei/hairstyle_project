from django.contrib import admin
from .models import Service, SlotTime, Category



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "user",
        "category",
        "price",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.role == "hairstyler":
            qs = qs.filter(
                user=request.user
            )

        return qs

    def get_exclude(self, request, obj=None):

        if request.user.role == "hairstyler":
            return ["user"]

        return []

    def save_model(self, request, obj, form, change):

        if request.user.role == "hairstyler":
            obj.user = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )


@admin.register(SlotTime)
class SlotTimeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "day",
        "start_time",
        "end_time",
        "is_booked",
    )

    list_filter = (
        "is_booked",
        "day",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    ordering = (
        "day",
        "start_time",
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        # آرایشگر فقط Slot های خودش را ببیند
        if request.user.role == "hairstyler":
            qs = qs.filter(
                user=request.user
            )

        return qs

    def get_exclude(self, request, obj=None):

        if request.user.role == "hairstyler":
            return ["user"]

        return []

    def save_model(self, request, obj, form, change):

        if request.user.role == "hairstyler":
            obj.user = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )
