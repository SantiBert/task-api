from django.urls import include, path

from .views import (
    CreateTaskView,
    EditTaskView,
    GetTaskView,
    TaskListView
)

urlpatterns = [
    path("create/", CreateTaskView.as_view(), name="create-task"),
    path("<int:pk>/edit/", EditTaskView.as_view(), name="edit-task"),
    path("list/", TaskListView.as_view(), name="tasks-list"),
    path("<int:pk>/task/", GetTaskView.as_view(), name="task")
]