from django.urls import include, path

from .views import (
    CreateTaskView,
    EditTaskView,
    GetTaskView,
    TaskListView
)

urlpatterns = [
    path("task/create/", CreateTaskView.as_view(), name="create-task"),
    path("task/<int:pk>/edit/", EditTaskView.as_view(), name="edit-task"),
    path("task/list/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/detail/", GetTaskView.as_view(), name="task")
]