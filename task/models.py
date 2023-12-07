from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from tasks_manager.settings import AUTH_USER_MODEL


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "L", "Low"
        MEDIUM = "M", "Medium"
        HIGH = "H", "High"

    class Status(models.TextChoices):
        IN_PROGRESS = "IP", "In progress"
        IN_PROGRESS_AFTER_DEADLINE = "IPAD", "In progress after the deadline"
        COMPLETED_ON_TIME = "COT", "Completed on time"
        COMPLETED_AFTER_DEADLINE = "CAD", "Completed after the deadline"

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )
    description = models.TextField()
    deadline = models.DateField()
    time_completed = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=7,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.name

    def update_task_status(self):
        if self.time_completed:
            if self.deadline >= self.time_completed.date():
                self.status = "Completed on time"
            else:
                self.status = "Completed after the deadline"
        else:
            if self.deadline >= timezone.now().date():
                self.status = "In progress"
            else:
                self.status = "In progress after the deadline"
        self.save()
