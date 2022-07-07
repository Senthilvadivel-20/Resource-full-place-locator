
from django.contrib import admin
from django.urls import path
from capital_city import views

from django.views.static import serve
from django.urls import re_path as url
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),                        #Home.html page
    path('first_add',views.first_add,name='first_add'),     #Add more.html page
    path('result',views.result,name='result'),              #result.html page
    path('Add_district',views.add_district,name='add_district'),    #district.html ---> add.html
    path('District_home',views.district_home,name='district_home'), #district.html page
    path('Add_State',views.add_state,name='add_state'),             #state.html ---> add.html
    path('State_home',views.state_home,name='state_home'),          #state.html page

    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})


]
