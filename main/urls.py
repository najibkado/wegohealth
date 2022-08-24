from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('client', views.client_info, name="client"),
    path('questianaire/<int:id>', views.client_business, name="questianaire"),
    path('kyc/<int:id>', views.client_kyc, name="kyc"),
    path('drugs', views.drugs, name="drugs"),
    path('reg', views.reg, name="reg"),
    path('shop/<int:pk>', views.shop, name="shop")
]