from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'file', views.FileView,'file')
router.register(r'file_type',views.FileTypeView,'file_type')

urlpatterns = [
    path('', views.index, name='home'),
    path('list/', views.get_file_type_list, name='list'),
    path('list/<str:data>/', views.get_file_type_list),
    path('about/', views.about, name='about'),
    path('add-file-page/', views.file_create_new, name='addNewFilePage'),
    path('add-file-page/new-group/',views.file_group_create_new, name='createFileGroup'),
    path('deleteFile/<int:id>', views.deleteFileById, name='deleteFile'),
    path('list/ajax/generatepdf/',views.generateZipAjax, name="generateZipAjax"),
    path('list/ajax/files/',views.getAndUpdateFileObject, name='getAndUpdateFileAjax'),
    path('api/', include(router.urls))
]
