from django.contrib import admin

from .models import User, Proof, Problem, Student, Instructor, Assignment, Course, StudentAssignment, ProofLine

# Register your models here.
admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(StudentAssignment)

class ProofLineInline(admin.TabularInline):
    model = ProofLine

@admin.register(Proof)
class ProofAdmin(admin.ModelAdmin):
    inlines = [
        ProofLineInline,
    ]