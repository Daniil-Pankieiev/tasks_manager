from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.test import TestCase

from task.models import TaskType, Position, Task


class ModelsTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="test_tasktype")
        self.position = Position.objects.create(name="test_position")
        self.worker1 = get_user_model().objects.create(
            username="user1",
            password="pass1",
            first_name="userfirst",
            last_name="userlast",
            position=self.position
        )
        self.worker2 = get_user_model().objects.create(
            username="user2",
            password="pass2",
            first_name="userfirst2",
            last_name="userlast2",
            position=self.position
        )

        self.task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline=datetime.now().date(),
            is_completed=False,
            priority="low",
            task_type=self.task_type,
        )

        self.task2 = Task.objects.create(
            name="test_task2",
            description="test_description2",
            deadline=date(2023, 11, 20),
            is_completed=False,
            priority="low",
            task_type=self.task_type,
        )

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "test_tasktype")

    def test_task_str(self):
        self.assertEqual(str(self.task), "test_task")

    def test_position_str(self):
        self.assertEqual(str(self.position), "test_position")

    def test_worker_str(self):
        self.assertEqual(str(self.worker1), "user1 (userfirst userlast)")
