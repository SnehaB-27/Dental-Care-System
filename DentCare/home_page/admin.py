from django.contrib import admin
from .models import Appointment  # Import your model

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'slot', 'bill')  # Columns to display in the admin panel
    search_fields = ('user__username', 'date')  # Add search functionality
    list_filter = ('date', 'slot')  # Add filtering options
    
admin.site.register(Appointment, AppointmentAdmin)  # Register the model with the admin site




from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at','message')  # Display these fields in admin
    search_fields = ('username',)  # Enable search by username

admin.site.register(ContactMessage, ContactMessageAdmin)  # Register the model with the admin site
