from django.db import models

class Category(models.Model):
    """Модель категорий услуг"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-слаг")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    # Для вложенности категорий (например, "Курсы" -> "Программирование")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель услуг/товаров"""
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-слаг")
    description = models.TextField(verbose_name="Описание")
    # DecimalField лучше подходит для финансовых расчетов, чем FloatField
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT, # Защита от случайного удаления категории с товарами
        related_name='products',
        verbose_name="Категория"
    )
    # Для хранения изображений понадобится Pillow
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар/Услуга"
        verbose_name_plural = "Товары/Услуги"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name