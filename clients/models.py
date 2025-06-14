from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='clients_created', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    client_ref = models.ForeignKey(Client, related_name='associated_projects', on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, related_name='assigned_projects')
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='projects_created', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
