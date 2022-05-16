from ast import Not
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, models #CREADOTEO
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist

from users.forms import CustomNewUserForm, ProfileForm, PersonForm
# Create your views here.

def signupUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {}
    if request.method == "POST":
        form = CustomNewUserForm(request.POST)
        form_person = PersonForm(request.POST)
        if form.is_valid() and form_person.is_valid():
            user = form.save()
            form_person = form_person.save(commit=False)
            form_person.user = user
            form_person.save()
            login(request, user)
            messages.success(request, f"Te has registrado correctamente {user.username}")
            return redirect("/")
    else:
        form = CustomNewUserForm()
        form_person = PersonForm()
    context={
        'form': form,
        'form_person':form_person
    }
    return render(request, "registration/signup.html", context)

def get_robot_file(request):
    return render(request, 'robots.txt',content_type='text/plain')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Has iniciado sesión {username}.")
                return redirect("/")
    else:
        form = AuthenticationForm()
    context={
        "login_form": form
    }
    return render(request, template_name="registration/login.html", context=context)

def logout_request(request):
    logout(request)
    messages.success(request, f"Has cerrado sesión con éxito")
    return render(request, 'home.html')

def profile_edit(request):
    context={}
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        try:
            form_person = PersonForm(request.POST, instance=request.user.person)
        except ObjectDoesNotExist:
            form_person = PersonForm(request.POST)

        if form.is_valid() and form_person.is_valid():
            user = form.save()
            form_person = form_person.save(commit=False)
            form_person.user = user
            form_person.save()
            messages.success(request, "Información actualizada correctamente")
            return redirect(profile_edit)
    else:
        form = ProfileForm(instance=request.user)
        try:
            form_person = PersonForm(instance=request.user.person)
        except ObjectDoesNotExist:
            form_person = PersonForm()
    context={
        'form': form,
        'form_person': form_person,
        'username': request.user.username
    }
    return render(request, "profile/profile.html", context)

