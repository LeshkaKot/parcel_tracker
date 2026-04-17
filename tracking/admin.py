from django.contrib import admin
from .models import PostOffice, Parcel, ParcelStatusHistory


@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ['number', 'city', 'address', 'postal_code']
    search_fields = ['number', 'city', 'postal_code']
    ordering = ['city']


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = [
        'tracking_number', 'sender_name', 'receiver_name',
        'status', 'origin_office', 'destination_office', 'created_at'
    ]
    list_filter = ['status', 'origin_office', 'destination_office']
    search_fields = ['tracking_number', 'sender_name', 'receiver_name']
    readonly_fields = ['tracking_number', 'created_at']
    ordering = ['-created_at']


@admin.register(ParcelStatusHistory)
class ParcelStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'status', 'office', 'changed_at']
    list_filter = ['status', 'office']
    ordering = ['-changed_at']