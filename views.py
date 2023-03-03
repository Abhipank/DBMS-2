from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.db import connection
import django.db as db
from django.utils import timezone
# Create your views he
from django.views.decorators.cache import cache_control
import datetime


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def say_hello(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
     print("*???")
     return redirect("home")
    else:
     return HttpResponse(render(request,'hello.html',{}))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fun(request):
 if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
    print("*???")
    return redirect("home")
 else:
    return render(request,'wait.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fun2(request):
    #post is not recognised POST is correct
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
     print("fubuki atsuya")
     return render(request,"rook.html")
    else:
     cursor=connection.cursor()
     val=(request.POST['num1'])
     va=(request.POST['num2'])
     rows=[]
     
     #print(len(va)) it is empty thing
     try:
      print("&")
      cursor.execute('''select password from users where id=%s'''%(val))
      rows=cursor.fetchall()
      print(rows)
      if len(rows)!=0 and ((len(va)==0 and len(rows[0])==0) or (rows[0][0]==va)):
       print("kalu")
       response=render(request,"rook.html")
       response.set_cookie("UserID",val)
       response.set_cookie("login_status",True)
       return response
      else:
       messages.success(request,("Invalid UsedID/password"))
       return redirect("hi")
      cursor.close()
     except Exception:
      print("*")
      messages.success(request,("Invalid UsedID/password"))
      return redirect("hi")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    #now=datetime.datetime.now()
    #print(now)
    #print(type(now))
    #now=str(now)
    #can on;ly be used in queriesprint(current_timestamp)
    cursor=connection.cursor()
    val=request.COOKIES['UserID']
    cursor.execute('''update users set last_access_date=current_timestamp where id=%s'''%(val))
    response=HttpResponseRedirect(reverse("hi"))
    response.delete_cookie('UserID')
    response.delete_cookie('login_status')
    cursor.close()
    return response
    #cookies ka no asar if return redirect("hi")
    #asar if done request.COOKIES.clear() then say_hello(request) otherwise again said redirect("path") no asar .if then said not path only page then still is a problem

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def successregis(request):
 if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
    print("*???")
    return redirect("home")
 else:
   try:
    val1=request.POST['num1']
    val2=request.POST['num2']
    val3=0
    val4=request.POST['num4']
    val5=request.POST['num5']
    val6=request.POST['num6']
    val7=request.POST['num7']
    cursor=connection.cursor()
    now=datetime.datetime.now()
    #here the real problem was '%s'
    
    cursor.execute('''insert into users (id,display_name,account_id,reputation,location,website_url,about_me,creation_date,last_access_date,password) values(nextval('users_id_seq'),'%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(val1,val2,val3,val4,val5,val6,now,now,val7))
    cursor.execute('''select last_value from users_id_seq''')
    value=cursor.fetchall()
    context={
        'UserID': value[0][0],
        'password': val7
    }
    cursor.close()
    return HttpResponse(render(request,'success.html',context))
   except Exception:
    messages.success(request,("Invalid Details"))
    return redirect("regis")
    

#function has return 0 then error int has no attribute