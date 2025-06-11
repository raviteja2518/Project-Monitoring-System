from django.shortcuts import render
from DBConnection.Database import getOneRecord
from DBConnection.Database import getAllRecords
from DBConnection.Database import insertMethod
import pymysql
from django.http import HttpResponse


# Create your views here.
def login(request):
    data=getAllRecords("select * from dept")
    strdata="<select class='form-control border-1 py-3 px-4' name='dept'  style='height: 55px;' required=''> <option selected></option>"
    for i in data:
        strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata}
    return render(request,'StudentApp/Login.html',context)

def Register(request):
    data=getAllRecords("select * from dept")
    strdata="<select class='form-control border-1 py-3 px-4' name='dept'  style='height: 55px;' required=''> <option selected></option>"
    for i in data:
        strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata}
    return render(request,'StudentApp/Register.html',context)

def RegAction(request):
    dept=request.POST['dept']
    rollno=request.POST['rollno']
    title=request.POST['title']
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']

    data=getOneRecord("select * from student")
    if data is not None:
        data1=getOneRecord("select count(*) from student where title='"+title+"'")
        if data1 is not None:
            c=int(data1[0])
            if c<4:
                insertMethod("insert into student values(null,'"+dept+"','"+rollno+"','"+title+"','"+name+"','"+email+"','"+mobile+"','waiting','waiting')")
                data=getAllRecords("select * from dept")
                strdata="<select class='form-control border-1 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
                for i in data:
                    strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
                strdata+= "</select>"
                context = {'data': strdata,'msg':'Registration Successful..!!'}
                return render(request,'StudentApp/Register.html',context)
            else:
                data=getAllRecords("select * from dept")
                strdata="<select class='form-control border-1 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
                for i in data:
                    strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
                strdata+= "</select>"
                context = {'data': strdata,'msg':'Only 4 Members Allowed for this Project..!!'}
                return render(request,'StudentApp/Register.html',context)
        else:
            i=insertMethod("insert into student values(null,'"+dept+"','"+rollno+"','"+title+"','"+name+"','"+email+"','"+mobile+"','waiting','waiting')")
            data=getAllRecords("select * from dept")
            strdata="<select class='form-control border-1 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
            for i in data:
                strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
            strdata+= "</select>"
            context = {'data': strdata,'msg':'Registration Successful..!!'}
            return render(request,'StudentApp/Register.html',context)

    else:
        i=insertMethod("insert into student values(null,'"+dept+"','"+rollno+"','"+title+"','"+name+"','"+email+"','"+mobile+"','waiting','waiting')")
        data=getAllRecords("select * from dept")
        strdata="<select class='form-control border-1 py-3 px-4' name='dept'  style='height: 50px;' required=''> <option selected></option>"
        for i in data:
            strdata+= "<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
        strdata+= "</select>"
        context = {'data': strdata,'msg':'Registration Successful..!!'}
        return render(request,'StudentApp/Register.html',context)

def LogAction(request):
    dept = request.POST['dept']
    rollno = request.POST['rollno']

    data=getOneRecord("select * from student where dept='"+dept+"' and rollno='"+rollno+"'")
    if data is not None:
        request.session['dept']=dept
        request.session['rollno']=rollno
        request.session['title']=data[3]

        return render(request, 'StudentApp/StudentHome.html')
    else:
        context={'data':'Login Failed..!!'}
        return render(request, 'StudentApp/Login.html', context)

def StudentHome(request):
    return render(request, 'StudentApp/StudentHome.html')

def viewfaculty(request):
    dept=request.session['dept']
    rollno=request.session['rollno']
    title=request.session['title']


    data=getAllRecords("select * from student s, faculty f  where s.fid=f.fid and s.title='"+title+"' and s.rollno='"+rollno+"'")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Project Title</th><th>Department</th><th>Faculty Name</th><th>Faculty Email</th>" \
            "<th>Designation</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[3])+"</td><td>"+str(i[1])+"</td><td>"+str(i[11])+"</td><td>"+str(i[13])+"</td>" \
                "<td>"+str(i[14])+"</td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'StudentApp/ViewFaculty.html', context)

def sendreport(request):
    dept=request.session['dept']
    rollno=request.session['rollno']
    title=request.session['title']


    data=getAllRecords("select * from student s, faculty f  where s.fid=f.fid and s.title='"+title+"' and s.rollno='"+rollno+"'")
    fid=None;
    for i in data:
        fid=i[10]
    context={'fid':fid}
    return render(request, 'StudentApp/SendReport.html',context)
def SendReportAction(request):
    if request.method == 'POST' and request.FILES['myfile']:
        review = request.POST['review']
        fid=request.POST['fid']

        dept=request.session['dept']
        rollno=request.session['rollno']
        title=request.session['title']

        con = pymysql.connect(host='localhost', user='root', password='', database='project_monitor')

        data = request.FILES['myfile'].read()
        cur = con.cursor()
        cur.execute('insert into post_review values(null,%s,%s,%s,%s,%s,%s,now(),%s)',(rollno,dept,title,fid,review,data,'waiting'))
        con.commit()
    context={'msg':'Review Successfully sent to Faculty..!!'}
    return render(request, 'StudentApp/SendReport.html',context)

def viewMarks(request):
    dept=request.session['dept']
    rollno=request.session['rollno']
    title=request.session['title']

    data=getAllRecords("select * from post_review where s_rollno='"+rollno+"' and dept='"+dept+"' and title='"+title+"'")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Department</th><th>Title</th><th>Review</th><th>Marks</th><th>Review PDF Submitted Date</th>" \
            "<th>View PDF</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[4])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[5])+"</td>" \
                "<td>"+str(i[8])+"</td><td>"+str(i[7])+"</td><td><a href='/student/ViewReview?r_id="+str(i[0])+"'>View Review </a></td>" \
                "</tr></tbody>"
    context={'data': strdata}
    return render(request, 'StudentApp/ViewMarks.html', context)
def ViewReview(request):
    r_id=request.GET['r_id']
    con=pymysql.connect(host="localhost",user="root",password="root",database="project_monitor")
    cur=con.cursor()
    cur.execute("select review_pdf from post_review where id='"+r_id+"'")
    file=cur.fetchone()[0]
    cur.close()

    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Resume.pdf"'
    return response

def viewnotification(request):
    title=request.session['title']
    data=getAllRecords("select * from notification where title='"+title+"'")
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Faculty ID</th><th>Title</th><th>Notification</th><th>date</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td>" \
                "</tr></tbody>"
    context={'data': strdata}
    return render(request, 'StudentApp/ViewNotification.html', context)

