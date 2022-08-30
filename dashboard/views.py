from sqlite3 import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main import models
from main.models import User

# Create your views here.

def login_view(request):

    if request.method == "GET":

        if request.user.is_authenticated:
            logout(request)

        return render(request, "dashboard/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user == None:
            #An error message here
            messages.error(request, "Invalid user credentials")
            return HttpResponseRedirect(reverse("dashboard_login"))

        if user.is_superuser or user.is_admin:
            login(request, user=user)
            return HttpResponseRedirect(reverse("dashboard_index"))

        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

@login_required
def dashboard_index(request):

    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":

        surverys = len(models.Client.objects.all())
        approved = len(models.Drug.objects.filter(approved=True))
        requests = len(models.Drug.objects.filter(approved=False))
        agents = len(User.objects.filter(is_superuser=False))
        admin = len(User.objects.filter(is_superuser=True))

        return render(request, "dashboard/index.html", {
            "surveys": surverys,
            "approved": approved,
            "requests": requests,
            "agents": agents,
            "admin": admin
        })

@login_required
def survey_requests(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        requests = models.Drug.objects.filter(approved=False)
        return render(request, "dashboard/requests.html", {
            "requests": requests
        })


@login_required
def all(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        all = models.Drug.objects.all()
        return render(request, "dashboard/all.html", {
            "all": all
        })

@login_required
def approved(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        approved = models.Drug.objects.filter(approved=True)
        return render(request, "dashboard/approved.html", {
            "approved": approved
        })

@login_required
def agents(request):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET": 
        agents = User.objects.filter(is_admin=False, is_superuser=False)
        return render(request, "dashboard/agents.html", {
            "agents": agents
        })

@login_required
def del_agent(request, id):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":
        agents = User.objects.get(pk=id)
        agents.delete()
        messages.success(request, "Successfully deleted")
        return HttpResponseRedirect(reverse("agents"))


@login_required
def new_agent(request):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":
        return render(request, "dashboard/new_agent.html")

    if request.method == "POST":
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )

            new_user.save()
        except IntegrityError:
            return HttpResponse("Pls provide all required data")

        return render(request, "dashboard/new_agent.html", {
            "success": True,
            "username":new_user.username,
            "password":password
        })

@login_required
def new_admin(request):

    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":
        return render(request, "dashboard/new_admin.html")

    if request.method == "POST":
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_admin=True
            )

            new_user.save()
        except IntegrityError:
            return HttpResponse("Pls provide all required data")

        return render(request, "dashboard/new_admin.html", {
            "success": True,
            "username":new_user.username,
            "password":password
        })


@login_required
def administrators(request):

    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":
        administrators = User.objects.filter(is_admin=True)
        return render(request, "dashboard/administrators.html", {
            "administrators": administrators
        })
