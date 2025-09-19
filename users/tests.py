import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('password123')

@pytest.mark.django_db
def test_superuser_creation():
    admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
    assert admin_user.username == 'admin'
    assert admin_user.is_staff
    assert admin_user.is_superuser