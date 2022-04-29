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
    msg = {}
    if request.method == "POST":
        form = CustomNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            msg = {
                "message":f"Te has registrado correctamente {user.username}",
                "tag" : "success"
            }
            context={
                'form': form,
                'messages': msg
            }
            return render(request, 'home.html', context)
    else:
            # msg = {
            #     "message":"Registro incorrecto, intentalo de nuevo",
            #     "tag" : "danger"
            # }
        form = CustomNewUserForm()
    context={
        'form': form,
        'messages': msg
    }
    return render(request, "registration/signup.html", context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {}
    msg={}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                msg = {
                    "message": f"Has iniciado sesión {username}.",
                    "tag": "success"
                }
                context = {
                    "messages": msg
                }
                return redirect("/", context)
    else:
        form = AuthenticationForm()
    context={
        "login_form": form
    }
    return render(request=request, template_name="registration/login.html", context=context)

def logout_request(request):
	logout(request)
	messages.success(request, "Has cerrado sesión con éxito")
	return redirect("/")

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
    msg={}
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = {
                "message":"Información actualizada correctamente",
                "tag" : "success"
            }
    else:
        form = ProfileForm(instance=request.user)
    context={
        'form': form,
        'username': request.user.username,
        'messages': msg
    }
    return render(request, "profile/profile.html", context)

