from django.db import models
from students.models import Student
from departments.models import Department
import uuid

class Organization(models.Model):
    ORG_TYPES = [
        ("Unit Organization", "Unit Organization"),
        ("Mother Organization", "Mother Organization"),
        ("FAESO Organization", "FAESO Organization"),
    ]

    _id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4, 
        editable=False
    )
    department_id = models.CharField(max_length=24)
    org_name = models.CharField(max_length=255)
    org_type = models.CharField(max_length=50, choices=ORG_TYPES)
    description = models.TextField()
    pfp = models.URLField(blank=True, null=True)
    cover_photo = models.URLField(blank=True, null=True)
    fb_link = models.URLField(blank=True, null=True)
    ig_link = models.URLField(blank=True, null=True)
    x_link = models.URLField(blank=True, null=True)
    moderator_name = models.CharField(max_length=255)

    class Meta:
        db_table = "organizations"
        managed = False

    def __str__(self):
        return self.org_name


class OrgOfficer(models.Model):
    ROLE_CHOICES = ['Committee', 'Manager', 'President']

    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    org_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=50, choices=[(r,r) for r in ROLE_CHOICES])
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "org_officers"
        managed = False
        unique_together = [('student_id', 'role')]  # for president uniqueness

    def __str__(self):
        return f"{self.student_id} - {self.role}"


class JoinRequest(models.Model):
    STATUS_CHOICES = ['Pending', 'Approved', 'Rejected']

    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    organization_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=[(s,s) for s in STATUS_CHOICES], default='Pending')

    class Meta:
        db_table = "join_requests"
        managed = False
        unique_together = [('student_id', 'organization_id')]

    def __str__(self):
        return f"{self.student_id} request to join {self.organization_id}"


class FollowedOrgs(models.Model):
    user_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    organization_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "followed_orgs"
        managed = False
        unique_together = [('user_id', 'organization_id')]

    def __str__(self):
        return f"{self.user_id} follows {self.organization_id}"