from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from . models import Customer


UserModel = get_user_model()

@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    ordering = ('email', )
    list_display = ['email', 'date_joined', 'last_login', ]
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #(('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
