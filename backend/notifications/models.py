from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    TYPE_CHOICES = (
        ('listing',   'Listing'),
        ('booking',   'Booking'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', db_index=True)
    type  = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)  # ← removed duplicate
    title = models.CharField(max_length=255)
    body  = models.TextField()
    read  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.title