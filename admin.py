# django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id", "name", "phone", "is_active", "is_staff", "is_superuser",)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    fieldsets = (
        ('Основная информация', {'fields': (('name', 'username', 'phone', 'avatar'), 'password', 'role', "comp")}),
        ('Права', {'fields': (
            'is_staff', 'is_active', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('phone', 'name', 'username'), ('password1', 'password2'),
                ('is_staff', 'is_active', 'is_superuser',),
            )}
         ),
    )
    search_fields = ('name', 'phone',)
    ordering = ("id", "name", "phone", "is_active", "is_staff", "is_superuser",)


admin.site.register(User, CustomUserAdmin)
