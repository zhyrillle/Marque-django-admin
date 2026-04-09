from djongo import models as djongo_models
from django.db import models
from students.models import Student
from organizations.models import Organization


def default_reminders():
    return {
        "twentyFourHours": False,
        "oneHour": False,
        "conclusion": False
    }

class Event(models.Model):
    EVENT_TYPES = ["Event", "Sub-Event"]
    STATUS_CHOICES = ["Upcoming", "Ongoing", "Concluded", "Cancelled"]

    _id = djongo_models.ObjectIdField(primary_key=True)  # explicit PK to prevent int() cast error

    organization_id = models.CharField(max_length=24)  # stored as string
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=[(t, t) for t in EVENT_TYPES])
    description = models.TextField()
    event_image = models.URLField(blank=True, null=True)
    event_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    venue_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[(s, s) for s in STATUS_CHOICES], default="Upcoming")
    is_mandatory = models.BooleanField(default=False)

    remindersSent = djongo_models.JSONField(default=default_reminders)

    class Meta:
        db_table = "events"
        managed = False

    def __str__(self):
        return self.event_name

    @property
    def reminders_twentyFourHours(self):
        return (self.remindersSent or {}).get("twentyFourHours", False)

    @reminders_twentyFourHours.setter
    def reminders_twentyFourHours(self, value):
        if not self.remindersSent:
            self.remindersSent = default_reminders()
        self.remindersSent["twentyFourHours"] = bool(value)

    @property
    def reminders_oneHour(self):
        return (self.remindersSent or {}).get("oneHour", False)

    @reminders_oneHour.setter
    def reminders_oneHour(self, value):
        if not self.remindersSent:
            self.remindersSent = default_reminders()
        self.remindersSent["oneHour"] = bool(value)

    @property
    def reminders_conclusion(self):
        return (self.remindersSent or {}).get("conclusion", False)

    @reminders_conclusion.setter
    def reminders_conclusion(self, value):
        if not self.remindersSent:
            self.remindersSent = default_reminders()
        self.remindersSent["conclusion"] = bool(value)

class AttendanceLog(models.Model):
    STATUS_CHOICES = ['Present', 'Absent', 'Late']
    PHOTO_STATUS_CHOICES = ['pending', 'verified', 'rejected']

    _id = djongo_models.ObjectIdField()

    event_id = models.ForeignKey(Event, on_delete=models.DO_NOTHING, db_column='event_id')
    user_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, db_column='user_id')
    status = models.CharField(max_length=20, choices=[(s, s) for s in STATUS_CHOICES])
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(blank=True, null=True)
    photoproof_url = models.URLField(blank=True, null=True)
    photoproof_status = models.CharField(max_length=20, choices=[(s, s) for s in PHOTO_STATUS_CHOICES], default='pending')
    photoproof_submitted_at = models.DateTimeField(blank=True, null=True)
    photoproof_verified_by = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name='verified_logs',
        db_column='photoproof_verified_by'
    )
    photoproof_verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "attendance_logs"
        managed = False

    def __str__(self):
        return f"{self.user_id} - {self.event_id}"

class Bookmark(models.Model):
    _id = djongo_models.ObjectIdField()

    event_id = models.ForeignKey(Event, on_delete=models.DO_NOTHING, db_column='event_id')
    user_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, db_column='user_id')

    class Meta:
        db_table = "bookmarks"
        managed = False
        unique_together = [('event_id', 'user_id')]

    def __str__(self):
        return f"{self.user_id} bookmarked {self.event_id}"

class Feedback(models.Model):
    _id = djongo_models.ObjectIdField()

    event_id = models.ForeignKey(Event, on_delete=models.DO_NOTHING, db_column='event_id')
    user_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, db_column='user_id')

    overall_experience = models.IntegerField()
    venue_facilities = models.IntegerField()
    speakers_program = models.IntegerField()
    event_organization = models.IntegerField()

    comment = models.TextField(blank=True, default="")
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        db_table = "feedbacks"
        managed = False
        unique_together = [('event_id', 'user_id')]

    def __str__(self):
        return f"Feedback by {self.user_id} for {self.event_id}"