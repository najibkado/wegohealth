from sqlite3 import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main import models
from main.models import Drug, Questionaire, User
import csv
import os

from main.views import shop

# Create your views here.
#TODO: When approving a survey, you have to make all drugs approved to valid

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

        if request.user.is_admin:
            # surverys = len(models.Client.objects.all())
            approved = models.Drug.objects.filter(approved=True)
            requests = models.Drug.objects.filter(approved=False)
            agents = len(User.objects.filter(is_admin=False))
            admin = len(User.objects.filter(is_admin=True))

            approved_shops = set()
            requests_shops = set()

            for req in approved:
                if req.shop in approved_shops:
                    pass
                else:
                    if req.shop.agent.reg_by == request.user.pk:
                        approved_shops.add(req.shop)

            for req in requests:
                if req.shop in requests_shops:
                    pass
                else:
                    if req.shop.agent.reg_by == request.user.pk:
                        requests_shops.add(req.shop)

            sample = []
            labels = ["Kano","Jigawa", "Katsina", "Yobe", "Bauchi", "Gombe", "Adamawa", "Taraba", "Kaduna", "Zamfara"]

            for label in labels:
                c = models.Client.objects.filter(state=label)
                sample.append(len(c))

            return render(request, "dashboard/index.html", {
                "surveys": len(requests_shops),
                "approved": len(approved_shops),
                "requests": len(requests_shops),
                "agents": "null",
                "admin": "null",
                "sample": sample
            })

        surverys = len(models.Client.objects.all())
        approved = models.Drug.objects.filter(approved=True)
        requests = models.Drug.objects.filter(approved=False)
        agents = len(User.objects.filter(is_admin=False))
        admin = len(User.objects.filter(is_admin=True))

        approved_shops = set()
        requests_shops = set()

        for req in approved:
            if req.shop in approved_shops:
                pass
            else:
                approved_shops.add(req.shop)

        for req in requests:
            if req.shop in requests_shops:
                pass
            else:
                requests_shops.add(req.shop)

        sample = []
        labels = ["Kano","Jigawa", "Katsina", "Yobe", "Bauchi", "Gombe", "Adamawa", "Taraba", "Kaduna", "Zamfara"]

        for label in labels:
            c = models.Client.objects.filter(state=label)
            sample.append(len(c))

        return render(request, "dashboard/index.html", {
            "surveys": surverys,
            "approved": len(approved_shops),
            "requests": len(requests_shops),
            "agents": agents,
            "admin": admin,
            "sample": sample
        })

@login_required
def survey_requests(request):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))
   
    if request.method == "GET":
        
        shops = set()
        requests = []
        unrequests = models.Drug.objects.filter(approved=False, declined=False)

        for req in unrequests:
            if req.shop in shops:
                pass
            else:
                if req.shop.agent.reg_by == request.user.pk:
                    shops.add(req.shop)
                    requests.append(req)

        return render(request, "dashboard/requests.html", {
            "requests": requests
        })

@login_required
def review_requests(request, id):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":
        shop = models.Shop.objects.get(pk=id)
        personal_info = shop.kyc.client
        survey = models.Questionaire.objects.get(client=personal_info)
        drugs = models.Drug.objects.filter(shop=shop)
        kyc = models.Kyc.objects.filter(client=personal_info).last()

        return render(request, "dashboard/review.html", {
            "personal": personal_info,
            "survey": survey,
            "drugs": drugs,
            "kyc": kyc,
            "shop": shop
        })

    if request.method == "POST":
        shop = models.Shop.objects.get(pk=id)
        drugs = models.Drug.objects.filter(shop=shop)

        for drug in drugs:
            drug.approved = True
            drug.save()

        messages.success(request, "Approved Successfuly")
        return HttpResponseRedirect(reverse("survey_requests"))

@login_required
def decline_requests(request, id):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "POST":
        shop = models.Shop.objects.get(pk=id)
        drugs = models.Drug.objects.filter(shop=shop)

        for drug in drugs:
            drug.declined = True
            drug.save()

        messages.success(request, "Declined Successfuly")
        return HttpResponseRedirect(reverse("survey_requests"))

@login_required
def approved_preview(request, id):
    if not request.user.is_superuser:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":

        shop = models.Shop.objects.get(pk=id)
        personal_info = shop.kyc.client
        survey = models.Questionaire.objects.get(client=personal_info)
        drugs = models.Drug.objects.filter(shop=shop)
        kyc = models.Kyc.objects.filter(client=personal_info).last()

        return render(request, "dashboard/preview.html", {
            "personal": personal_info,
            "survey": survey,
            "drugs": drugs,
            "kyc": kyc,
            "shop": shop
        })

@login_required
def generate_csv(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))

        # file = open("data.csv", "w")
        header = [
            'Wego ID',
            'Customer Name',
            'Business Name',
            'Email',
            'Phone Number',
            'Address',
            'State',
            'Local Government',
            'Ward',
            'Gender',
            'Age',
            'Shop Latitude',
            'Shop Longitude',
            'Location URL',
            'Date Collected',
            'Do you have a bank account?',
            'Have you had access to loan for your business?',
            'Do you need financial support in form of loan for your business?',
            'What is the maximum amount that you be able to collect as loan for your business?',
            'Years of experience in business?',
            'Years in present shop?',
            'Are you the business owner?',
            'Expected time of delivery when you place order for drugs on our app?',
            'How much would you be able to pay for delivery after placing order for drugs on our app?',
            'How often do you visit the market in a month to buy drugs for your business?',
            'What are your major challenges in this business?',
            'How much credit worth of drugs do you give out to your customers in a monthly?',
            'Do debtors slow down your business turn over?',
            'What Services are you interested in from our app?',
            'What is your qualification?',
            'How many employees do you have currently?',
            'What is your turnover in the last 12 months?',
            'What are your typical monthly sales?',
            'Is your company registered with the Corporate Affairs Commission?',
            'Is your business registered with the Pharmacists Council of Nigeria?',
            'Date Collected',
            'Collected By',
            'Agent Name',
            'drugs',
            'quantity',
            ]
        row = []

        shops = set()
        drugs = models.Drug.objects.filter(approved=True)

        res = HttpResponse( content_type='text/csv')
        res ['Content-Disposition'] = 'attachment; filename=' + 'data.csv'

        writer = csv.writer(res)
        writer.writerow(header)

        rows = []

        for drug in drugs:
            if drug.shop in shops:
                pass

            shops.add(drug.shop)

        for shop in shops:
            row = []
            row.append(shop.wego_id)
            row.append(shop.kyc.client.name)
            row.append(shop.kyc.client.business_name)
            row.append(shop.kyc.client.email)
            row.append(shop.kyc.client.phone)
            row.append(shop.kyc.client.address)
            row.append(shop.kyc.client.state)
            row.append(shop.kyc.client.lga)
            row.append(shop.kyc.client.ward)
            row.append(shop.kyc.client.gender)
            row.append(shop.kyc.client.age)
            row.append(shop.kyc.client.lat)
            row.append(shop.kyc.client.lon)
            row.append(shop.kyc.client.url)
            row.append(shop.kyc.client.date)

            qstn = Questionaire.objects.get(client=shop.kyc.client)

            row.append(qstn.have_account)
            row.append(qstn.loan_access)
            row.append(qstn.financial_support)
            row.append(qstn.max_loan)
            row.append(qstn.business_experience)
            row.append(qstn.shop_experience)
            row.append(qstn.is_business_owner)
            row.append(qstn.duration)
            row.append(qstn.delivery)
            row.append(qstn.commute)
            row.append(qstn.challenges)
            row.append(qstn.credit)
            row.append(qstn.debtors)
            row.append(qstn.service)
            row.append(qstn.qualification)
            row.append(qstn.employees)
            row.append(qstn.turnover)
            row.append(qstn.sales)
            row.append(qstn.cac)
            row.append(qstn.council)
            row.append(qstn.date)

            row.append(shop.agent.username)
            row.append(f"{shop.agent.first_name} {shop.agent.last_name}")

            drugs = Drug.objects.filter(shop=shop)

            for d in drugs:
                dr = []
                qt = []

                dr.append(d.drug)
                qt.append(str(d.quantity))

                f_dr = "-".join(dr)
                f_qt = "-".join(qt)

                row.append(f_dr)
                row.append(f_qt)


            rows.append(row)

        for r in rows:

            writer.writerow(r)
        
        return res
        


@login_required
def all(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))
        

        all = []
        shops = set()
        unrequests = models.Drug.objects.all()

        for req in unrequests:
            if req.shop in shops:
                pass
            else:
                shops.add(req.shop)
                all.append(req)

        return render(request, "dashboard/all.html", {
            "all": all
        })

@login_required
def approved(request):
    if request.method == "GET":

        if not request.user.is_superuser:
            messages.error(request, "You have no access to this portal!")
            return HttpResponseRedirect(reverse("dashboard_login"))

        shops = set()
        approved = []
        unrequests = models.Drug.objects.filter(approved=True)

        for req in unrequests:
            if req.shop in shops:
                pass
            else:
                shops.add(req.shop)
                approved.append(req)
        
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
        return render(request, "dashboard/del_confirm.html", {
            "agent": agents
        })

    if request.method == "POST":
        agents = User.objects.get(pk=id)
        agents.delete()
        messages.success(request, "Successfully deleted")
        return HttpResponseRedirect(reverse("agents"))

@login_required
def jobs(request, id):
    if request.user.is_superuser or request.user.is_admin:
        pass
    else:
        messages.error(request, "You have no access to this portal!")
        return HttpResponseRedirect(reverse("dashboard_login"))

    if request.method == "GET":
        agent = User.objects.get(pk=id)
        shops = models.Shop.objects.filter(agent=agent)
        
        requests = set()
        approved = set()
        declined = set()

        for shop in shops:
            drugs = models.Drug.objects.filter(shop=shop)

            if not drugs:
                pass

            if drugs[0].approved:
                approved.add(shop)

            if drugs[0].declined:
                declined.add(shop)

            requests.add(shop)
                


        return render(request, "dashboard/jobs.html", {
            "agent": agent,
            "requests": requests,
            "approved": approved,
            "declined": declined,
            "req_count": len(requests),
            "app_count": len(approved),
            "dec_count": len(declined)
        })

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
        phone = request.POST["phone"]
        password = request.POST["password"]

        try:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                phone=phone,
                reg_by=request.user.pk
            )

            new_user.save()
        except IntegrityError:
            messages.error(request, "Pls provide all required data!")
            return HttpResponseRedirect(reverse("new_agent"))

        messages.success(request, "Successfull!")
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
        phone = request.POST["phone"]
        password = request.POST["password"]

        try:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_admin=True,
                phone=phone
            )

            new_user.save()
        except IntegrityError:
            messages.error(request, "Pls provide all required data!")
            return HttpResponseRedirect(reverse("new_admin"))

        messages.success(request, "Successfull!")
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
