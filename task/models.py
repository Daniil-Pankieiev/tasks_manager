from django.db import models
from django.contrib.auth.models import AbstractUser

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
    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )
    STATUS_CHOICES = (
        ("In progress", "In progress"),
        ("Completed on time", "Completed on time"),
        ("Completed after the deadline", "Completed after the deadline"),
    )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="In progress",
    )
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="LOW",
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.name
