import pandas as pd
from geopy import distance
import folium
from capital_city import map_generator_for_lis

df=pd.read_csv('.\File\class.csv')


#decide how many cities will suggest
def map_marker(lis):
    size=len(lis)

    if size <=5:
        n=1
    elif size <=10:
        n=2
    elif size <= 25:
        n=3
    elif size <=40:
        n=4
    elif size <=50:
        n=5
    elif size <=100:
        n=6
    elif size <=200:
        n=7
    else:
        n=8


    area=map_generator_for_lis.map_for_marker()

    cap_list=[]
    for city in range(n):
        da=pd.DataFrame(index=lis,columns=lis)
        for i in lis:
            for j in lis:
                city=[i,j]
                loc_1=df.loc[df['Constituency']==i,'lat'].values,df.loc[df['Constituency']==i,'long'].values
                loc_2=df.loc[df['Constituency']==j,'lat'].values,df.loc[df['Constituency']==j,'long'].values
                dist=distance.distance(loc_1,loc_2).km
                da.loc[i,j]=dist
          

        sample=da.sum(axis=1).reset_index()
        mini=sample[0].min()
        cap=sample.loc[sample[0]==mini,'index'].iloc[0]
        
        #print(lis)
        cap_list.append(cap)
        lis.remove(cap)
        #print(f'{cap} is poped')
    
    
    cap_df=df[df['Constituency']=='None']

    for i in cap_list:
        m=df[df['Constituency']==i]
        cap_df=pd.concat([cap_df,m])

    cap_df.sort_values(by=['Tire','Population'],ascending=[True,False],inplace=True)

    capital=cap_df['Constituency'].to_list()[0]
    capital=[capital]

    air=pd.read_csv('.\File\Airport.csv')
    port_name=air['Name'].to_list()

    port=pd.DataFrame(index=port_name,columns=capital)

    for i in range(len(port_name)):
        loc1=df.loc[df['Constituency']==capital[0],'lat'].values,df.loc[df['Constituency']==capital[0],'long'].values
        loc2=air.loc[air['Name']==port_name[i],'lat'].values,air.loc[air['Name']==port_name[i],'long'].values
        dist=distance.distance(loc1,loc2).km
        #print(dist)
        port.loc[port_name[i],capital[0]]=dist

    air_dist=port.reset_index().sort_values(by=capital[0])

    #Airport Marker
    for i in range(2):
        name=air_dist['index'].iloc[i]
        loc=air.loc[air['Name']==air_dist['index'].iloc[i],'lat'].values,air.loc[air['Name']==air_dist['index'].iloc[i],'long'].values
        icn=folium.Icon(color='blue', icon='plane', icon_color="black", prefix='fa')
        folium.Marker(loc,icon=icn,popup=f'<strong>The nearest airport {name}</strong>',tooltip='Airport').add_to(area)

    #capital city marker
    for cap in cap_list:
        if (df.loc[df['Constituency']==cap,'Tire'].values)==1: #Tire 1 city
            cap_location=df.loc[df['Constituency']==cap,'lat'].iloc[0],df.loc[df['Constituency']==cap,'long'].iloc[0]
            icn=folium.Icon(color='red', icon='fort-awesome', icon_color="black", prefix='fa')
            folium.Marker(cap_location,icon=icn,popup=f'<strong>Suggested capital city {cap}</strong>',tooltip=cap).add_to(area)
        elif (df.loc[df['Constituency']==cap,'Tire'].values)==2: #Tire 2 city
            cap_location=df.loc[df['Constituency']==cap,'lat'].iloc[0],df.loc[df['Constituency']==cap,'long'].iloc[0]
            icn=folium.Icon(color='lightgray', icon='fort-awesome', icon_color="black", prefix='fa')
            folium.Marker(cap_location,icon=icn,popup=f'<strong>Suggested capital city {cap}</strong>',tooltip=cap).add_to(area)
        elif (df.loc[df['Constituency']==cap,'Tire'].values)==3: #Tire 3 city
            cap_location=df.loc[df['Constituency']==cap,'lat'].iloc[0],df.loc[df['Constituency']==cap,'long'].iloc[0]
            icn=folium.Icon(color='blue', icon='fort-awesome', icon_color="black", prefix='fa')
            folium.Marker(cap_location,icon=icn,popup=f'<strong>Suggested capital city {cap}</strong>',tooltip=cap).add_to(area)
        else: #Tire 4 city
            cap_location=df.loc[df['Constituency']==cap,'lat'].iloc[0],df.loc[df['Constituency']==cap,'long'].iloc[0]
            icn=folium.Icon(color='green', icon='fort-awesome', icon_color="black", prefix='fa')
            folium.Marker(cap_location,icon=icn,popup=f'<strong>Suggested capital city {cap}</strong>',tooltip=cap).add_to(area)

    
                           
    area=area._repr_html_()   #Map variable 
    return area,cap_list