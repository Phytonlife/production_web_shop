from django.conf import settings
from django.db import models
from products.models import Product

class Cart(models.Model):
    """Модель корзины"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    """Модель элемента корзины"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Гарантирует, что один и тот же товар не будет добавлен в корзину дважды
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

class Order(models.Model):
    """Модель заказа"""
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'В ожидании'
        PAID = 'paid', 'Оплачен'
        COMPLETED = 'completed', 'Выполнен'
        CANCELED = 'canceled', 'Отменен'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Anonymous'}"

class OrderItem(models.Model):
    """Модель элемента заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    # Сохраняем цену на момент покупки
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"