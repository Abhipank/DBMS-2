from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import connection
# Create your views here.


def say_hello(request):
    return render(request,'hello.html',{})

def fun(request):
    return render(request,'wait.html')

def fun2(request):
    #post is not recognised POST is correct
     cursor=connection.cursor()
     val=(request.POST['num1'])
     va=(request.POST['num2'])
     rows=[]
     #print(len(va)) it is empty thing
     if len(val)!=0:
      cursor.execute('''select password from users where id=%s'''%(val))
      rows=cursor.fetchall()
     #p=[('')]
     #print(len(p[0][0])) will through error
     # but it is not null 
     if len(rows)!=0 and ((len(va)==0 and len(rows[0])==0) or (rows[0][0]==va)):
      return render(request,"rook.html")
     else:
      messages.success(request,("Invalid UsedID/password"))
      return redirect("hi")
     cursor.close()