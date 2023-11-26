from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task.models import TaskType, Task, Position
from datetime import datetime


POSITION_URL = reverse("task:position-list")
TASKTYPE_URL = reverse("task:tasktype-list")
TASK_URL = reverse("task:task-list")
WORKER_URL = reverse("task:worker-list")


class PublicTests(TestCase):
    def test_task_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_tasktype_login_required(self):
        res = self.client.get(TASKTYPE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_worker_login_required(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_position_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTests(TestCase):

    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="user1pass",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_tasktypes(self):
        TaskType.objects.create(name="BugFix")
        TaskType.objects.create(name="NewFeature")
        response = self.client.get(TASKTYPE_URL)
        tasktype_all = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(tasktype_all)
        )
        self.assertTemplateUsed(response, "task/tasktype_list.html")


class PrivateTaskTests(TestCase):

    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="user1pass",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_search_form_initial(self):
        response = self.client.get(TASK_URL)
        form = response.context["search_form"]

        self.assertEqual(form.initial["name"], "")

    def test_retrieve_tasks(self):
        Task.objects.create(
            name="task1",
            description="description1",
            deadline=datetime.now().date(),
            priority="Low",
            is_completed=False,
            task_type=TaskType.objects.create(name="BugFix")
        )
        Task.objects.create(
            name="testtask2",
            description="testdescription2",
            deadline=datetime.now().date(),
            priority="High",
            is_completed=False,
            task_type=TaskType.objects.create(name="NewFeature")
        )
        task_all = Task.objects.all()
        response = self.client.get(TASK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(task_all)
        )

        self.assertTemplateUsed(
            response,
            "task/task_list.html"
        )


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="user1pass",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        get_user_model().objects.create(
            username="user1name",
            first_name="first1",
            password="pass155111",
            last_name="last1",
            email="user1@user.com",
            position=self.position
        )
        get_user_model().objects.create(
            username="user111",
            password="pass1111",
            first_name="user11first",
            last_name="userl11ast",
            email="user2@user.com",
            position=self.position
        )

        response = self.client.get(WORKER_URL)
        worker_all = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(worker_all)
        )
        self.assertTemplateUsed(
            response,
            "task/worker_list.html"
        )


class PrivatePositionTests(TestCase):

    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="user1pass",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        Position.objects.create(name="Tester")
        Position.objects.create(name="Leader")

        response = self.client.get(POSITION_URL)
        position_all = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(position_all)
        )

        self.assertTemplateUsed(
            response,
            "task/position_list.html"
        )
