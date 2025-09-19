from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with fake data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))

        # Create regular users
        for _ in range(10):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
            )
        self.stdout.write(self.style.SUCCESS('Created 10 fake users.'))

        # Create Categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.unique.word().capitalize(),
                slug=fake.unique.slug(),
                description=fake.text(max_nb_chars=100),
            )
            categories.append(category)
        self.stdout.write(self.style.SUCCESS('Created 5 fake categories.'))

        # Create Products
        for _ in range(20):
            product = Product.objects.create(
                name=fake.unique.sentence(nb_words=3).replace('.', '').capitalize(),
                slug=fake.unique.slug(),
                description=fake.text(max_nb_chars=500),
                price=random.randint(100, 10000) / 100.0,
                category=random.choice(categories),
                is_active=True,
            )
        self.stdout.write(self.style.SUCCESS('Created 20 fake products.'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
