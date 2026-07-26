from django.shortcuts import render
from django.http import HttpResponse
from .models import Service
from django.views import View
# Create your views here.


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        # استفاده از select_related برای لود همزمان اطلاعات آرایشگر
        services = Service.objects.select_related('user').all()
        return render(request, self.template_name, {"services": services})