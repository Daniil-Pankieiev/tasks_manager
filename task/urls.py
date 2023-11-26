from django.urls import path

from task.views import (
    TaskListView,
    index,
    TaskDetailView,
    toggle_assign_to_task,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list",
    ),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="tasks-create",
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),
]
app_name = "task"
