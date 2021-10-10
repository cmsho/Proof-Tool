from django.db import models

# Create your models here.
class Proof(models.Model):
    premise = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)
    proof_text = models.TextField()

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class Instructor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class Course(models.Model):
    title = models.CharField(max_length=255)

    # Relationships
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
        # One-to-many relationship (could perhaps be many-to-many)
        # If instructor is deleted, the course is preserved
    students = models.ManyToManyField(Student)
        # Many-to-many relationship

class Problem(models.Model):
    grade = models.DecimalField(max_digits=5, decimal_places=2)

    proof = models.ForeignKey(Proof, on_delete=models.CASCADE)
        # If the proof is deleted, the problem is deleted

class Assignment(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    due_by = models.DateTimeField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2)

    problems = models.ManyToManyField(Problem)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

