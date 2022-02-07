from django.urls import path, include
from . import views

urlpatterns = [

    path("courses/", views.CourseView.as_view(), name="all_courses"),
    path('courses/add', views.CourseCreateView.as_view(), name="add_course"),
    path('courses/<pk>/update', views.CourseUpdateView.as_view(), name="edit_course"),
    path('courses/<pk>/delete', views.CourseDeleteView.as_view(), name="delete_course"),

]
