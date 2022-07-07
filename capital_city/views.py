from capital_city import add_places
from django.shortcuts import render
import folium
from geopy import distance
import pandas as pd
from capital_city import map_generator_for_lis
from capital_city.marker import map_marker




df=pd.read_csv('./File/class.csv')

lis=[]


#Home page action or initial action
def home(request):
    add_places.Create_Data_Frame()
    return render(request,'home.html',{'lis':lis})


#Add more places action
def first_add(request):
    place=request.GET['Place']
    add_places.add_place(place)
    # lis=add_places.get_city()
    lis = pd.read_csv('./File/lis.csv')['city'].unique()
    map=map_generator_for_lis.map_generator(lis)
    return render(request,'add.html',{'lis':lis,'map':map}) 

#Redirect to district page
def district_home(request):
    return render(request,'district.html')

#Add district
def add_district(request):
    District=request.GET['District']
    dis=df[df['District']==District]
    for place in dis['Constituency'].to_list():
        add_places.add_place(place)

    lis=add_places.get_city()
    map=map_generator_for_lis.map_generator(lis)
    return render(request,'add.html',{'lis':lis,'map':map}) 


#Redirect to State page
def state_home(request):
    return render(request,'state.html')

#Add state
def add_state(request):
    State=request.GET['State']
    st=df[df['State']==State]
    for place in st['Constituency'].to_list():
        add_places.add_place(place)
    lis=add_places.get_city()
    map=map_generator_for_lis.map_generator(lis)
    return render(request,'add.html',{'lis':lis,'map':map}) 

#Final Action, redirect to Result page
def result(request):
    lis=add_places.get_city()
    lis1=[]
    for i in lis:
        lis1.append(i)
    area,cap_list=map_marker(lis)
    city_list=[]
    for i in cap_list:
        idx=df[df['Constituency']==i].index.values[0]
        temp={
        'city':df.loc[idx,'Constituency'],
        'dist':df.loc[idx,'District'],
        'st':df.loc[idx,'State'],
        'typ':df.loc[idx,'Classifier'],
        'ppl':df.loc[idx,'Population'],
        'tir':df.loc[idx,'Tire'],
        'link':f"https://www.google.com/search?client=firefox-b-d&q={df.loc[idx,'Constituency']}"
        }
        city_list.append(temp)
    city_len=len(city_list)
    return render(request,'result.html',locals())
