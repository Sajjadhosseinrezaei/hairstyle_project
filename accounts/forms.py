from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ۱. اعمال کلاس‌های بوت‌استرپ
        for field_name, field in self.fields.items():
            if field_name == 'role':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        # ۲. فارسی کردن نام (Label) فیلدهای پسورد
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'

        # ۳. فارسی کردن متن‌های راهنمای رمز عبور
        self.fields['password1'].help_text = (
            '<ul class="text-muted ps-3 small mb-0">'
            '<li>رمز عبور نباید خیلی شبیه به اطلاعات شخصی شما باشد.</li>'
            '<li>رمز عبور باید حداقل شامل ۸ کاراکتر باشد.</li>'
            '<li>از رمزهای عبور خیلی رایج و ساده استفاده نکنید.</li>'
            '<li>رمز عبور نباید فقط شامل اعداد باشد.</li>'
            '</ul>'
        )
        
        # ۴. فارسی کردن راهنمای تکرار رمز عبور
        self.fields['password2'].help_text = 'برای اطمینان، همان رمز عبور بالا را مجدداً وارد کنید.'
        self.fields['username'].help_text = "الزامی است. حداکثر ۱۵۰ کاراکتر. فقط حروف انگلیسی، اعداد و کاراکترهای @، .، +، - و _ مجاز هستند."

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phone_number')
        
        labels = {
            'username': _('نام کاربری'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'phone_number': _('شماره موبایل'),
            'role': _('نقش کاربری'),
        }


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        
        # ۱. فارسی کردن لیبل فیلدها
        self.fields['username'].label = _('نام کاربری')
        self.fields['password'].label = _('رمز عبور')
        
        # ۲. اعمال کلاس‌های بوت‌استرپ برای ظاهر زیبا
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # ۳. فارسی کردن پیام‌های خطا (مانند اشتباه بودن نام کاربری یا رمز عبور)
    error_messages = {
        'invalid_login': _(
            'لطفاً %(username)s و رمز عبور صحیح را وارد کنید. توجه داشته باشید که هر دو فیلد ممکن است به بزرگ و کوچک بودن حروف حساس باشند.'
        ),
        'inactive': _('این حساب کاربری غیرفعال است.'),
    }
