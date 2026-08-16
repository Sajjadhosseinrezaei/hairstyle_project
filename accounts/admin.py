from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        "id",
        "username",
        "phone_number",
        "first_name",
        "last_name",
        "role",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "created",
    )

    search_fields = (
        "username",
        "phone_number",
        "first_name",
        "last_name",
    )

    ordering = ("-created",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "اطلاعات اختصاصی",
            {
                "fields": (
                    "phone_number",
                    "role",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "اطلاعات اختصاصی",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):

        if obj.role in ["admin", "hairstyler"]:
            obj.is_staff = True
        else:
            obj.is_staff = False

        super().save_model(
            request,
            obj,
            form,
            change,
        )
