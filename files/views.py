from multiprocessing import context
import os
from django.shortcuts import render, redirect
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


from .models import Fi_file, Fi_file_type
from .forms import Fi_file_typeForm, Fi_fileForm

def index(request):
    SECRET_KEYj = os.getenv("ENVIRONMENT_MODE")
    print(SECRET_KEYj)
    return render(request, 'home.html', {'envi': SECRET_KEYj})

@login_required
def get_file_type_list(request):

    query=""
    filesParent = None
    try:
        if any(request.GET):
            query = request.GET.get('qr')
    except:
        query=""

    typeObjFather = Fi_file_type.objects.all().order_by('id').filter(name__contains=query)
    if typeObjFather.exists():
        filesParent = Fi_file.objects.all().order_by('fileType_id')
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
        objGroupSelect = Fi_file_type.objects.filter(isActive=1)
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
            return redirect('/add-file-page')
        else:
            print(form.errors)
            # messages.error(request, form.errors.get('message'))
    return redirect('/add-file-page')

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