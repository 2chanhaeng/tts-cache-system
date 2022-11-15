from django.db import models


class Project(models.Model):
    project_title = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Sentence(models.Model):
    """
    Sentence model
    text: str = text of the sentence
    """

    text = models.TextField(unique=True)


class Audio(models.Model):
    index = models.IntegerField()
    text = models.TextField(unique=True)
    speed = models.FloatField(default=1.0)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
