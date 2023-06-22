from django.db import models

class Project(models.Model):
    repository = models.CharField(max_length=200)
    desc = models.CharField(max_length=400,default="")
    repo = models.CharField(max_length=200)
    lang = models.CharField(max_length=200)
    owner = models.CharField(max_length=200, default="")

class Issue(models.Model):
    repository = models.CharField(max_length=200,default="")
    title = models.CharField(max_length=200)
    labels = models.CharField(max_length=200)
    owner = models.CharField(max_length=200,default="")
    url = models.URLField()
