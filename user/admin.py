from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = [
        'full_name',
        "phone_number",
        'email',
        'birth_date',
        'is_admin',
        'is_active',

    ]
    list_display_links = ['full_name', 'phone_number', 'email']
    list_filter = []
    fieldsets = [
        (None, {"fields": [
            "phone_number",
            'email',
            'full_name',
            'birth_date',
            'image',
            'is_admin',
            'password',
        ]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "phone_number",
                    'email',
                    'full_name',
                    'birth_date',
                    'image',
                    'is_admin',
                    'password1',
                    'password2',
                ],
            },
        ),
    ]
    ordering = ["id"]
    filter_horizontal = []
    search_fields = [
        "phone_number",
        'full_name',
        'email'
    ]


admin.site.register(CustomUser, CustomUserAdmin)
