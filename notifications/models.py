# notifications/models.py
from django.db import models
from students.models import Student
from organizations.models import Organization
from events.models import Event

class Notification(models.Model):
    TYPE_CHOICES = ["invite", "event", "role_change", "announcement"]
    ROLE_CHOICES = ['Committee', 'Manager']
    STATUS_CHOICES = ['pending', 'accepted', 'rejected', 'info']

    user_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    organization_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    event_id = models.ForeignKey(Event, on_delete=models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=50, choices=[(t,t) for t in TYPE_CHOICES])
    title = models.CharField(max_length=255)
    message = models.TextField()
    role = models.CharField(max_length=50, choices=[(r,r) for r in ROLE_CHOICES], blank=True, null=True)
    status = models.CharField(max_length=20, choices=[(s,s) for s in STATUS_CHOICES], default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"
        managed = False

    def __str__(self):
        return f"{self.type} - {self.title}"