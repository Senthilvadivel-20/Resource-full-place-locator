import folium
import pandas as pd
from geopy import distance

df=pd.read_csv('./File/class.csv')


#Generate map for added places
def map_generator(lis):
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

    cap_location=df.loc[df['Constituency']==cap,'lat'].iloc[0],df.loc[df['Constituency']==cap,'long'].iloc[0]

    area=folium.Map((cap_location),zoom_star=8)


    lis1=lis[:-1]
    last=lis[-1]

    file=open(r'./File/Edited_South.txt','r')
    w_file=open(r'./File/writed.geojson','r+')
    w_file.truncate()
    w_file.write('{"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },"features": [')
    for i in file.readlines():
        for j in lis1:
            if f'"ac_name":"{j}"' in i:
                w_file.write(i+',')   

    file=open(r'./File/Edited_South.txt','r')
    for i in file.readlines():
        if f'"ac_name":"{last}"' in i:
            w_file.write(i)


    w_file.write(']}')
    w_file.close()


    geojson=r'./File/writed.geojson'
    g=folium.GeoJson(geojson).add_to(area)
    folium.GeoJsonTooltip(fields=['ac_name']).add_to(g)

                              
    area=area._repr_html_()
    return area 

#Mark the marker in added places
def map_for_marker():
    area=folium.Map(location=[15.36855162114983, 77.64474715878777],zoom_start=5)
    geojson=r'./File/writed.geojson'
    g=folium.GeoJson(geojson).add_to(area)
    folium.GeoJsonTooltip(fields=['ac_name']).add_to(g)
    return area

