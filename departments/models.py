from django.db import models
from colleges.models import College

class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="departments")
    department_code = models.CharField(max_length=10, unique=True)
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.department_code} - {self.department_name}"