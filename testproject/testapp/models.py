from django.db import models

# Create your models here.

class TestModel(models.Model):
    field = models.FileField()
