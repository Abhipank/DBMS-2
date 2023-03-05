from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_control

urlpatterns=[
    path('home', views.fun2, name='user_posts'),
    path('home',views.fun2,name="home"),
    # path('', views.say_hello, name='index'),
    path('',views.say_hello,name="hi"),
    path('register/',views.fun,name="regis"),
    path('register1/',views.successregis),
    path('logout/',views.logout,name="logout"),
    #path('home', views.user_posts, name='home'),
    path('create_post', views.create_post, name='create_post'),
    path('create_post/add_tags', views.add_tags, name='add_tags'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('<int:post_id>/edit_post/', views.edit_post, name='edit_post'),
    path('<int:post_id>/edit_tags/', views.edit_tags, name='edit_tags'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/reply/', views.reply, name='reply'),
    path('search_tag/', views.search_tag, name='search_tag'),
    path('search_user/', views.search_user, name='search_user'),
    path('search_detail/', views.search_detail, name='search_detail'),
    path('search/', views.call_search, name='search'),
    path('auto/',views.auto),
    path('tag_search/',views.tag_search),
    path('search_tag/', views.search_tag,name='done_now'),
    path('search_tag/', views.search_tag,name='add_now'),
    # path('add_tags/',views.add_tags,name='udd_tags')
]