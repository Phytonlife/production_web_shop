from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя.
    На данном этапе не добавляем новых полей, но это позволит
    легко расширять модель в будущем, не ломая миграции.
    """
    pass