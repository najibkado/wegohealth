from audioop import add
from sqlite3 import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def login_view(request):
    if request.method == "GET":
        return render(request, "main/login.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return HttpResponseRedirect(reverse("client"))

        return HttpResponse("User not registered") 

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Needs auth
@login_required
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
        state = request.POST["state"]
        lga = request.POST["lga"]
        ward = request.POST["ward"]

        if name == "" or business_name == "" or email == "" or phone == "" or address == "" or gender == "" or age == "" or state == "" or lga == "" or ward == "":
            messages.error(request, "Fields can't be empty!")
            return HttpResponseRedirect(reverse("client"))

        try:
            client = models.Client(
                name = name,
                business_name = business_name,
                email = email,
                phone = phone,
                address = address,
                gender = gender,
                age = age,
                state = state,
                lga = lga,
                ward = ward
            )

            client.save()
        except IntegrityError:
            messages.error(request, "Invalid form data!")
            return HttpResponseRedirect(reverse("client"))

        return HttpResponseRedirect(reverse("questianaire", args=(client.pk,)))
#Questionaire
@login_required
def client_business(request, id):
    
    if request.method == "GET":
        return render(request, "main/biz-info.html", {
            "id": id
        })

    if request.method == "POST":
        account = request.POST["account"]
        loan = request.POST["loan"]
        support = request.POST["support"]
        amount = request.POST["amount"]
        busines_experience = request.POST["busines-experience"]
        shop_experience = request.POST["shop-experience"]
        business_owner = request.POST["busines"]
        duration = request.POST.get("duration")
        delivery = request.POST.get("delivery")
        commute = request.POST.get("commute")
        challenges = request.POST.getlist("challenges")
        credit = request.POST.get("credit")
        debtors = request.POST["debtors"]
        service = request.POST.getlist("service")
        qualification = request.POST["qualification"]
        employees = request.POST.get("employees")
        turnover = request.POST.get("turnover")
        sales = request.POST.get("sales")
        cac = request.POST["cac"]
        council = request.POST["council"]
        # "-".join(challenges)

        if account == "" or loan == "" or support == "" or amount == "" or busines_experience == "" or shop_experience == "" or business_owner == "" or duration == "" or delivery == "" or commute == "" or challenges == "" or credit == "" or debtors == "" or service == "" or qualification == "" or employees == "" or turnover == "" or sales == "" or cac == "" or council == "":
            messages.error(request, "Fields can't be empty!")
            return HttpResponseRedirect(reverse("questianaire", args=(id, )))

        try:
            c = models.Client.objects.get(pk=id)
        except models.Client.DoesNotExist:
            return HttpResponseRedirect(reverse("client"))

        try:
            q = models.Questionaire.objects.get(client=c)
            return HttpResponseRedirect(reverse("kyc", args=(q.pk,)))
        except models.Questionaire.DoesNotExist:
            pass

        try:
            new_questionaire = models.Questionaire(
                client = c,
                have_account = True if account == "yes" else False,
                loan_access = True if loan == "yes" else False,
                financial_support = True if support == "yes" else False,
                max_loan = amount,
                business_experience = busines_experience,
                shop_experience = shop_experience,
                is_business_owner = True if business_owner == "yes" else False,
                duration = duration,
                delivery = delivery,
                commute = commute,
                challenges = "-".join(challenges),
                credit = credit,
                debtors = debtors,
                service = "-".join(service),
                qualification = qualification,
                employees = employees,
                turnover = turnover,
                sales = sales,
                cac = True if cac == "yes" else False,
                council = True if council == "yes" else False 
            )

            new_questionaire.save()

        except IntegrityError:
            messages.error(request, "Unable to finish data submission pls try again")
            return HttpResponseRedirect(reverse("questianaire", args=(id, )))

        return HttpResponseRedirect(reverse("kyc", args=(new_questionaire.pk,)))

@login_required
def client_kyc(request, id):

    if request.method == "GET":
        return render(request, "main/kyc.html", {
            "id":id
        })

    if request.method == "POST":
        passport = request.FILES.get('passport')
        inner = request.FILES.get('inner')
        outter = request.FILES.get('outter')

        try:
            client = models.Questionaire.objects.get(pk=id).client
        except models.Questionaire.DoesNotExist:
            return HttpResponseRedirect(reverse("client"))

        try:
            k = models.Kyc.objects.get(client=client)
            return HttpResponseRedirect(reverse("drugs", args=(k.pk,)))
        except models.Kyc.DoesNotExist:
            pass

        try:

            # client = models.ForeignKey(Client, on_delete=models.CASCADE)
            # passport_name = models.CharField(max_length=50)
            # outter_name = models.CharField(max_length=50)
            # inner_name = models.CharField(max_length=50)
            # client_Passport_Img = models.ImageField(upload_to='images/')
            # client_Outter_Img = models.ImageField(upload_to='images/')
            # client_Inner_Img = models.ImageField(upload_to='images/')


            kyc = models.Kyc(
                client = client,
                passport_name = client.business_name + " Passport",
                outter_name = client.business_name + " Outter shop",
                inner_name = client.business_name + " Inner shop",
                client_Passport_Img = passport,
                client_Outter_Img = outter,
                client_Inner_Img = inner
            )

            kyc.save()
        except IntegrityError:
            messages.error(request, "Unable to upload pictures, Try again")
            return HttpResponseRedirect(reverse("kyc", args=(id,)))

        return HttpResponseRedirect(reverse("drugs", args=(kyc.pk,)))

@login_required
def drugs(request, id):

    if request.method == "GET":
        return render(request, "main/selection.html", {
            "id": id
        })

    if request.method == "POST":
        # name = request.POST["name"]
        # addr = request.POST["addr"]
        drug = request.POST.getlist('test')

        # if name == "" or addr == "" or len(drug) == 0:
        #     return HttpResponse("Can't submit empty fields")

        if len(drug) <= 0:
            messages.error(request, "Please select drugs")
            return HttpResponseRedirect(reverse("drugs", args=(id,)))

        kyc = models.Kyc.objects.get(pk=id)

        shop = models.Shop.objects.create(
            agent = request.user,
            kyc = kyc,
            wego_id = f"WGH-SURV-{kyc.client.pk}",
            name = kyc.client.name,
            addr = kyc.client.address
        )
        shop.save()

        for d in drug:
            new_d = models.Drug.objects.create(
                shop = shop,
                quantity = 1,
                drug = d
            )
            new_d.save()
        
        return HttpResponseRedirect(reverse("quantity", args=(shop.pk,)))

@login_required
def quantity(request, id):
    if request.method == "GET":
        shop = models.Shop.objects.get(pk=id)
        drugs = models.Drug.objects.filter(shop=shop)

        fin_drugs = []
        count = len(drugs)

        for drug in drugs:
            item = {
                "drug": drug.drug,
                "name": "form" + str(count)
            }

            fin_drugs.append(item)
            count-=1

        return render(request, "main/quantity.html", {
            "id": id,
            "drugs": fin_drugs
        })

    if request.method == "POST":
        shop = models.Shop.objects.get(pk=id)
        drugs = models.Drug.objects.filter(shop=shop)
        count = len(drugs) + 1
        quantities = []
        indexes = 0
        for i in range(1, count):
            item = request.POST["form" + str(i)]
            quantities.append(item)

        quantities.reverse()

        for drug in drugs:
            drug.quantity = int(quantities[indexes])
            drug.save()
            indexes+=1

        return HttpResponseRedirect(reverse("location", args=(id, )))

@login_required
def location(request, id):
    if request.method == "GET":
        return render(request, "main/location.html", {
            "id": id
        })

    if request.method == "POST":
        lon = request.POST["lon"]
        lat = request.POST["lat"]
        url = request.POST["url"]

        shop = models.Shop.objects.get(pk=id)

        shop.lon = lon
        shop.lat = lat
        shop.url = url

        shop.save()

        return HttpResponseRedirect(reverse("success"))

        
@login_required
def success(request):
    return render(request, "main/success.html")

def error(request):
    return render(request, "main/error.html")

def about(request):
    return render(request, "main/about.html")

def contact(request):
    return render(request, "main/contact.html")

def coiming(request):
    return render(request, "main/coming.html")

def solutions(request):
    return render(request, "main/solutions.html")

@login_required
def reg(request):
    shops = models.Shop.objects.all()
    return render(request, "main/registered.html", {
        "shops": shops
    })

@login_required
def shop(request, pk):
    sho = models.Shop.objects.get(pk=pk)
    drugs = models.Drug.objects.filter(shop=sho)
    return render(request, "main/shop.html", {
        "shop": sho,
        "drugs": drugs
    })
