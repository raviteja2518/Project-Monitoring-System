import pymysql
def insertMethod(query):
    con=pymysql.connect(host='localhost',user='root',password='',database='project_monitor', charset='utf8')
    cur=con.cursor()
    i=cur.execute(query)
    con.commit()
    return i

def getOneRecord(query):
    con=pymysql.connect(host='localhost',user='root',password='',database='project_monitor', charset='utf8')
    cur=con.cursor()
    cur.execute(query)
    data=cur.fetchone()
    return data


def getAllRecords(query):
    con=pymysql.connect(host='localhost',user='root',password='',database='project_monitor', charset='utf8')
    cur=con.cursor()
    cur.execute(query)
    data=cur.fetchall()
    return data
