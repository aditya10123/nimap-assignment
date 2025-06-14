from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def client_list_or_create(request):
    if request.method == 'GET':
        all_clients = Client.objects.all()
        serializer = ClientSerializer(all_clients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def client_detail_update_delete(request, id):
    try:
        client_obj = Client.objects.get(id=id)
    except Client.DoesNotExist:
        return Response({'detail': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        related_projects = client_obj.associated_projects.all()
        project_serializer = ProjectSerializer(related_projects, many=True)
        client_serializer = ClientSerializer(client_obj)
        data = client_serializer.data
        data['projects'] = project_serializer.data
        return Response(data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ClientSerializer(client_obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        client_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def project_create(request, client_id):
    try:
        client_obj = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({'detail': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    member_ids = [user_data['id'] for user_data in request.data.get('team_members', [])]
    members = User.objects.filter(id__in=member_ids)

    if len(members) != len(member_ids):
        return Response({'detail': 'Some team members not found'}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'title': request.data.get('title'),
        'client_ref': client_obj.id,
        'creator': request.user.id,
        'team_members': member_ids,
    }

    serializer = ProjectSerializer(data=data)

    if serializer.is_valid():
        project = serializer.save()

        response_data = {
            'id': project.id,
            'title': project.title,
            'client': client_obj.name,
            'team_members': [{'id': member.id, 'name': member.username} for member in project.team_members.all()],
            'date_created': project.date_created.isoformat(),
            'creator': project.creator.username,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def projects_by_user(request):
    user_projects = request.user.assigned_projects.all()
    serialized_projects = ProjectSerializer(user_projects, many=True)

    response_data = []
    for project in serialized_projects.data:
        response_data.append({
            'id': project['id'],
            'title': project['title'],
            'date_created': project['date_created'],
            'creator': project['creator'],
        })

    return Response(response_data)
