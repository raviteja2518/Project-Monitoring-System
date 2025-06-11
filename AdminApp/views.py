from django.shortcuts import render
from DBConnection.Database import insertMethod
from DBConnection.Database import getOneRecord
from DBConnection.Database import getAllRecords
import pymysql
import random
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'AdminApp/Login.html')

def LogAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']
    if uname == 'Admin' and pwd == 'Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        return render(request,'AdminApp/Login.html')

def AdminHome(request):
    return render(request,'AdminApp/AdminHome.html')

def AddDept(request):
    return render(request,'AdminApp/AddDepartment.html')

def DeptAction(request):
    dept=request.POST['dept']
    data=getOneRecord("select * from dept where name='"+dept+"'")
    if data is not None:
        context={'data':'Department Already Exist'}
        return render(request,'AdminApp/AddDepartment.html',context)
    else:
        i=insertMethod("insert into dept values(null,'"+dept+"')")
        if i>0:
            context={'data':'Department Added'}
            return render(request,'AdminApp/AddDepartment.html',context)
        else:
            context={'data':'Department Failed'}
            return render(request,'AdminApp/AddDepartment.html',context)


def AddFaculty(request):
    id=random.randint(1,99999)
    data=getAllRecords("select * from dept")
    strdata="<select class='form-control border-0 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
    for i in data:
        strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata,'id':id}
    return render(request,'AdminApp/AddFaculty.html',context)

def AddFacultyAction(request):
    fid=request.POST['fid']
    dept=request.POST['dept']
    name=request.POST['name']
    design=request.POST['designation']
    email=request.POST['email']
    mobile=request.POST['mobile']

    data=getOneRecord("select * from faculty where mobile='"+mobile+"' and dept='"+dept+"'")
    if data is not None:
        id=random.randint(1,99999)
        data=getAllRecords("select * from dept")
        strdata="<select class='form-control border-0 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
        for i in data:
            strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
        strdata+= "</select>"
        context={'data': strdata, 'id': id, 'msg': 'Faculty Already Exist'}
        return render(request,'AdminApp/AddFaculty.html',context)
    else:
        i=insertMethod("insert into faculty values(null,'"+fid+"','"+name+"','"+dept+"','"+email+"','"+design+"','"+mobile+"','waiting')")
        if i>0:
            id=random.randint(1,99999)
            data=getAllRecords("select * from dept")
            strdata="<select class='form-control border-0 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
            for i in data:
                strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
            strdata+= "</select>"
            context={'data': strdata, 'id': id, 'msg': 'Faculty Details Added'}
            return render(request,'AdminApp/AddFaculty.html',context)
        else:
            id=random.randint(1,99999)
            data=getAllRecords("select * from dept")
            strdata="<select class='form-control border-0 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
            for i in data:
                strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
            strdata+= "</select>"
            context={'data': strdata, 'id': id, 'msg': 'Faculty Details Adding Failed'}
            return render(request,'AdminApp/AddFaculty.html',context)

def ViewFaculty(request):
    data=getAllRecords("select * from faculty")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Faculty Name</th><th>Department</th><th>Email</th><th>Designation</th><th>Mobile</th>" \
            "<th>Delete</th> <th>Project Assign</th><th>Update</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[7]

        if status == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td><td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                    "<td><a href='AssignProject?f_id="+str(i[0])+"'><font color='red'>Assign Project</font></a></td>" \
                    "<td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td><td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                "<td>"+str(i[7])+"</td><td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"

    context={'data': strdata}
    return render(request, 'AdminApp/ViewFaculty.html', context)
def DeleteFaculty(request):
    id=request.GET["f_id"]
    i=insertMethod("delete from faculty where id='"+id+"'")
    if i>0:
        data=getAllRecords("select * from faculty")
        strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Faculty Name</th><th>Department</th><th>Email</th><th>Designation</th><th>Mobile</th>" \
            "<th>Delete</th> <th>Project Assign</th><th>Update</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[7]

        if status == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td><td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                    "<td><a href='AssignProject?f_id="+str(i[0])+"'><font color='red'>Assign Project</font></a></td>" \
                    "<td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td><td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                "<td>"+str(i[7])+"</td><td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"

        context={'data': strdata,'msg':'Faculty Deleted Successfully...!!'}
        return render(request,'AdminApp/ViewFaculty.html',context)
    else:
        data=getAllRecords("select * from faculty")
        strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Faculty Name</th><th>Department</th><th>Email</th><th>Designation</th><th>Mobile</th>" \
            "<th>Delete</th> <th>Project Assign</th><th>Update</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[7]

        if status == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td><td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                    "<td><a href='AssignProject?f_id="+str(i[0])+"'><font color='red'>Assign Project</font></a></td>" \
                    "<td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td><td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                "<td>"+str(i[7])+"</td><td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"

    context={'data': strdata, 'msg':'Faculty Deletion Failed...!!'}
    return render(request,'AdminApp/ViewFaculty.html',context)

def AssignProject(request):
    f_id=request.GET['f_id']
    data=getAllRecords("select distinct title from student where status='waiting'")
    strdata="<select class='form-control border-0 py-3 px-4' name='title'  style='height: 50px;' required=''> <option selected></option>"
    for i in data:
        strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata,'id':id}

    context={'data': strdata, 'f_id':f_id }
    return render(request,'AdminApp/AssignFaculty.html',context)

def ConfirmAction(request):
    f_id=request.POST['f_id']
    title=request.POST['title']
    i=insertMethod("update student set fid='"+f_id+"',status='Assigned' where title='"+title+"'")
    i=insertMethod("update faculty set status='Assigned' where id='"+f_id+"'")
    data=getAllRecords("select * from faculty")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Faculty Name</th><th>Department</th><th>Email</th><th>Designation</th><th>Mobile</th>" \
            "<th>Delete</th> <th>Project Assign</th><th>Update</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[7]

        if status == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td>" \
                 "<td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                    "<td><a href='AssignProject?f_id="+str(i[1])+"'><font color='red'>Assign Project</font></a></td>" \
                    "<td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td>" \
                "<td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                "<td>"+str(i[7])+"</td><td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"
    context={'data': strdata, 'f_id':f_id,'msg':'Assigned Successfully..!!'}
    return render(request,'AdminApp/ViewFaculty.html',context)


def ViewReports(request):
    data=getAllRecords("select * from post_review")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Student Rollno</th><th>Faculty ID</th><th>Department</th><th>Title</th><th>Review</th><th>Marks</th><th>Review Submitted Date</th>" \
            "<th>View PDF</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[4])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[5])+"</td>" \
                "<td>"+str(i[8])+"</td><td>"+str(i[7])+"</td><td><a href='/ViewReview?r_id="+str(i[0])+"'>View Review </a></td>" \
                "</tr></tbody>"
    context={'data': strdata}
    return render(request, 'AdminApp/ViewReview.html', context)
def ViewReview(request):
    r_id=request.GET['r_id']
    con=pymysql.connect(host="localhost",user="root",password='',database="project_monitor")
    cur=con.cursor()
    cur.execute("select review_pdf from post_review where id='"+r_id+"'")
    file=cur.fetchone()[0]
    cur.close()

    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Resume.pdf"'
    return response
def ViewNotification(request):
    data=getAllRecords("select * from notification")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Title</th><th>Notification</th><th>date</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td>" \
                "</tr></tbody>"
    context={'data': strdata}
    return render(request, 'AdminApp/ViewNotification.html', context)

def UpdateFaculty(request):
    f_id=request.GET['f_id']
    context={'fid':f_id}
    return render(request,'AdminApp/UpdateFaculty.html', context)
def UpdateFacultyAction(request):
    fid=request.POST['fid']
    name=request.POST['name']
    design=request.POST['designation']
    email=request.POST['email']
    mobile=request.POST['mobile']

    insertMethod("update faculty set name='"+name+"',email='"+email+"',designation='"+design+"',mobile='"+mobile+"' where fid='"+fid+"'")
    data=getAllRecords("select * from faculty")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:600px'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Faculty Name</th><th>Department</th><th>Email</th><th>Designation</th><th>Mobile</th>" \
            "<th>Delete</th> <th>Project Assign</th><th>Update</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[7]

        if status == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td>" \
                 "<td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                    "<td><a href='AssignProject?f_id="+str(i[1])+"'><font color='red'>Assign Project</font></a></td>" \
                    "<td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td>"+str(i[6])+"</td>" \
                "<td><a href='DeleteFaculty?f_id="+str(i[0])+"'><font color='red'>Delete</font></a></td>" \
                "<td>"+str(i[7])+"</td><td><a href='/UpdateFaculty?f_id="+str(i[1])+"'>Update </a></td></tr></tbody>"

    context={'data': strdata,'msg':'Assigned Successfully..!!'}
    return render(request,'AdminApp/ViewFaculty.html',context)
