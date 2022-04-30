from queue import Empty
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #CREADOTEO
from django.contrib import messages
import os
from .models import Fi_file_type
from .forms import Fi_file_typeForm

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

    typeObjFather = Fi_file_type.objects.all().order_by('id').filter(parentID=0).filter(name__contains=query)
    typeObjChild = Fi_file_type.objects.all().order_by('parentID').exclude(parentID=0).filter(name__contains=query)
    context = {
        'typeObjFather':typeObjFather,
        'typeObjChild': typeObjChild,
    }
    return render(request, 'fileList/fileList.html', context)

def about(request):
    return render(request, 'about.html')

#ADDPAGE - GROUP, TYPEFILE, FILE
@login_required
def redirect_to_new_file_page(request):
    try:
        objGroupSelect = Fi_file_type.objects.filter(parentID=0).filter(isActive=1)
    except:
        objGroupSelect = None

    context = {
        'objGroupSelect': objGroupSelect,
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
            obj = form.save()
            print(obj,'OBJETICO ')
            messages.success(request, f"Se ha guardado correctamente el grupo")
            return redirect('/add-file-page')
        else:
            print(form.errors)
            # messages.error(request, form.errors.get('message'))
    return redirect('/add-file-page')
