from djongo import models as djongo_models
from django.db import models
from students.models import Student
from organizations.models import Organization


# -----------------------
# Event
# -----------------------
class Event(models.Model):
    EVENT_TYPES = ["Event", "Sub-Event"]
    STATUS_CHOICES = ["Upcoming", "Ongoing", "Concluded", "Cancelled"]

    _id = djongo_models.ObjectIdField()  # explicit PK to prevent int() cast error

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

    reminders_twentyFourHours = models.BooleanField(default=False)
    reminders_oneHour = models.BooleanField(default=False)
    reminders_conclusion = models.BooleanField(default=False)

    class Meta:
        db_table = "events"
        managed = False

    def __str__(self):
        return self.event_name


# -----------------------
# Attendance Log
# -----------------------
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


# -----------------------
# Bookmark
# -----------------------
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


# -----------------------
# Feedback
# -----------------------
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