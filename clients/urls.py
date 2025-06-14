from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.client_list_or_create, name='client_list_or_create'),
    path('clients/<int:id>/', views.client_detail_update_delete, name='client_detail_update_delete'),
    path('clients/<int:client_id>/projects/', views.project_create, name='project_create'),
    path('projects/', views.projects_by_user, name='projects_by_user'),
]
