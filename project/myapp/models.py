from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    professor_code = models.CharField(max_length=4, unique=True)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} ({self.professor_code})"

class Module(models.Model):
    module_code = models.CharField(max_length=4, unique=True)
    module_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.module_code} - {self.module_name}" 

class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    professors = models.ManyToManyField(Professor)  

    def __str__(self):
        professor_names = ", ".join([prof.full_name for prof in self.professors.all()])
        return f"{self.module.module_code} ({self.year}, Semester {self.semester}) - {professor_names}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.module_instance} ({self.score})"

