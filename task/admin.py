from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Task, TaskType, Worker, Position


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ("position",)
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = (
        "is_completed",
        "status",
        "assignees",
        "task_type",
        "priority",
        "deadline",
    )
    list_display = (
        "name",
        "is_completed",
        "status",
        "task_type",
        "description",
        "deadline",
        "priority",
        "all_assignees",
    )

    def all_assignees(self, task):
        return ", ".join([worker.username for worker in task.assignees.all()])

    all_assignees.short_description = "assignees"


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
