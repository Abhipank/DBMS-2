from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_control

urlpatterns=[
    path('home',views.fun2,name="home"),
    path('',views.say_hello,name="hi"),
    path('register/',views.fun,name="regis"),
    path('register1/',views.successregis),
    path('logout/',views.logout,name="logout")
]