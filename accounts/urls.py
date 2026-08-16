from django.urls import path
from . import  views

app_name = 'accounts'

urlpatterns = [
    path(
        "register/",
        views.RegisterChoiceView.as_view(),
        name="register_choice",
    ),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name='logout'),
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "register/user/",
        views.UserCreationView.as_view(),
        name="register",
    ),

    path(
        "register/hairstyler/",
        views.HairstylerRegisterView.as_view(),
        name="hairstyler_register",
    ),

    path(
        "register/hairstyler/success/",
        views.HairstylerRegisterSuccessView.as_view(),
        name="hairstyler_register_success",
    ),
]
