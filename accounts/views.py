from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LoginForm
from django.contrib import  messages
from django.views import View
from django.contrib.auth import login, logout

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


class UserLoginView(View):
    form_class = LoginForm
    template_name = "accounts/login_user.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request, "شما وارد شدید")
            return redirect('home:home')
        else:
            return render(request, self.template_name, {"form": form})



class UserLogoutView(View):

    def post(self, request):
        logout(request)
        messages.success(request, "شما با موفقیت خارج شدید.")
        return redirect("home:home")




