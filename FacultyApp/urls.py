
from django.urls import path
from FacultyApp import views
urlpatterns = [
    path('login', views.login),
    path('EmpLogAction',views.EmpLogAction),
    path('FacultyHome', views.FacultyHome),
    path('viewassigned', views.viewassigned),
    path('studentreport', views.studentreport),
    path('ViewReview', views.ViewReview),
    path('Marks', views.Marks),
    path('AssignAction', views.AssignAction),
    path('notification', views.notification),
    path('NotifyAction',views.NotifyAction)



]
