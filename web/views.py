from django.views.generic import ListView
from products.models import Product, Category

class HomePageView(ListView):
    model = Product
    template_name = 'web/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context
