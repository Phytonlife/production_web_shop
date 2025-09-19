from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order Confirmation #{order.id}'
    message = f'Dear {order.user.username},\n\nThank you for your order. Your order details are as follows:\n\n'
    for item in order.items.all():
        message += f'- {item.product.name} (x{item.quantity}): {item.price} руб.\n'
    message += f'\nTotal: {order.total_amount} руб.\n\nThank you for shopping with us!'
    send_mail(subject, message, 'from@example.com', [order.user.email])

