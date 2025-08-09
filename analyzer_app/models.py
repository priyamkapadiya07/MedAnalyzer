from django.db import models
from django.contrib.auth.models import User
# from .models import UserProfile
from django.db.models import JSONField


class Report(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # OCR and NLP processed results
    extracted_data = models.JSONField(null=True, blank=True, default=dict)  # example: {"Glucose": 180, "Hemoglobin": 12.3}
    diseases_detected = models.JSONField(null=True, blank=True, default=dict)  # example: {"Diabetes": "Yes", "Anemia": "No"}
    medicine_suggestions = models.JSONField(null=True, blank=True, default=dict)  # example: {"Diabetes": ["Metformin", "Insulin"]}

    def __str__(self):
        return f"Report of {self.user.username} on {self.uploaded_at.strftime('%Y-%m-%d')}"

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    
class UserQuestion(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    question = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"