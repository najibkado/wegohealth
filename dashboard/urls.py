from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.login_view, name="dashboard_login"),
    path('index', views.dashboard_index, name="dashboard_index"),
    path('requests', views.survey_requests, name="survey_requests"),
    path('myrequests', views.my_requests, name="my_requests"),
    path('myapproved', views.my_approved, name="my_approved"),
    path('mydeclined', views.my_declined, name="my_declined"),
    path('requests/review/<int:id>', views.review_requests, name="review_requests"),
    path('requests/decline/<int:id>', views.decline_requests, name="decline_requests"),
    path('approved', views.approved, name="dashboard_approved"),
    path('approved/preview/<int:id>', views.approved_preview, name="preview"),
    path('all', views.all, name="dashboard_all"),
    path('agents', views.agents, name="agents"),
    path('agents/new', views.new_agent, name="new_agent"),
    path('user/del/<int:id>', views.del_agent, name="del_agent"),
    path('user/jobs/<int:id>', views.jobs, name="jobs"),
    path('administrators', views.administrators, name="administrators"),
    path('administrators/new', views.new_admin, name="new_admin"),
    path('export', views.generate_csv, name="csv")
]

