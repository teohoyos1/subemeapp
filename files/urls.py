from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('list/', views.get_file_type_list, name='list'),
    path('list/<str:data>/', views.get_file_type_list),
    path('about/', views.about, name='about'),
    path('add-file-page/', views.file_create_new, name='addNewFilePage'),
    path('add-file-page/new-group/',views.file_group_create_new, name='createFileGroup'),
]
