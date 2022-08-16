from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('drugs', views.drugs, name="drugs"),
    path('reg', views.reg, name="reg"),
    path('shop/<int:pk>', views.shop, name="shop")
]