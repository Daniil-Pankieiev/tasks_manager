from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from task.forms import (
    TaskSearchForm,
    TaskForm,
    WorkerSearchForm,
    WorkerCreationForm,
    TaskTypeSearchForm,
    PositionSearchForm,
)
from task.models import Task, TaskType, Position
from task.mixins.check_superuser import SuperUserCheckMixin


def index(request):
    """View function for the home page of the site."""

    num_workers = get_user_model().objects.count()
    num_tasks = Task.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_positions": num_positions,
        "num_visits": num_visits + 1,
    }

    return render(request, "task/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("task_type")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
                "task_type",
            ).prefetch_related(
                "assignees__position",
            )

    def get_object(self, queryset=None):
        task = super().get_object(queryset=queryset)
        task.update_task_status()
        return task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")


class TaskDeleteView(SuperUserCheckMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


@login_required
def toggle_assign_to_task(request, pk):
    worker = get_user_model().objects.get(id=request.user.id)
    if Task.objects.get(id=pk) in worker.tasks.all():
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("task:task-detail", args=[pk]))


class WorkerListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.select_related(
            "position",
        )
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        worker_id = self.kwargs["pk"]

        worker = get_user_model().objects.get(id=worker_id)

        tasks_in_progress = worker.tasks.filter(is_completed=False)
        completed_tasks = worker.tasks.filter(is_completed=True)

        context["tasks_in_progress"] = tasks_in_progress
        context["completed_tasks"] = completed_tasks

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task:worker-list")


class WorkerDeleteView(SuperUserCheckMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task:index")


@login_required
def finish_task(request, pk):
    task = Task.objects.get(id=pk)
    task.is_completed = True
    task.time_completed = datetime.now().date()
    task.save()
    return HttpResponseRedirect(reverse_lazy("task:task-detail", args=[pk]))


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task:tasktype-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task:tasktype-list")


class TaskTypeDeleteView(SuperUserCheckMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task:tasktype-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionDeleteView(SuperUserCheckMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task:position-list")
