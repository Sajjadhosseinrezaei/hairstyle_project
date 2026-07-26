from django.db import models
from accounts.models import User
from home.models import Service, SlotTime

class Order(models.Model):

    # تعریف کلاس وضعیت‌ها با TextChoices
    class StatusChoices(models.TextChoices):
        PENDING = 'unpaid', 'پرداخت نشده'
        PAID = 'paid', 'پرداخت شده'
        CANCELED = 'canceled', 'لغو شده'

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders', 
        verbose_name='مشتری'
    )
    
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="وضعیت سفارش"
    )
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'

    def __str__(self):
        # get_status_display() مقدار فارسی وضعیت را برمی‌گرداند
        return f"سفارش شماره {self.id} - {self.user.username} ({self.get_status_display()})"

    def get_total_price(self):
        return sum(item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name='سفارش'
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        verbose_name='خدمت'
    )
    # OneToOneField جلوی رزرو همزمان یک اسلات توسط دو نفر را می‌گیرد
    slot_time = models.OneToOneField(
        SlotTime, 
        on_delete=models.CASCADE, 
        verbose_name='اسلات زمانی'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        verbose_name='قیمت (تومان)'
    )

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f"{self.service.name} در {self.slot_time.day} ({self.slot_time.start_time.strftime('%H:%M')})"