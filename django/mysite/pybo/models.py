from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Project(models.Model):
    NAME = models.CharField(max_length=50, null=False)
    KIND = models.CharField(max_length=50, null=False)
    GIT = models.CharField(max_length=200, null=False)
    GITTOKEN = models.CharField(max_length=100, null=False)
    SONARTOKEN = models.CharField(max_length=100, null=False)
    
