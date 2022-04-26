# rest framework
from rest_framework import serializers

# локальные импорты
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "name",
            "rating",
            "locale",
            "driver_rating",
            "user_rating",
            "avatar",
            "is_active",
            "is_staff",
            "is_superuser",
            "activist",
            "date_joined",
            "user_shipped_weight",
            "driver_shipped_weight",
        ]
