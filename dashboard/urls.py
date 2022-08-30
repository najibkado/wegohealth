from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name="dashboard_login"),
    path('index', views.dashboard_index, name="dashboard_index"),
    path('requests', views.survey_requests, name="survey_requests"),
    path('approved', views.approved, name="dashboard_approved"),
    path('all', views.all, name="dashboard_all"),
    path('agents', views.agents, name="agents"),
    path('agents/new', views.new_agent, name="new_agent"),
    path('user/del/<int:id>', views.del_agent, name="del_agent"),
    path('administrators', views.administrators, name="administrators"),
    path('administrators/new', views.new_admin, name="new_admin")
]