from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # DateField to track appointment date
    slot = models.CharField(max_length=10)
    report = models.FileField(upload_to='reports/', blank=True, null=True)
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Appointment with {self.user.username} on {self.date}"
    
    
# models.py
class SlotAvailability(models.Model):
    date = models.DateField()
    section = models.CharField(max_length=20, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')])
    available_slots = models.IntegerField(default=20)

    class Meta:
        unique_together = ('date', 'section')  # Ensure date and section combination is unique

    def __str__(self):
        return f'{self.date} - {self.section} ({self.available_slots} slots remaining)'



from django.db import models

class ContactMessage(models.Model):
    username = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return self.username  # Display username in admin
