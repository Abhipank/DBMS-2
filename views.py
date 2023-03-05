from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.db import connection, transaction
import django.db as db
from django.utils import timezone
# Create your views he
from django.views.decorators.cache import cache_control
import datetime
from django.http import JsonResponse

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def say_hello(request):
    print("first")
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        user_id=request.COOKIES['UserID']
        print(user_id)
        cursor = connection.cursor()
        cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
        val1 = cursor.fetchall()
        cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
        ids = cursor.fetchall()
        title_list = []
        id_list = []
        for v in val1:
            title_list.append(v[0])

        for i in ids:
            id_list.append(i[0])
        
        data = []
        i = 0
        for id in id_list:
            data.append([id, title_list[i]])
            i = i+1

        context = {'data': data, 'user_id': user_id}
        
        cursor.close()
        
        return render(request, 'user_posts.html', context)
    else:
        return HttpResponse(render(request,'hello.html',{}))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fun(request):
 if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
    print("*???")
    return redirect("home")
 else:
    return render(request,'wait.html')


def fun2(request):
    #post is not recognised POST is correct
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
     print("fubuki atsuya")
     user_id=request.COOKIES['UserID']
     print(user_id)
     cursor = connection.cursor()
     cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
     val1 = cursor.fetchall()
     cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
     ids = cursor.fetchall()
     title_list = []
     id_list = []
     for v in val1:
        title_list.append(v[0])

     for i in ids:
        id_list.append(i[0])
    
     data = []
     i = 0
     for id in id_list:
        data.append([id, title_list[i]])
        i = i+1

     context = {'data': data, 'user_id': user_id}
    
     cursor.close()
     return render(request,"user_posts.html",context)
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
      user_id=val
      cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
      val1 = cursor.fetchall()
      cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
      ids = cursor.fetchall()
      title_list = []
      id_list = []
      for v in val1:
        title_list.append(v[0])

      for i in ids:
        id_list.append(i[0])
    
      data = []
      i = 0
      for id in id_list:
        data.append([id, title_list[i]])
        i = i+1

      context = {'data': data, 'user_id': user_id}

      response=render(request,"user_posts.html",context)
      response.set_cookie("UserID",val)
      response.set_cookie("login_status",True)
      return response
     else:
      messages.success(request,("Invalid UsedID/password"))
      return redirect("hi")
     cursor.close()
    except Exception:
     print("********error")
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


def user_posts(request):
    user_id = request.COOKIES['UserID']
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
        val = cursor.fetchall()
        cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
        ids = cursor.fetchall()
        title_list = []
        id_list = []
        for v in val:
            title_list.append(v[0])

        for i in ids:
            id_list.append(i[0])
        
        data = []
        i = 0
        for id in id_list:
            data.append([id, title_list[i]])
            i = i+1

        context = {'data': data, 'user_id': user_id}
        
        cursor.close()
        
        return render(request, 'user_posts.html', context)

    else:
        context = {}
        return render(request, 'hello.html', context)

def split_tags_list(tag_string):
    tags = []
    fin_tags = []
    tags = tag_string.split('<')[1:]
    for b in tags:
        fin_tags.append(b.split('>')[0])
    return fin_tags

def make_tags_str(tags):
    if tags:
        tag_str = '<'
        for a in tags[:-1]:
            tag_str = tag_str + a + '><'
        tag_str = tag_str + tags[-1] + '>'
    else:
        tag_str = ''
    return tag_str

def tag_check(tag):
    cursor = connection.cursor()
    cursor.execute(''' select tag_name from tags where tag_name = %s ''', [tag])
    tag_name = cursor.fetchall()
    cursor.close()
    if tag_name:
        return True
    else:
        return False

#back direction removed bec there was error of index
def detail(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        u_id = request.COOKIES['UserID']
        cursor = connection.cursor()
        cursor.execute(''' select owner_user_id from posts where id = %s ''', [post_id])
        owner_id = cursor.fetchall()[0][0]
        cursor.execute(''' select title from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        post_title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        body = cursor.fetchall()[0][0]
        cursor.execute(''' select tags from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        tag_str = cursor.fetchall()[0][0]
        if tag_str:
            tags = split_tags_list(tag_str)
        else:
            tags = None
        cursor.execute(''' select owner_user_id from posts where parent_id=%s order by id desc ''', [post_id])
        rid = cursor.fetchall()
        is_owner = (u_id == str(owner_id))
        #print(type(u_id),type(owner_id))
        print(is_owner)
        r_id_fin = []
        for i in rid:
            if i[0] == None:
                r_id_fin.append('Anonymous')
            else:
                r_id_fin.append(i[0])
        
        cursor.execute(''' select body from posts where parent_id=%s order by id desc ''', [post_id])
        bod = cursor.fetchall()
        bod_fin = []
        for i in bod:
            bod_fin.append(i[0])
        Replies = []
        i = 0
        for id in r_id_fin:
            Replies.append([id, bod_fin[i]])
            i = i+1
        context = {'is_owner': is_owner, 'u_id': owner_id ,'post_title': post_title, 'body': body, 'tags': tags, 'Replies': Replies, 'post_id': post_id}
        return render(request, 'detail.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reply(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        #u_id = request.session.get('user_id')
        u_id = request.COOKIES['UserID']
        cursor = connection.cursor()
        reply=None
        cursor.execute(''' select title from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        post_title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        body = cursor.fetchall()[0][0]
        cursor.execute(''' select tags from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        tag_str = cursor.fetchall()[0][0]
        if tag_str:
            tags = split_tags_list(tag_str)
        else:
            tags = None
        cursor.close()
        if request.method == 'POST':
            if request.POST.get('reply_text'):
                cursor = connection.cursor()
                creation_date = datetime.datetime.now()
                reply_text = request.POST.get('reply_text')
                reply_text='<p>' + reply_text +'</p>'
                strt="CC BY-SA 2.5"
                cursor.execute(''' insert into posts (owner_user_id,score,content_license, parent_id, post_type_id, body, creation_date) values(%s,1,%s, %s, 2, %s, %s) ''', [u_id,strt, post_id, reply_text, creation_date])
                transaction.commit()
                cursor.close()
                return redirect('detail', post_id)
            else:
                message = "Please fill in all the required fields."
                context = {'post_id': post_id, 'post_title': post_title, 'body':body, 'message': message, 'tags': tags}
                return render(request, 'reply.html', context)
        else:
            context = {'post_id': post_id, 'post_title': post_title, 'body':body, 'tags': tags}
            return render(request, 'reply.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_post(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES: 
        if request.method == 'POST':
            if request.POST.get('post_title') and request.POST.get('post_text'):
                request.session['tags'] = []
                user_id = request.COOKIES['UserID']
                post_title = request.POST.get('post_title')
                post_body = request.POST.get('post_text')
                post_body = '<p>' + post_body +'</p>'
                post_body = post_body.replace('\n', '</p><p>')
                creation_date = datetime.datetime.now()
                cursor = connection.cursor()
                strt="CC BY-SA 2.5"
                cursor.execute('''Insert into posts (owner_user_id, post_type_id,score,content_license, view_count, answer_count, title, body, creation_date) values( %s, 1,0,%s, 0, 0, %s, %s, %s)''', [user_id,strt, post_title, post_body, creation_date])
                transaction.commit()
                cursor.close()
                return redirect('add_tags')
            else:
                message = "Please fill in all required fields."
                return render(request, 'create_post.html', {'message': message})
        else:
            return render(request, 'create_post.html')
    else:
        context = {}
        return render(request, 'hello.html', context)


def search_tag_in(tags):
    if len(tags) != 0:
        cursor = connection.cursor()
        cursor.execute(''' select tags from posts order by creation_date desc ''')
        rset_tags = cursor.fetchall()
        tags_arr = []
        for a in rset_tags:
            tags_arr.append(a[0])
        
        n_tags_arr = []
        
        for a in tags_arr:
            if a:
                n_tags_arr.append(split_tags_list(a))
            else:
                n_tags_arr.append(None)

        cursor.execute(''' select id from posts order by creation_date desc ''')
        rset_id = cursor.fetchall()
    
        id_arr = []

        for a in rset_id:
            id_arr.append(a[0])

        cursor.execute(''' select count(*) from posts ''')
        count = cursor.fetchall()[0][0]
    
        pos_count = list(range(count))
    
        n_pos = []
    
        for t in tags:
            n_pos = pos_count.copy()
            pos_count = []
            for i in n_pos:
                if n_tags_arr[i]:
                    for in_tag in n_tags_arr[i]:
                        if in_tag == t:
                            pos_count.append(i)
            n_pos = []

        cursor.execute(''' select title from posts order by creation_date desc ''')
        rset_title = cursor.fetchall()
        title_arr = []
        for a in rset_title:
            title_arr.append(a[0])

        id_title = [] 

        for i in pos_count:
            id_title.append([id_arr[i], title_arr[i]])
        cursor.close()
        return id_title
    else:
        return []



def search_tag(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        print("8888")
        if request.method=='POST':
            if 'done_now' in request.POST:
                print('jgh')
                if request.POST.get('taggg') != '':
                    print('ZHC')
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('taggg', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            request.session['tags'] = []
                            id_title = search_tag_in(tags)
                            return search_detail(request, id_title, 1, tags)
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                else:
                    try:
                        tags = request.session.get('tags')
                        request.session['tags'] = []
                        id_title = search_tag_in(tags)
                        return search_detail(request, id_title, 1, tags)
                    except ValueError:
                        context = {}
                return render(request, 'search_tag.html', context)
            elif 'add_now' in request.POST:
                print("kira hiroto")
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags') 
                        if tags==None: tags=[]
                        print("tags",tags)
                        tag = request.POST.get('taggg', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            request.session['tags'] = []
                            context={'tags': tags}
                            request.session['tags'] = tags
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'search_tag.html', context)
                else:
                    try:
                        tags = request.session.get('tags')
                        error_message = 'Select tag!'
                        context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'search_tag.html', context)
            else:
                context = {}
                return render(request, 'search_tag.html', context)
        else:  
            context = {}
            return render(request, 'search_tag.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)


def search_user(request):
    print("fdjfdj")
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        print("*")
        if request.method == 'POST':
         print("*")

         s_user = request.POST.get('s_user')
         print(s_user)

         if s_user:
            cursor = connection.cursor()
            cursor.execute(''' select id from users where id = %s ''', [s_user])
            id_exist = cursor.fetchall()
            if id_exist:
                cursor = connection.cursor()
                cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc''', [s_user])
                rset_id = cursor.fetchall()
                rs_id = []
                for a in rset_id:
                    rs_id.append(a[0])

                cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc ''', [s_user])
                rset_title = cursor.fetchall()
                rs_title = []
                for a in rset_title:
                    rs_title.append(a[0])

                id_title = []
                i = 0
                for a in rs_id:
                    id_title.append([a, rs_title[i]])
                    i += 1

                return search_detail(request, id_title, 2, s_user)
            else:
                error_message = 'Selected user does not exist!'
                context = {'error_message': error_message}
                return render(request, 'search_user.html', context)
         else:
            error_message = 'Selected user does not exist!'
            context = {'error_message': error_message}
            return render(request, 'search_user.html', context)
        else:
            return render(request, 'search_user.html', {})
    else:
        context = {}
        return render(request, 'hello.html', context)


def search_detail(request, id_title, type, q):
    if id_title:
        if type == 1:
            tags = q
            tag = True
            context = {'tag': tag, 'tags': tags, 'id_title': id_title}
        elif type == 2:
            s_user = q
            context = {'s_user': s_user, 'id_title': id_title}
    else:
        if type == 1:
            tags = q
            tag = True
            message= "No posts with such tags"
            context = {'message': message, 'tag': tag, 'tags': tags}
        if type == 2:
            s_user = q
            message = "User_{} has no posts yet".format(s_user)
            context = {'message': message, 's_user': s_user}
    return render(request, 'search_detail.html', context)



def call_search(request):
    print("***")
    return render(request, 'search.html')

def edit_post(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' select title from posts where id = %s ''', [post_id])
        title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where id = %s ''', [post_id])
        body = cursor.fetchall()[0][0]
        cursor.close()
        if request.method == 'POST':
            if request.POST['post_title'] and request.POST['post_text']:
                post_title = request.POST.get('post_title')
                post_text = request.POST.get('post_text')
                edit_time = datetime.datetime.now()
                cursor = connection.cursor()
                cursor.execute(''' update posts set title = %s, body = %s, last_edit_date = %s where id = %s ''', [post_title, post_text, edit_time, post_id])
                transaction.commit()
                cursor.close()
                return redirect('edit_tags', post_id)
            else:
                message = "Please fill in all required fields."
                return render(request, 'edit_post.html', {'title': title, 'body': body, 'message': message, 'post_id': post_id})
        else:
            context = {'title': title, 'body': body, 'post_id': post_id}
            return render(request, 'edit_post.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_tags(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' select tags from posts where id = %s ''', [post_id])
        pre_tags_str = cursor.fetchall()[0][0]
        cursor.close()
        pre_tags=[]
        if pre_tags_str!=None:
         pre_tags = split_tags_list(pre_tags_str)
        if request.method=='POST':
            if 'done' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            cursor = connection.cursor()
                            tags.append(tag)
                            p_id = post_id
                            t_string = make_tags_str(tags)
                            cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                            transaction.commit()
                            request.session['tags'] = []
                            cursor.close()
                            pre_tags = []
                            return redirect('user_posts')
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                else:
                    try:
                        tags = request.session.get('tags')
                        cursor = connection.cursor()
                        p_id = post_id
                        t_string = make_tags_str(tags)
                        cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                        transaction.commit()
                        request.session['tags'] = []
                        pre_tags = []
                        cursor.close()
                        return redirect('user_posts')
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                return render(request, 'edit_tags.html', context)
            elif 'add' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            context={'pre_tags': pre_tags, 'tags': tags}
                            request.session['tags'] = tags
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                    return render(request, 'edit_tags.html', context)
                else:
                    try:
                        tags = request.session.get('tags')
                        error_message = 'Select tag!'
                        context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                    return render(request, 'edit_tags.html', context)
            else:
                context = {'pre_tags': pre_tags}
                return render(request, 'edit_tags.html', context)
        else:
            context = {'pre_tags': pre_tags}
            return render(request, 'edit_tags.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_post(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' delete from posts where id = %s ''', [post_id])
        transaction.commit()
        cursor.close()
        return redirect('user_posts')
    else:
        context = {}
        return render(request, 'hello.html', context)


def add_tags(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' select last_value from posts_id_seq ''')
        p_id = cursor.fetchall()[0][0]
        cursor.close()
        if request.method=='POST':
            if 'done' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        print("*here we areoifw")
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            cursor = connection.cursor()
                            tags.append(tag)
                            t_string = make_tags_str(tags)
                            print(t_string,type(t_string),p_id,type(p_id))
                            p_id=str(p_id)
                            cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                            transaction.commit()
                            request.session['tags'] = []
                            cursor.close()
                            return redirect('user_posts')
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        print("ppppppppppppp")
                        context = {}
                else:
                    try:
                        tags = request.session.get('tags')
                        cursor = connection.cursor()
                        t_string = make_tags_str(tags)
                        cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                        transaction.commit()
                        request.session['tags'] = []
                        cursor.close()
                        return redirect('user_posts')
                    except ValueError:
                        context = {}
                return render(request, 'add_tags.html', context)
            elif 'add' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            context={'tags': tags}
                            request.session['tags'] = tags
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'add_tags.html', context)
                else:
                    try:
                        tags = request.session.get('tags')
                        error_message = 'Select tag!'
                        context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'add_tags.html', context)
            else:
                context = {}
                return render(request, 'add_tags.html', context)
        else:  
            context = {}
            return render(request, 'add_tags.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)


def auto(request):
   search=request.GET.get('search')
   #space being removed by js not in case 30 30
   #print(search.isspace())
   payload=[]
   if search:
    search="%"+search+"%"
    payload=[]
    print("*********************")
    if search:
     cursor=connection.cursor()
     #= not works but like works
     print(search)
     cursor.execute('''select id from users where CAST(id AS TEXT) like %s  limit 10 ''',[search])
     out=cursor.fetchall()
     if len(out)!=0:
      for i in range(0,len(out)):
        payload.append(out[i][0])
     return JsonResponse({
        'status': True,
        'payload':payload
     })
   else:
    return JsonResponse({
        'status': True,
        'payload':payload
     })


def tag_search(request):
   print("TAGS")
   search=request.GET.get('search')
   print(search)
   #space being removed by js not in case 30 30
   #print(search.isspace())
   payload=[]
   if search:
    search="%"+search+"%"
    payload=[]
    print("*********************")
    if search:
     cursor=connection.cursor()
     #= not works but like works
     print(search)
     cursor.execute('''select tag_name from tags where tag_name like %s  ''',[search])
     out=cursor.fetchall()
     if len(out)!=0:
      for i in range(0,len(out)):
        payload.append(out[i][0])
     return JsonResponse({
        'status': True,
        'payload':payload
     })
   else:
    return JsonResponse({
        'status': True,
        'payload':payload
     })