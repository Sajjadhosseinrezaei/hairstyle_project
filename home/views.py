from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Service, Category
from django.views import View
# Create your views here.


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        # دریافت دسته‌بندی‌های اصلی (که والد ندارند)
        categories = Category.objects.all()
        return render(request, self.template_name, {"categories": categories})



class ServicesView(View):
    template_name = 'home/services.html'

    def get(self, request, id):
        # دریافت دسته‌بندی برای نمایش نام آن در هدر صفحه (در صورت عدم وجود ارور 404 می‌دهد)
        category = get_object_or_404(Category, id=id)
        
        # دریافت خدمات مربوط به این دسته‌بندی
        services = Service.objects.filter(category_id=id).select_related('user', 'category')
        
        context = {
            'category': category,
            'services': services,
        }
        return render(request, self.template_name, context)




class ServiceView(View):
    template_name = 'home/service.html'

    def get(self, request, service_id):

        service = get_object_or_404(Service, id=service_id)
        slots = service.user.slot_times.filter(
            is_booked=False
        ).order_by('day', 'start_time')

        context = {"service": service, "slots": slots}
        return render(request, self.template_name, context)