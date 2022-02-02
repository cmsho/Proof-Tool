from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
from proofchecker.proofs.proofutils import is_line_no, make_tree


def validate_line_no(value):
    try:
        is_line_no(value)
    except:
        raise ValidationError(
            _('%(value)s is not a valid line number'),
            params={'value': value},
        )


def validate_formula(value):
    try:
        make_tree(value)
    except:
        raise ValidationError(
            _('%(value)s is not a valid expression'),
            params={'value': value},
        )

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    mobile = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Instructor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    mobile = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Proof(models.Model):
    premises = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ("Proof {}:\nPremises: {},\nConclusion: {}\nLine Count: {}").format(
            self.pk,
            self.premises,
            self.conclusion,
            self.proofline_set.count()
        )

    def get_absolute_url(self):
        return "/proofs"


class ProofLine(models.Model):
    proof = models.ForeignKey(Proof, on_delete=models.CASCADE)
    line_no = models.CharField(max_length=100, validators=[validate_line_no])
    formula = models.CharField(max_length=255, validators=[validate_formula])
    rule = models.CharField(max_length=255)
    ORDER = models.IntegerField(null=True)

    def __str__(self):
        return ('Line {}: {}, {}'.format(
            self.line_no,
            self.formula,
            self.rule
        ))


class Problem(models.Model):
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    proof = models.ForeignKey(Proof, on_delete=models.CASCADE)
    # If the proof is deleted, the problem is deleted


class Course(models.Model):
    title = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    section = models.PositiveSmallIntegerField()
    # Relationships
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    # One-to-many relationship (could perhaps be many-to-many)
    # If instructor is deleted, the course is preserved
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    due_by = models.DateTimeField()
    problems = models.ManyToManyField(Problem)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/assignments"


class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
