from django.db import models
from accounts.models import User
from home.models import Service, SlotTime


class Order(models.Model):

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

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name='خدمت'
    )

    slot_time = models.OneToOneField(
        SlotTime,
        on_delete=models.PROTECT,
        verbose_name='اسلات زمانی'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name='قیمت'
    )

    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    authority = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    ref_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)