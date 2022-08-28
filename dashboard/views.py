from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main import models
from django.contrib.auth.models import User

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

        if user.is_superuser:
            login(request, user=user)
            return HttpResponseRedirect(reverse("dashboard_index"))

        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

@login_required
def dashboard_index(request):

    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))

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
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        agents = User.objects.filter(is_superuser=False)
        return render(request, "dashboard/agents.html", {
            "agents": agents
        })

@login_required
def new_agent(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        return render(request, "dashboard/new_agent.html")

@login_required
def new_admin(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        return render(request, "dashboard/new_admin.html")


@login_required
def administrators(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        
        administrators = User.objects.filter(is_superuser=True)
        return render(request, "dashboard/administrators.html", {
            "administrators": administrators
        })
