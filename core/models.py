import uuid

from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=100)


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
