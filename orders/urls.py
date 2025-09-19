from django.urls import path
from .views import add_to_cart, checkout, payment, webhook, payment_success, payment_failed

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/<int:order_id>/', payment, name='payment'),
    path('webhook/', webhook, name='webhook'),
    path('payment-success/<int:order_id>/', payment_success, name='payment_success'),
    path('payment-failed/<int:order_id>/', payment_failed, name='payment_failed'),
]
