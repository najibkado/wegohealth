import imp
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

        return HttpResponseRedirect(reverse("drugs"))

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