from django.db import models
from accounts.models import User
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    # اسلاگ برای آدرس‌های وب زیبا و SEO (مثال: /services/hair-cut/)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='اسلاگ/آدرس')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name


class Service(models.Model):

    category = models.ForeignKey(
            Category,
            on_delete=models.SET_NULL, # اگر دسته‌بندی پاک شد، خدمت حذف نشود
            null=True,
            blank=True,
            related_name='services',
            verbose_name='دسته‌بندی'
        )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='services',
        verbose_name='آرایشگر/ارائه‌دهنده'
    )
    name = models.CharField(max_length=150, verbose_name='نام خدمت')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        verbose_name='قیمت (تومان)'
    )

    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'

    def __str__(self):
        return f"{self.name} - {self.user.get_full_name() or self.user.username}"


class SlotTime(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='slot_times',
        verbose_name='آرایشگر'
    )
    day = models.DateField(verbose_name='تاریخ')
    start_time = models.TimeField(verbose_name='زمان شروع')
    end_time = models.TimeField(verbose_name='زمان پایان')
    
    is_booked = models.BooleanField(default=False, verbose_name='رزرو شده؟')

    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'زمان نوبت'
        verbose_name_plural = 'زمان‌های نوبت‌دهی'
        # جلوگیری از ساخت اسلات تکراری با زمان شروع و روز یکسان برای یک آرایشگر
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'day', 'start_time'], 
                name='unique_barber_slot'
            )
        ]

    def __str__(self):
        status = "رزرو شده" if self.is_booked else "خالی"
        return f"{self.user.username} | {self.day} ({self.start_time.strftime('%H:%M')} تا {self.end_time.strftime('%H:%M')}) - {status}"