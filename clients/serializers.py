from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'date_created', 'creator']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    client_ref = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    team_members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'title', 'client_ref', 'team_members', 'date_created', 'creator']

    def create(self, validated_data):
        members_data = validated_data.pop('team_members')
        project = Project.objects.create(**validated_data)
        project.team_members.set(members_data)
        project.save()
        return project
