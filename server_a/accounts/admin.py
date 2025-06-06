from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'classes': ("wide",), 'fields': ('avatar',)}),
    )
    add_fieldsets = (
        (None, {'classes': ("wide",), 'fields': ('username', 'email', 'password1', 'password2', 'avatar',)}),
    )

    list_display = ['email', 'username']

admin.site.register(CustomUser, CustomUserAdmin)


