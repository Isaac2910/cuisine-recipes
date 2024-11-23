from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('name', 'phone',)
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('name', 'phone', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'name', 'email', 'phone', 'is_staff', 'is_active')
    search_fields = ('username', 'name', 'email')
    ordering = ('username',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('title', 'description', 'ingredients')
    ordering = ('-created_at',)
    raw_id_fields = ('user',)  # Facilite la sélection des utilisateurs dans l'interface d'administration


# Enregistrement du modèle utilisateur personnalisé avec la configuration étendue
admin.site.register(User, CustomUserAdmin)