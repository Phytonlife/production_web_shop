from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent"]

class ProductSerializer(serializers.ModelSerializer):
    # Чтобы в API вместо id категории видеть ее название
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "category_name",
            "image",
            "is_active",
            "created_at",
        ]
        # Поле category будет только для записи (при создании/обновлении товара)
        read_only_fields = ["category_name", "created_at"]
