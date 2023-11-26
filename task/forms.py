from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from task.models import Task, Worker


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees"
        )

    def clean_deadline(self):
        if self.cleaned_data["deadline"] < datetime.now().date():
            raise ValidationError(
                "Deadline can not be earlier than today"
            )
        return self.cleaned_data["deadline"]



class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )