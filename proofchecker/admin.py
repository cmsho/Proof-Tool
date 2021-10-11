from django.contrib import admin
from .models import Proof, Student, Instructor, Assignment, Course

# Register your models here.
admin.site.register(Proof)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Assignment)
admin.site.register(Course)