from django.shortcuts import render
from DBConnection.Database import getOneRecord
from DBConnection.Database import getAllRecords
from DBConnection.Database import insertMethod
import pymysql
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request,'FacultyApp/Login.html')

def EmpLogAction(request):
    empid=request.POST['empid']

    data=getOneRecord("select * from faculty where fid='"+empid+"'")
    if data is not None:
        request.session['empid']=empid
        return render(request, 'FacultyApp/FacultyHome.html')
    else:
        context={'data':'Login Failed..!!'}
        return render(request, 'FacultyApp/Login.html', context)

def FacultyHome(request):
    return render(request, 'FacultyApp/FacultyHome.html')

def viewassigned(request):
    empid=request.session['empid']

    data=getAllRecords("select * from student where fid='"+empid+"'")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Project Title</th><th>Department</th><th>Student Name</th><th>Roll Number</th><th>Email</th>" \
            "</tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[3])+"</td><td>"+str(i[1])+"</td><td>"+str(i[4])+"</td><td>"+str(i[2])+"</td>" \
                "<td>"+str(i[5])+"</td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'FacultyApp/ViewAssign.html', context)

def studentreport(request):
    empid=request.session['empid']

    data=getAllRecords("select * from post_review where f_id='"+empid+"'")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Student Rollno</th><th>Department</th><th>Title</th><th>Review</th><th>Marks</th><th>Date</th>" \
            "<th>View PDF</th><th>Assign Marks</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[5])+"</td>" \
                "<td>"+str(i[8])+"</td><td>"+str(i[7])+"</td><td><a href='/faculty/ViewReview?r_id="+str(i[0])+"'>View Review </a></td>" \
                "<td><a href='/faculty/Marks?r_id="+str(i[0])+"'>Give Marks </a></td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'FacultyApp/ViewReview.html', context)
def ViewReview(request):
    r_id=request.GET['r_id']
    con=pymysql.connect(host="localhost",user="root",password="",database="project_monitor")
    cur=con.cursor()
    cur.execute("select review_pdf from post_review where id='"+r_id+"'")
    file=cur.fetchone()[0]
    cur.close()

    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Resume.pdf"'
    return response
def Marks(request):
    id= request.GET['r_id']
    context={'id':id}
    return render(request,'FacultyApp/AssignMarks.html', context)
def AssignAction(request):
    id=request.POST['id']
    mark=request.POST['marks']
    i=insertMethod("update post_review set marks='"+mark+"' where id='"+id+"'")
    empid=request.session['empid']

    data=getAllRecords("select * from post_review where f_id='"+empid+"'")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Student Rollno</th><th>Department</th><th>Title</th><th>Review</th><th>Marks</th><th>Date</th>" \
            "<th>View PDF</th><th>Assign Marks</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[5])+"</td>" \
                "<td>"+str(i[8])+"</td><td>"+str(i[7])+"</td><td><a href='/faculty/ViewReview?r_id="+str(i[0])+"'>View Review </a></td>" \
                "<td><a href='/faculty/Marks?r_id="+str(i[0])+"'>Give Marks </a></td></tr></tbody>"

    context={'data': strdata,'msg':'Marks Assigned Successfully...!!'}
    return render(request,'FacultyApp/ViewReview.html', context)

def notification(request):
     empid=request.session['empid']
     fid=str(empid)
     data=getOneRecord("select * from student where fid='"+fid+"'")
     title=data[3]
     context={'data': title}
     return render(request,'FacultyApp/SendNotification.html', context)

def NotifyAction(request):
    empid=request.session['empid']
    fid=str(empid)
    title=request.POST['title']
    notify=request.POST['notify']

    insertMethod("insert into notification values(null,'"+fid+"','"+title+"','"+notify+"',now())")
    context={'msg': "Notification Successfully Submitted...!!!"}
    return render(request,'FacultyApp/SendNotification.html', context)




