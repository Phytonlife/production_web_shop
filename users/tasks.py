from celery import shared_task
from django.core.mail import send_mail
from .models import User

@shared_task
def send_welcome_email(user_id):
    """Задача для отправки приветственного письма новому пользователю."""
    try:
        user = User.objects.get(id=user_id)
        # В реальном проекте здесь будет красивый HTML-шаблон
        send_mail(
            'Добро пожаловать в E-comm Service!',
            f'Здравствуйте, {user.username}! Спасибо за регистрацию.',
            'from@ecomm-service.com',
            [user.email],
            fail_silently=False,
        )
        return f"Welcome email sent to {user.email}"
    except User.DoesNotExist:
        return "User not found"
