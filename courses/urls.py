from django.urls import path

from . import views
from .views import CourseCreateView

urlpatterns = [

    path("courses/", views.CourseView.as_view(), name="all_courses"),
    path('courses/add', views.course_create_view, name="add_course"),
    path('courses/<int:pk>/update', views.course_edit_view, name="edit_course"),
    path('courses/<int:pk>/delete', views.CourseDeleteView.as_view(), name="delete_course"),

]
