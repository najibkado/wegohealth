from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('client', views.client_info, name="client"),
    path('questianaire/<int:id>', views.client_business, name="questianaire"),
    path('kyc/<int:id>', views.client_kyc, name="kyc"),
    path('drugs/<int:id>', views.drugs, name="drugs"),
    path('quantity/<int:id>', views.quantity, name="quantity"),
    path('reg', views.reg, name="reg"),
    path('shop/<int:pk>', views.shop, name="shop"),
    path('success', views.success, name="success"),
    path('error', views.error, name="error"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('coming', views.coiming, name="coming"),
    path('solutions', views.solutions, name="solutions"),
    path('logout', views.logout_view, name="logout")
]