from datetime import datetime

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.test import TestCase
from task.admin import WorkerAdmin, TaskTypeAdmin, PositionAdmin, TaskAdmin
from task.models import Worker, TaskType, Position, Task


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.worker_admin = WorkerAdmin(Worker, self.site)
        self.position_admin = PositionAdmin(Position, self.site)
        self.task_admin = TaskAdmin(Task, self.site)
        self.task_type_admin = TaskTypeAdmin(TaskType, self.site)
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="test_tasktype")
        self.worker1 = get_user_model().objects.create(
            username="user1",
            password="pass1",
            first_name="userfirst",
            last_name="userlast",
            position=self.position,
        )

    def test_task_all_assignees(self):
        task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline=datetime.now().date(),
            is_completed=False,
            priority="low",
            task_type=self.task_type,
        )
        task.assignees.add(self.worker1)

        result = self.task_admin.all_assignees(task)

        self.assertIn(self.worker1.username, result)

    def test_all_assignees_short_description(self):
        self.assertEqual(
            self.task_admin.all_assignees.short_description,
            "assignees"
        )

    def test_task_list_filter(self):
        expected_filters = [
            "is_completed",
            "status",
            "assignees",
            "task_type",
            "priority",
            "deadline",
        ]
        self.assertEqual(list(self.task_admin.list_filter), expected_filters)

    def test_task_list_display(self):
        expected_display = (
            "name",
            "is_completed",
            "status",
            "task_type",
            "description",
            "deadline",
            "priority",
            "all_assignees",
        )
        self.assertEqual(self.task_admin.list_display, expected_display)

    def test_position_listed(self):
        user_worker = Worker.objects.get(username="user1")
        self.assertEqual(user_worker.position, self.position)

    def test_admin_list_display(self):
        expected = UserAdmin.list_display + ("position",)
        self.assertEqual(self.worker_admin.list_display, expected)

    def test_admin_list_filter(self):
        admin_filters = UserAdmin.list_filter
        expected = admin_filters + ("position",)
        self.assertEqual(self.worker_admin.list_filter, expected)

    def test_admin_fieldsets(self):
        admin_fieldsets = UserAdmin.fieldsets
        expected = admin_fieldsets + (
            ("Additional info", {"fields": ("position",)}),
        )
        self.assertEqual(self.worker_admin.fieldsets, expected)
