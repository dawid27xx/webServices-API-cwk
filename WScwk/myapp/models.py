from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    professor_code = models.CharField(max_length=5)
    full_name = models.CharField(max_length=100)

class Module(models.Model):
    module_code = models.CharField(max_length=5)
    module_name = models.CharField(max_length=100)

class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    score = models.IntegerField()
