# users/models.py
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Student', 'Student'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.URLField(blank=True, default="")

    class Meta:
        db_table = "users"
        managed = True

    def __str__(self):
        return f"{self.firstname} {self.lastname}"