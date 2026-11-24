from django.contrib import admin
from .models import UserProfile, Address


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'state', 'postal_code', 'is_default_shipping', 'address_type')
    list_filter = ('is_default_shipping', 'address_type', 'country')
    search_fields = ('full_name', 'street_address', 'city', 'user__username')

