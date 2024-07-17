from django.shortcuts import render,HttpResponse
from . models import login_user
from django.contrib.auth import authenticate
import sqlite3
from datetime import datetime 
from calendar import monthrange
from datetime import timedelta, date
# Create your views here.

def index(request):
    datem = datetime.now()
    year=datem.year
    month=datem.month

    i=0
    list_month=[]
    list_month.append((month,year))
    while(i<6):
        if((month+1)>12):
            month=(month%12)+1
            year=year+1
        else:
            month=month+1
        list_month.append((month,year))
        i=i+1
    con = sqlite3.connect("rooms.sqlite3")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_name=cursor.fetchall()
    con.close()

    table_list_name=[]

    for i in tables_name:
        table_list_name.append(i[0])
    #print(table_list_name)

    for k in list_month:
        table_name='YEAR'+str(k[1])+'MONTH'+str(k[0])
        if(table_name in table_list_name):
            pass
        else:
            table_name='YEAR'+str(k[1])+'MONTH'+str(k[0])
            conn=sqlite3.connect('rooms.sqlite3')
            sql='CREATE TABLE IF NOT EXISTS {} (room_no integer PRIMARY KEY)'.format(table_name)
            conn.execute(sql)
            conn.close()
        
            no_of_days=monthrange(k[1],k[0])[1]

            for i in range(1,no_of_days+1):
                conn=sqlite3.connect('rooms.sqlite3')
                sql="ALTER TABLE {} ADD COLUMN {} varchar(32) DEFAULT NONE".format(table_name,'DATE'+str(i)+'MONTH'+str(k[0])+'YEAR'+str(k[1]))
                conn.execute(sql)
                conn.commit()
                conn.close()

    return render(request,'index.html')

def userlogin(request):
    if(request.method=='POST' and 'submit_button' in request.POST):
        user_id=request.POST['user_id']
        user_password=request.POST['user_password']

        data=login_user.objects.filter(email=user_id,password=user_password)
        if(len(data)==1): 
            request.session['user_id']=user_id
            return render(request,'user_Homepage.html')
        else:
            return render(request,'user_login.html',{'name':'unsuccess'})
    elif(request.method=='POST' and 'singup_button' in request.POST):
        return render(request,'user_signup.html')
    else:
        return render(request,'user_login.html')

def usersignup(request):
    if(request.method=='POST'):
        user_id=request.POST['user_id']
        user_name=request.POST['user_name']
        user_mobile=request.POST['user_mobile']
        user_password=request.POST['user_password']

        login=login_user(email=user_id,name=user_name,mobile=user_mobile,password=user_password)
        login.save()
        return render(request,'user_login.html')
    else:
        return render(request,'user_signup.html')

def adminlogin(request):
    if(request.method=='POST'):
        admin_name=request.POST['admin_name']
        admin_password=request.POST['admin_password']
        pass1=authenticate(username=admin_name,password=admin_password)
        if(pass1 is not None):
            return render(request,'admin_Homepage.html')
        else:
            return render(request,'admin_login.html',{'name':'unsuccess'})
    else:
        return render(request,'admin_login.html')

def admin_add_room(request):
    unsucess=False
    if(request.method=='POST'):
        room_number=request.POST['room_number']
        room_type=request.POST['room_type']
        room_capacity=request.POST['room_capacity']

        conn=sqlite3.connect("rooms.sqlite3")
        sql='CREATE TABLE IF NOT EXISTS room (room_no integer PRIMARY KEY,room_type text,room_capacity text)'
        conn.execute(sql)
        conn.close()
        try:
            conn=sqlite3.connect("rooms.sqlite3")
            sql='INSERT INTO room (room_no,room_type,room_capacity) VALUES(?,?,?)'
            conn.execute(sql,(room_number,room_type,room_capacity,))
            conn.commit()
            conn.close()

            con = sqlite3.connect("rooms.sqlite3")
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables_name=cursor.fetchall()
            con.close()

            list_table=[]
            for i in tables_name:
                list_table.append(i[0])

            for i in list_table:
                try:
                    conn=sqlite3.connect("rooms.sqlite3")
                    sql='INSERT INTO {} (room_no) VALUES(?)'.format(i)
                    conn.execute(sql,(room_number,))
                    conn.commit()
                    conn.close()
                except:
                    print(i)

        

        except:
            unsucess=False

        conn=sqlite3.connect('rooms.sqlite3')
        sql='select * from room'
        cur=conn.execute(sql)
        data=cur.fetchall()
        conn.close()
        print(data)
        return render(request,'admin_add_room.html',{'name':unsucess,'data':data})
    else:
        con = sqlite3.connect("rooms.sqlite3")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables_name=cursor.fetchall()
        con.close()
        if('room' in tables_name):
            conn=sqlite3.connect('rooms.sqlite3')
            sql='select * from room'
            cur=conn.execute(sql)
            data=cur.fetchall()
            conn.close()
            print(data)
        else:
            data=[]
        return render(request,'admin_add_room.html',{'name':unsucess,'data':data})

def admin_change_room(request):
    conn=sqlite3.connect('rooms.sqlite3')
    sql='select * from room'
    cur=conn.execute(sql)
    data=cur.fetchall()
    conn.close()
    if(request.method=='POST'):

        room_number=request.POST['room_number']
        room_change_date=request.POST.get('room_date')
        room_capacity=request.POST['room_capacity']
        #print(type(room_change_date))
        
        date_time_obj = datetime.strptime(room_change_date, '%Y-%m-%d')
        year=date_time_obj.year
        month=date_time_obj.month
        date=date_time_obj.day

        tabel_name=table_name='YEAR'+str(year)+'MONTH'+str(month)

        con = sqlite3.connect("rooms.sqlite3")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables_name=cursor.fetchall()
        con.close()

       
        list_table=[]
        for i in tables_name:
            list_table.append(i[0])

        
        date_error=False
        if(table_name in list_table):
            
            conn=sqlite3.connect('rooms.sqlite3')
            sql='CREATE TABLE IF NOT EXISTS change_room (room_no integer,capacity text,date text)'
            conn.execute(sql)
            conn.close()

            conn=sqlite3.connect('rooms.sqlite3')
            sql='INSERT INTO change_room (room_no,capacity,date) VALUES (?,?,?)'
            conn.execute(sql,(room_number,room_capacity,room_change_date,))
            conn.commit()
            conn.close()

        else:
            date_error=True
        return render(request,'admin_change_room.html',{'name':date_error,'data':data})
    else:
        date_error=False
        return render(request,'admin_change_room.html',{'name':date_error,'data':data})

def user_search_room(request):
    if(request.method=='POST'):
        check_in_date=request.POST.get('check_in_date')
        check_out_date=request.POST.get('check_out_date')

        check_in_date=check_in_date.split('-')
        check_out_date=check_out_date.split('-')
        check_in=date(int(check_in_date[0]),int(check_in_date[1]),int(check_in_date[2]))
        check_out=date(int(check_out_date[0]),int(check_out_date[1]),int(check_out_date[2]))
        #print(type(check_in))
        list_date=[]
        for dt in daterange(check_in, check_out):
            list_date.append(dt.strftime("%Y-%m-%d"))
        list_date_modify=[]
        for i in list_date:
            date_time_obj = datetime.strptime(i, '%Y-%m-%d')
            list_date_modify.append(date_time_obj)
        reqired_table_name=[]
        for i in list_date_modify:
            table_name='YEAR'+str(i.year)+'MONTH'+str(i.month)
            if(table_name in reqired_table_name):
                continue
            else:
                reqired_table_name.append(table_name)
        conn=sqlite3.connect('/home/venish/Downloads/Hotel_management/hotel_management/rooms.sqlite3')
        cur=conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table=cur.fetchall()
        conn.close()
        table_list=[]
        for i in table:
            table_list.append(i[0])
        count=0
        for i in reqired_table_name:
            if(i in table_list):
                continue
            else:
                count=count+1
        if(count>0):
            return render(request,'user_search_room.html',{'name':False})
        else:
            dict_final={}
            for j in list_date_modify:
                table_name='YEAR'+str(j.year)+'MONTH'+str(j.month)
                if(table_name in dict_final.keys()):
                    dict_final[table_name].append(j)
                else:
                    dict_final[table_name]=[]
                    dict_final[table_name].append(j)
            list_final={}
            for i in dict_final.keys():
                li=[]
                for j in dict_final[i]:
                    column_name='DATE'+str(j.day)+'MONTH'+str(j.month)+'YEAR'+str(j.year)
                    li.append(column_name)
                list_final[i]=li
            
            for i in list_final.keys():
                string=""
                for j in range(len(list_final[i])):
                    if(j==(len(list_final[i])-1)):
                        string=string+' '+list_final[i][j]+'='+" 'NONE'"
                    else:
                        string=string+' '+list_final[i][j]+'='+" 'NONE'" + ' and'
                list_final[i]=string
            data1={}
            for i in list_final:
                conn=sqlite3.connect('/home/venish/Downloads/Hotel_management/hotel_management/rooms.sqlite3')
                sql='SELECT room_no from {} where {}'.format(i,list_final[i])
                cur=conn.execute(sql)
                data=cur.fetchall()
                conn.close()
                data2=[]
                for j in data:
                    data2.append(j[0])
                data1[i]=data2
            data3=[]
            for i in data1:
                data3.append(i)
            final_room=[]
            for i in range(1):
                for j in data1[data3[i]]:
                    count=0
                    for k in data1:
                        if(j not in data1[k]):
                            count=count+1
                    if(count==0):
                        final_room.append(j)
            list_for_given=[]
            for i in final_room:
                conn=sqlite3.connect('rooms.sqlite3')
                sql='SELECT * FROM room WHERE room_no=(?)'
                cur=conn.execute(sql,(i,))
                data=cur.fetchall()
                list_for_given.append(data)
            
            return render(request,'user_search_room.html',{'name':True,'data':list_for_given})
    
    else:
        return render(request,'user_search_room.html',{'name':False})

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def user_book_room(request):
    if(request.method=='POST' and 'search_button' in request.POST):
        check_in_date1=request.POST.get('check_in_date')
        check_out_date1=request.POST.get('check_out_date')
        room_type=request.POST['room_type']

        check_in_date=check_in_date1.split('-')
        check_out_date=check_out_date1.split('-')
        check_in=date(int(check_in_date[0]),int(check_in_date[1]),int(check_in_date[2]))
        check_out=date(int(check_out_date[0]),int(check_out_date[1]),int(check_out_date[2]))
        list_date=[]
        for dt in daterange(check_in, check_out):
            list_date.append(dt.strftime("%Y-%m-%d"))
        list_date_modify=[]
        for i in list_date:
            date_time_obj = datetime.strptime(i, '%Y-%m-%d')
            list_date_modify.append(date_time_obj)
        reqired_table_name=[]
        for i in list_date_modify:
            table_name='YEAR'+str(i.year)+'MONTH'+str(i.month)
            if(table_name in reqired_table_name):
                continue
            else:
                reqired_table_name.append(table_name)
        conn=sqlite3.connect('rooms.sqlite3')
        cur=conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table=cur.fetchall()
        conn.close()
        table_list=[]
        for i in table:
            table_list.append(i[0])
        count=0
        for i in reqired_table_name:
            if(i in table_list):
                continue
            else:
                count=count+1
        if(count>0):
            return render(request,'user_book_room.html',{'name':False})
        else:
            dict_final={}
            for j in list_date_modify:
                table_name='YEAR'+str(j.year)+'MONTH'+str(j.month)
                if(table_name in dict_final.keys()):
                    dict_final[table_name].append(j)
                else:
                    dict_final[table_name]=[]
                    dict_final[table_name].append(j)
            list_final={}
            for i in dict_final.keys():
                li=[]
                for j in dict_final[i]:
                    column_name='DATE'+str(j.day)+'MONTH'+str(j.month)+'YEAR'+str(j.year)
                    li.append(column_name)
                list_final[i]=li
            
            for i in list_final.keys():
                string=""
                for j in range(len(list_final[i])):
                    if(j==(len(list_final[i])-1)):
                        string=string+' '+list_final[i][j]+'='+" 'NONE'"
                    else:
                        string=string+' '+list_final[i][j]+'='+" 'NONE'" + ' and'
                list_final[i]=string
            data1={}
            for i in list_final:
                conn=sqlite3.connect('rooms.sqlite3')
                sql='SELECT room_no from {} where {}'.format(i,list_final[i])
                cur=conn.execute(sql)
                data=cur.fetchall()
                conn.close()
                data2=[]
                for j in data:
                    data2.append(j[0])
                data1[i]=data2
            data3=[]
            for i in data1:
                data3.append(i)
            final_room=[]
            for i in range(1):
                for j in data1[data3[i]]:
                    count=0
                    for k in data1:
                        if(j not in data1[k]):
                            count=count+1
                    if(count==0):
                        final_room.append(j)
            list_for_given=[]
            for i in final_room:
                conn=sqlite3.connect('rooms.sqlite3')
                sql='SELECT room_no FROM room WHERE room_no=(?) and room_type=(?)'
                cur=conn.execute(sql,(i,room_type,))
                data=cur.fetchall()
                if(len(data)>0):
                    list_for_given.append(data)
            #print(list_for_given)
            return render(request,'user_book_room.html',{'name':True,'data':list_for_given,'check_in_date':check_in_date1,'check_out_date':check_out_date1})
    elif(request.method=='POST' and 'book_button' in request.POST):
        no_of_guest=request.POST['no_of_guest']
        room_no=request.POST['room_number']
        email=request.session['user_id']
        check_in_date2=request.POST.get('check_in')
        check_out_date2=request.POST.get('check_out')
        data=login_user.objects.filter(email=email).first()
        name=data.name
        mobile=data.mobile

        check_in_date=check_in_date2.split('-')
        check_out_date=check_out_date2.split('-')
        check_in=date(int(check_in_date[0]),int(check_in_date[1]),int(check_in_date[2]))
        check_out=date(int(check_out_date[0]),int(check_out_date[1]),int(check_out_date[2]))


        list_date=[]
        for dt in daterange(check_in, check_out):
            list_date.append(dt.strftime("%Y-%m-%d"))
        
        table_name='MONTH'+check_in_date[1]+'YEAR'+check_in_date[0]+'VISITOR'

        conn=sqlite3.connect('rooms.sqlite3')
        sql='CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,Name text,mobile TEXT,room_no TEXT,no_of_guest TEXT,check_in TEXT,check_out TEXT)'.format(table_name)
        conn.execute(sql)
        conn.close()

        conn=sqlite3.connect('rooms.sqlite3')
        sql='INSERT  INTO {} (email,Name,mobile,room_no,no_of_guest,check_in,check_out) VALUES (?,?,?,?,?,?,?)'.format(table_name)
        conn.execute(sql,(email,name,mobile,room_no,no_of_guest,check_in_date2,check_out_date2,))
        conn.commit()
        conn.close()
            
        conn=sqlite3.connect('rooms.sqlite3')
        sql='SELECT * FROM {}'.format(table_name)
        cur=conn.execute(sql)
        data=cur.fetchall()
        data_len=len(data)
        conn.close()
        
        for i in list_date:
            da=i.split('-')
            #print(da)
            if(da[2].startswith('0')):
                da[2]=da[2][1:]
            if(da[1].startswith('0')):
                da[1]=da[1][1:]
            #print(da)
            table_name='YEAR'+da[0]+'MONTH'+da[1]
            column_name='DATE'+da[2]+'MONTH'+da[1]+'YEAR'+da[0]

            conn=sqlite3.connect("rooms.sqlite3")
            sql='UPDATE {} SET {} = (?) WHERE room_no=(?)'.format(table_name,column_name)
            conn.execute(sql,(str(data_len),room_no))
            conn.commit()
            conn.close()

        return render(request,'user_Homepage.html')
    else:
        return render(request,'user_book_room.html',{'name':False})

def admin_view_details(request):
    if(request.method=='POST'):
        name=False
        month=request.POST.get('select_month')
        da=month.split('-')
        table_name='MONTH'+da[1]+'YEAR'+da[0]+'VISITOR'

        conn=sqlite3.connect('rooms.sqlite3')
        cur=conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table=cur.fetchall()
        conn.close()
        table_list=[]
        for i in table:
            table_list.append(i[0])
        if(table_name not in table_list):
            name=True
            return render(request,'admin_view_details.html',{'name':name})
        else:
            conn=sqlite3.connect('rooms.sqlite3')
            cur=conn.execute("SELECT * FROM {}".format(table_name))
            table=cur.fetchall()
            conn.close()

            return render(request,'admin_view_details.html',{'name':False,'data':table})
    else:
        return render(request,'admin_view_details.html',{'name':False})
