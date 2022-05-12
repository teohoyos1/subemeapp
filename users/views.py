from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, models #CREADOTEO
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm

from users.forms import CustomNewUserForm, ProfileForm
# Create your views here.

def signupUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {}
    if request.method == "POST":
        form = CustomNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Te has registrado correctamente {user.username}")
            return redirect("/")
    else:
        form = CustomNewUserForm()
    context={
        'form': form
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

@login_required
def profile_page(request):
    context={}
    if request.method == "GET":
        form = ProfileForm(instance=request.user)
        context={
            'form':form,
            'username': request.user.username
        }
        # userid = 0
        # if request.user is not None and isinstance(request.user.pk, int):
        #     userid = request.user.pk
        #     user = get_object_or_404(models.User, pk=userid)
        #     context={
        #         'userObj':user
        #     }
        # else:
            # redirect("/")
    return render(request, "profile/profile.html", context)


def profile_edit(request):
    context={}
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Información actualizada correctamente")
    else:
        form = ProfileForm(instance=request.user)
    context={
        'form': form,
        'username': request.user.username,
    }
    return render(request, "profile/profile.html", context)

