import uuid
from django.db import models

class College(models.Model):
    _id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4, 
        editable=False
    )
    college_code = models.CharField(max_length=10, unique=True)
    college_name = models.CharField(max_length=255)

    class Meta:
        db_table = "colleges"
        managed = False

    def __str__(self):
        return f"{self.college_code} - {self.college_name}"