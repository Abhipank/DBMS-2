from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.fun2),
    path('',views.fun2,name="hi"),
    path('register/',views.fun)
]