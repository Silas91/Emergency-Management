sde_connection = r"C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\Blue_Roof\artners_BlueRoof.sde"

import arcpy
import pandas as pd
from arcgis import GIS

tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
remote_group = gis.groups.search('title:DCO - Blue Roof QA', max_groups=15)[0]
df = pd.DataFrame(columns=['name','user','type'])
new_row = pd.DataFrame({'name':'Open to Anyone', 'user':'_Open', 'type':'Remote'}, index =[0])

remote_qa_list = remote_group.get_members()['users']
for i in remote_qa_list:
    rem = i.split('@')[0].lower()
    usnm = gis.users.get(username=i).fullName.replace(rem,'')
    usnm = usnm.split(', ')[1]+ '' + usnm.split(', ')[0]

    df.loc[len(df.index)] = [usnm, i,'Remote']
df_group = pd.concat([new_row, df[:]]).reset_index(drop = True)

gis = GIS("home")
field_group = gis.groups.search('title:DCO - Blue Roof - Field QA', max_groups=15)[0]
field_qa_list = field_group.get_members()['users']
for i in field_qa_list:
    usnm = (gis.users.get(username=i).fullName).replace('.civ','').replace('.',' ').title()
    df.loc[len(df.index)] = [usnm, i,'Field']

df = df.sort_values('name')
df = pd.concat([new_row, df[:]]).reset_index(drop = True)

domains = arcpy.da.ListDomains(sde_connection)
for domain in domains:
    if domain.name == 'QA_Names':
        coded_values = domain.codedValues

for index, row in df.iterrows():
    try:
        try:
            coded_values[row['user']]
            print('{0} : Exists - {0}'.format(str(index+1)+'/'+str(len(df)), row['name']+' ('+row['type']+')')), end = "\r")
        except KeyError:
            print('{0} : Adding - {0}'.format(str(index+1)+'/'+str(len(df)), row['name']+' ('+row['type']+')')), end = "\r")
            arcpy.AddCodedValueToDomain_management(sde_connection, "QA_Names", row['user'], row['name']+' ('+row['type']+')')
    except Exception:
        pass
