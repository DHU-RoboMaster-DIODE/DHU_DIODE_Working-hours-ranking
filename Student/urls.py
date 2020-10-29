from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from login import views

urlpatterns = [

    path('<first>/<mid>/',                               views.deal.as_view()),
    path('<first>/<mid>/<function>/',                    views.deal.as_view()),
    path('<first>/<mid>/<function>/<value>/',            views.deal.as_view()),
    path('<first>/<mid>/<function>/<value>/<json>',      views.deal.as_view()),
    
    path('captcha/', include('captcha.urls')),

]
