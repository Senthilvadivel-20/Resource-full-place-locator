import pandas as pd

#create data frame for added places
def Create_Data_Frame():
    lis=pd.DataFrame(columns=['city'])
    lis.to_csv('.\File\lis.csv',index=False)

lis=pd.read_csv('.\File\lis.csv')


#Add new place in new row
def add_place(place):
    try:
        idx=len(lis['city'])
    except:
        idx=0

    lis.loc[idx,'city']=place
    lisst=lis['city']
    lisst.to_csv('.\File\lis.csv',index=False)

#Get all added places
def get_city():
    lis=pd.read_csv('.\File\lis.csv')
    liss=set(lis['city'].to_list())
    liss=list(liss)
    return liss

#delete added places
def delete_city():
    lis.drop('city',inplace=True,axis=1)


