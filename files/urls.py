from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'file', views.FileView,'file')
router.register(r'file_type',views.FileTypeView,'file_type')

urlpatterns = [
    path('', views.index, name='home'),
    path('list/file/', views.get_file_type_list, name='listFile'),
    path('list/file/<str:data>/', views.get_file_type_list),
    path('about/', views.about, name='about'),
    path('list/group/', views.file_create_new, name='listGroup'),
    path('add/group/',views.file_group_create_new, name='createFileGroup'),
    path('edit/group/', views.file_group_edit, name="editFileGroup"),
    path('delete/group/<int:id>/', views.deleteGroupById, name="deleteGroup"),
    path('delete/file/<int:id>/', views.deleteFileById, name='deleteFile'),
    path('list/ajax/generatepdf/',views.generateZipAjax, name="generateZipAjax"),
    path('list/ajax/files/',views.getAndUpdateFileObject, name='getAndUpdateFileAjax'),
    path('api/', include(router.urls))
]
