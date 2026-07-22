from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):

    # فیلد یوزرنیم از abstractuser ارث بری شده است نیاز نیست دوباره بنویسیم
    ROLE = (
        ("admin", "ادمین"),
        ("hairstyler","آرایشگر"),
        ("user", "کاربر"),
    )
    
    first_name = models.CharField(max_length=255, default='fristname')
    last_name = models.CharField(max_length=255, default='lastname')
    phone_number = models.CharField(max_length=11, unique=True)
    role = models.CharField(choices=ROLE, max_length=10, default="user")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        # متد get role display فیلد رول را به صورت فارسی نشان میدهد
        return f"{self.username} - {self.get_role_display()}"

