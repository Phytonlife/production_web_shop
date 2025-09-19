from django.views.generic import ListView
from products.models import Product

class HomePageView(ListView):
    model = Product
    template_name = 'web/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)[:6] # Показываем 6 последних товаров