from multiprocessing import context
import os
from django.db.models import RestrictedError
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required #CREADOTEO
from django.contrib import messages
import zipfile
import io
from urllib.request import urlopen
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED
from rest_framework import viewsets

from .models import Fi_file, Fi_file_type
from .forms import Fi_file_typeForm, Fi_fileForm, Fi_fileFormEditWOFile, Fi_fileFormEditWithFile
from files.serializers import Fi_file_serializer,Fi_file_type_serializer

class FileView(viewsets.ModelViewSet):
    serializer_class = Fi_file_serializer
    queryset = Fi_file.objects.all()

class FileTypeView(viewsets.ModelViewSet):
    serializer_class = Fi_file_type_serializer
    queryset = Fi_file_type.objects.all()

def index(request):
    return render(request, 'home.html')

@login_required
def get_file_type_list(request):

    query=""
    filesParent = None
    try:
        if any(request.GET):
            query = request.GET.get('qr')
    except:
        query=""

    typeObjFather = Fi_file_type.objects.filter(name__contains=query, isActive=1).order_by('id')
    if typeObjFather.exists():
        listIds = []
        for data in typeObjFather:
            listIds.append(data.pk)
        filesParent = Fi_file.objects.filter(fileType_id__in=listIds).order_by('fileType_id')
    context = {
        'typeObjFather':typeObjFather,
         'filesParent': filesParent
    }
    return render(request, 'fileList/fileList.html', context)

def about(request):
    return render(request, 'about.html')

#ADDPAGE - GROUP, TYPEFILE, FILE
@login_required
def file_create_new(request):
    context = {}
    if request.method == 'POST':
        form = Fi_fileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Archivo creado con éxito')
            return redirect(file_create_new)
    else:
        form = Fi_fileForm()
    try:
        objGroupSelect = Fi_file_type.objects.all().order_by("pk")
    except:
        objGroupSelect = None
    context = {
        'form_file':form,
        'objGroupSelect': objGroupSelect
    }
    return render(request, 'fileList/fileAdd.html',context)

@login_required
def file_group_create_new(request):

    context = {}
    if request.method == "POST":
        form = Fi_file_typeForm(request.POST)
        print(form)
        context['form'] = form

        if form.is_valid():
            form.save()
            messages.success(request, f"Se ha guardado correctamente el grupo")
            return redirect(file_create_new)
        else:
            print(form.errors)
            # messages.error(request, form.errors.get('message'))
    return redirect(file_create_new)

@login_required
def deleteFileById(request, id):
    if request.method == "GET":
        try:
            obj = Fi_file.objects.get(pk=id)
        except Fi_file.DoesNotExist:
            obj = None
        if obj:
            obj.delete()
            messages.success(request, "Se ha eliminado con éxito")
        else:
            messages.error(request, "Se ha producido un error, no se ha podido eliminar el archivo")
    return redirect(get_file_type_list)

def deleteGroupById(request, id):
    if request.method == "GET":
        try:
            obj = Fi_file_type.objects.get(pk=id)
        except Fi_file_type.DoesNotExist:
            obj = None
        if obj:
            try:
                obj.delete()
                messages.success(request, "Se ha eliminado con éxito")
            except RestrictedError:
                messages.warning(request, "No es posible eliminar el grupo si tiene asociado archivos, elimine los archivos antes de volver a eliminar este grupo")
        else:
            messages.error(request, "Se ha producido un error, no se ha podido eliminar el archivo")
    return redirect(file_group_create_new)


@login_required
def generateZipAjax(request):
    if request.method == "POST":
        if request.POST.get('id'):
            qrId = int(request.POST.get('id'))
            fileObj = Fi_file.objects.filter(fileType=qrId).exclude(files=None)
            if fileObj.exists():
                zipname = request.POST.get('name')
                s = io.BytesIO()
                zf = zipfile.ZipFile(s, "w")
                try:
                    if str(os.getenv('USE_S3_CLOUD')) == "1":
                        fileUrl = ''
                        for file in fileObj:
                            if file.files:
                                fileUrl = file.files.url
                                url = urlopen(fileUrl)
                                fname = os.path.split(fileUrl)[1]
                                zf.writestr(fname,url.read())
                    else:
                        for file in fileObj:
                            if file.files:
                                fileUrl = file.files.url
                                fname = os.path.split(fileUrl)[1]
                                zf.write("."+file.files.url,fname)
                                print('.'+file.files.url)
                finally:
                    zf.close()

                response = HttpResponse(s.getvalue())
                response['Content-Type'] = 'application/zip'
                response['Content-Disposition'] = 'attachment; filename='+zipname+'.zip'
                return response

    return HttpResponse("error", content_type="text/plain")

@login_required
def getAndUpdateFileObject(request):
    fileObj = None
    if request.method == "GET" and request.GET.get('id')!= None:
        id = request.GET.get('id')
        fileObj = get_object_or_404(Fi_file, pk=id)
        print(fileObj)
        data = {
            "id":fileObj.pk,
            "fileTypeName":fileObj.fileType.name,
            "fileName":fileObj.fileTypeName,
            "fileDescription":fileObj.fileDescription
            }
        return JsonResponse({"response":data})

    elif request.method == "POST":
        id = request.POST.get('id')
        fileObj = get_object_or_404(Fi_file, pk=id)
        if 'files' in request.FILES:
            form = Fi_fileFormEditWithFile(request.POST, request.FILES, instance=fileObj)
        else:
            form = Fi_fileFormEditWOFile(request.POST, instance=fileObj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Se ha actualizado correctamente el documento")
        else:
            messages.error(request, form.errors)
    return redirect(get_file_type_list)

def file_group_edit(request):

    if request.method == "POST":
        id = request.POST.get('id')
        obj = get_object_or_404(Fi_file_type, pk=id)
        form = Fi_file_typeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Se ha actualizado el grupo con éxito")
        else:
            messages.warning(request, form.errors)
    return redirect(file_create_new)