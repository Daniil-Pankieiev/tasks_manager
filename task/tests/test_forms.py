from django.test import TestCase
from task.forms import (
    TaskTypeSearchForm,
    WorkerCreationForm,
    PositionSearchForm
)
from task.models import Position
from django.contrib.auth import get_user_model


class FormsTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.position = Position.objects.create(name="Developer")
        self.worker1 = get_user_model().objects.create(
            username="user1",
            password="pass1",
            first_name="userfirst",
            last_name="userlast",
            position=self.position,
        )

    def test_task_type_search_form(self):
        form_data = {"name": "TaskType"}
        form = TaskTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_position_search_form(self):
        form_data = {"name": "Developer"}
        form = PositionSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_form_invalid(self):
        form_data = {
            "username": "user1test",
            "first_name": "userfirst",
            "last_name": "userlast",
            "email": "user@user.com",
            "position": self.position.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_worker_form_valid(self):
        form_data = {
            "username": "user1test",
            "first_name": "userfirst",
            "last_name": "userlast",
            "email": "user@user.com",
            "position": self.position.id,
            "password1": "testpass1",
            "password2": "testpass1",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
