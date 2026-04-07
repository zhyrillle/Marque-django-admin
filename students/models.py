# students/models.py
from django.db import models
from users.models import User
from colleges.models import College
from departments.models import Department

class Student(models.Model):
    users_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    college_id = models.ForeignKey(College, on_delete=models.DO_NOTHING)
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    student_number = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "students"
        managed = False

    def __str__(self):
        return self.student_number