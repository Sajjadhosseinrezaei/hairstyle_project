from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, time
from home.models import Service, SlotTime

User = get_user_model()


class Command(BaseCommand):
    help = "ساخت دیتای تست (خدمات و اسلات‌های زمانی) برای آرایشگرهای مشخص"

    def handle(self, *args, **options):
        barber_ids = [1, 2, 4]
        barbers = User.objects.filter(id__in=barber_ids)

        if not barbers.exists():
            self.stdout.write(
                self.style.ERROR("هیچ کاربری با آیدی‌های ۱، ۲ یا ۴ یافت نشد!")
            )
            return

        # لیست خدمات نمادین
        sample_services = [
            {"name": "اصلاح سر و صورت", "price": 250000},
            {"name": "کوتاهی و استایل مو", "price": 180000},
            {"name": "پاکسازی پوست", "price": 350000},
            {"name": "رنگ و کراتین", "price": 600000},
        ]

        # ساعت‌های کاری (مثلاً از ۱۰ صبح تا ۳ بعدازظهر)
        slot_hours = [
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
            (time(12, 0), time(13, 0)),
            (time(14, 0), time(15, 0)),
        ]

        today = timezone.now().date()
        services_created = 0
        slots_created = 0

        for barber in barbers:
            self.stdout.write(f"در حال ایجاد داده برای آرایشگر: {barber.username} (ID: {barber.id})...")

            # ۱. ساخت خدمات برای آرایشگر (اگر از قبل وجود نداشته باشد)
            for s in sample_services[:2]:  # برای هر آرایشگر ۲ خدمت اول ثبت می‌شود
                service, created = Service.objects.get_or_create(
                    user=barber,
                    name=f"{s['name']}",
                    defaults={"price": s["price"]},
                )
                if created:
                    services_created += 1

            # ۲. ساخت اسلات‌های زمانی برای ۳ روز آینده
            for day_offset in range(1, 4):  # فردا، فرداشب و روز بعدش
                slot_day = today + timedelta(days=day_offset)

                for start, end in slot_hours:
                    # استفاده از get_or_create برای جلوگیری از تداخل با UniqueConstraint
                    _, created = SlotTime.objects.get_or_create(
                        user=barber,
                        day=slot_day,
                        start_time=start,
                        defaults={
                            "end_time": end,
                            "is_booked": False
                        }
                    )
                    if created:
                        slots_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"تعداد {services_created} خدمت و {slots_created} اسلات زمانی با موفقیت ایجاد شدند!"
            )
        )