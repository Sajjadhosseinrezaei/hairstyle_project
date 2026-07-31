from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # ستون‌هایی که در جدول لیست کاربران نشان داده می‌شوند
    list_display = ('id','username', 'phone_number', 'first_name', 'last_name', 'role', 'is_staff')
    
    # فیلترهای سمت راست پنل ادمین
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'created')
    
    # قابلیت جستجو بر اساس نام کاربری، شماره تلفن و نام و نام خانوادگی
    search_fields = ('username', 'phone_number', 'first_name', 'last_name')
    
    # مرتب‌سازی بر اساس جدیدترین کاربران ثبت‌نام‌شده
    ordering = ('-created',)

    # فیلدست‌ها (Fieldsets): نحوه نمایش فیلدها در صفحه ویرایش یک کاربر
    fieldsets = BaseUserAdmin.fieldsets + (
        ('اطلاعات اختصاصی', {
            'fields': ('phone_number', 'role')
        }),
    )

    # فیلدها هنگام ساخت کاربر جدید از طریق پنل ادمین
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('اطلاعات اختصاصی', {
            'fields': ('first_name', 'last_name', 'phone_number', 'role'),
        }),
    )