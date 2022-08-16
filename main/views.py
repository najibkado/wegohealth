import imp
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def drugs(request):

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
        
        return HttpResponseRedirect(reverse("index"))

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