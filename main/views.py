import imp
from sqlite3 import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def login(request):
    if request.method == "GET":
        return render(request, "main/login.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        return HttpResponseRedirect(reverse("client"))

# Needs auth
def client_info(request):
    if request.method == "GET":
        return render(request, "main/client-info.html")

    if request.method == "POST":
        name = request.POST["name"]
        business_name = request.POST["business-name"]
        email = request.POST["email-address"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        gender = request.POST["gender"]
        age = request.POST["age"]

        try:
            client = models.Client(
                name = name,
                business_name = business_name,
                email = email,
                phone = phone,
                address = address,
                gender = gender,
                age = age
            )

            client.save()
        except IntegrityError:
            return HttpResponse("Unable to register client at the moment!")

        return HttpResponseRedirect(reverse("questianaire", args=(client.pk,)))
#Questionaire
def client_business(request, id):
    
    if request.method == "GET":
        return render(request, "main/biz-info.html", {
            "id": id
        })

    if request.method == "POST":
        return HttpResponse("Sup Sup Bro, What you looking for?")

def drugs(request):

    if request.method == "GET":
        return render(request, "main/selection.html")

    if request.method == "POST":
        name = request.POST["name"]
        addr = request.POST["addr"]
        drug = request.POST.getlist('test')

        if name == "" or addr == "" or len(drug) == 0:
            return HttpResponse("Can't submit empty fields")

        shop = models.Shop.objects.create(
            name = name,
            addr = addr
        )
        shop.save()

        for d in drug:
            new_d = models.Drug.objects.create(
                shop = shop,
                drug = d
            )
            new_d.save()
        
        return HttpResponseRedirect(reverse("drugs"))

def reg(request):
    shops = models.Shop.objects.all()
    return render(request, "main/registered.html", {
        "shops": shops
    })

def shop(request, pk):
    sho = models.Shop.objects.get(pk=pk)
    drugs = models.Drug.objects.filter(shop=sho)
    return render(request, "main/shop.html", {
        "shop": sho,
        "drugs": drugs
    })