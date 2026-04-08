import uuid
from django.db import models
from colleges.models import College

class Department(models.Model):
    _id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4, 
        editable=False
    )
    college = models.ForeignKey(
        College, 
        on_delete=models.DO_NOTHING, 
        related_name="departments", 
        db_column="college_id",
        to_field="_id" 
    )
    department_code = models.CharField(max_length=10, unique=True)
    department_name = models.CharField(max_length=255)

    class Meta:
        db_table = "departments"
        managed = False

    def __str__(self):
        return f"{self.department_code} - {self.department_name}"