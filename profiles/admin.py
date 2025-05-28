from django.contrib import admin
from .models import UserProfile, InterestRequest, ContactMessage

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'age', 'religion', 'caste', 'occupation', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['gender', 'religion', 'is_approved', 'is_featured', 'is_premium', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'occupation', 'education']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['created_at', 'updated_at', 'profile_views']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'date_of_birth', 'gender', 'photo')
        }),
        ('Personal Details', {
            'fields': ('religion', 'caste', 'mother_tongue', 'marital_status', 'height', 'weight', 'location', 'bio')
        }),
        ('Professional Details', {
            'fields': ('occupation', 'education', 'annual_income')
        }),
        ('Admin Controls', {
            'fields': ('is_approved', 'is_featured', 'is_premium')
        }),
        ('Statistics', {
            'fields': ('profile_views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(InterestRequest)
class InterestRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__user__username', 'receiver__user__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
