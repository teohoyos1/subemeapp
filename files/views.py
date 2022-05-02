from multiprocessing import context
from queue import Empty
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required #CREADOTEO
from django.contrib import messages
import os
from .models import Fi_file, Fi_file_type
from .forms import Fi_file_typeForm, Fi_fileForm

def index(request):
    SECRET_KEYj = os.getenv("ENVIRONMENT_MODE")
    print(SECRET_KEYj)
    return render(request, 'home.html', {'envi': SECRET_KEYj})

@login_required
def get_file_type_list(request):

    query=""
    try:
        if any(request.GET):
            query = request.GET.get('qr')
    except:
        query=""

    typeObjFather = Fi_file_type.objects.all().order_by('id').filter(name__contains=query)
    filesParent = Fi_file.objects.all().order_by('fileType_id')
    # typeObjChild = Fi_file_type.objects.all().filter(name__contains=query)
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

def generateAllOnePdf(request):

    if request.is_ajax() and request.method == "POST":
        # number = request.POST.get('id')
        dataa = "Holi"
        return JsonResponse({'data': dataa})

    return JsonResponse({'error':"Errores mi papa"}, status_code=201)