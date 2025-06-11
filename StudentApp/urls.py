
from django.urls import path
from StudentApp import views
urlpatterns = [
    path('login', views.login),
    path('Register', views.Register),
    path('RegAction', views.RegAction),
    path('LogAction', views.LogAction),
    path('StudentHome', views.StudentHome),
    path('viewfaculty', views.viewfaculty),
    path('sendreport', views.sendreport),
    path('SendReportAction', views.SendReportAction),
    path('viewMarks', views.viewMarks),
    path('ViewReview', views.ViewReview),
    path('viewnotification', views.viewnotification)
]
