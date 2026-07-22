from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import  messages
from django.views import View

# Create your views here.

class UserCreationView(View):
    form_class = CustomUserCreationForm
    template_name = "accounts/creation_user.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "کاربر با موفقیت ایجاد شد")
            return redirect("/")

        return render(request, self.template_name, {"form": form})


