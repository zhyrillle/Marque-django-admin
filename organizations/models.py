from django.db import models
from departments.models import Department

class Organization(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=255)
    org_type = models.CharField(max_length=100)
    description = models.TextField()

    pfp = models.ImageField(upload_to='pfp/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover/', blank=True, null=True)

    fb_link = models.URLField(blank=True, null=True)
    ig_link = models.URLField(blank=True, null=True)
    x_link = models.URLField(blank=True, null=True)

    moderator_name = models.CharField(max_length=255)

    def __str__(self):
        return self.org_name