from django.contrib import admin

from .models import User, Proof, Student, Instructor, Assignment, Course, StudentAssignment

# Register your models here.
admin.site.register(User)
admin.site.register(Proof)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(StudentAssignment)
