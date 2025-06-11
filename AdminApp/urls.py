
from django.urls import path
from AdminApp import views
urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('LogAction', views.LogAction),
    path('AdminHome', views.AdminHome),
    path('AddDept', views.AddDept),
    path('DeptAction', views.DeptAction),
    path('AddFaculty', views.AddFaculty),
    path('AddFacultyAction', views.AddFacultyAction),
    path('ViewFaculty', views.ViewFaculty),
    path('DeleteFaculty', views.DeleteFaculty),
    path('AssignProject', views.AssignProject),
    path('ConfirmAction', views.ConfirmAction),
    path('ViewReports', views.ViewReports),
    path('ViewReview', views.ViewReview),
    path('ViewNotification', views.ViewNotification),
    path('UpdateFaculty', views.UpdateFaculty),
    path('UpdateFacultyAction', views.UpdateFacultyAction),
]
