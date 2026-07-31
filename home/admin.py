from django.contrib import admin
from .models import Service, SlotTime, Category



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    search_fields = ('name', 'slug')
    # تولید خودکار اسلاگ بر اساس نام دسته‌بندی موقع تایپ در ادمین
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست خدمات نشان داده می‌شوند
    list_display = ('name', 'user', 'price_formatted', 'created')
    
    # امکان جستجو بر اساس نام خدمت، نام و نام کاربری آرایشگر
    search_fields = ('name', 'user__username', 'user__first_name', 'user__last_name')
    
    # فیلتر برای جداسازی خدمات براساس آرایشگر
    list_filter = ('user', 'created')
    
    # مرتب‌سازی بر اساس تازه‌ترین خدمات
    ordering = ('-created',)

    # متد برای نمایش سه رقم سه رقم قیمت در پنل ادمین
    @admin.display(description='قیمت (تومان)')
    def price_formatted(self, obj):
        return f"{obj.price:,.0f}"


@admin.register(SlotTime)
class SlotTimeAdmin(admin.ModelAdmin):
    # ستون‌های اصلی جدول زمان‌ها
    list_display = ('user', 'day', 'start_time', 'end_time', 'is_booked', 'created')
    
    # فیلترهای کاربردی (فیلتر بر اساس رزرو شده/خالی، آرایشگر و تاریخ)
    list_filter = ('is_booked', 'user', 'day')
    
    # قابلیت جستجو
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'day')
    
    # ویرایش سریع وضعیت «رزرو شده» مستقیماً از داخل لیست
    list_editable = ('is_booked',)
    
    # مرتب‌سازی بر اساس نزدیک‌ترین تاریخ و زمان
    ordering = ('-day', 'start_time')
    
    # فیلتر تاریخ به صورت نوار بازشونده بالای صفحه
    date_hierarchy = 'day'