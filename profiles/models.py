from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('Never Married', 'Never Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)
    mother_tongue = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    height = models.CharField(max_length=10)  # e.g., "5'6\""
    weight = models.CharField(max_length=10, blank=True)
    occupation = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    annual_income = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    # Admin fields
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    
    # Tracking fields
    profile_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.username}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={'pk': self.pk})

class InterestRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_interests')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_interests')
    message = models.TextField(max_length=300, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['sender', 'receiver']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.user.username} -> {self.receiver.user.username}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
