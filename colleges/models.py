from django.db import models

class College(models.Model):
    college_code = models.CharField(max_length=10, unique=True)
    college_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.college_code} - {self.college_name}"