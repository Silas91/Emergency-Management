#!/usr/bin/env python
# coding: utf-8

# In[12]:


print('Loading API')
import pandas as pd
import arcgis as arcgis
from datetime import timezone
from arcgis import geometry #use geometry module to project Long,Lat to X and Y
from copy import deepcopy
import json
import urllib.request as request
print('Logging into uCOP')
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
print('Fetching CCIR feature service')
track_layer_item = gis.content.get('3cbe1195427b47319dad679820af3388')


# In[13]:


flayer = track_layer_item.layers[0]


# In[14]:


remove_features = track_layer_item.layers[0].query(where="daterecovered is not null or datedeceased is not null",as_df=True)
remove_features = remove_features.dodi.values.tolist()


# In[15]:


EXCLUDE = pd.DataFrame({'dodi':remove_features})


# In[16]:


features = track_layer_item.layers[0].query()


# In[17]:


print('Prepping Geocoder')
def geocode(addressLine):
    try:
        addressLine = addressLine.replace(' ','%20')
        with request.urlopen(r'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?Address=' + addressLine + '&outFields=*&forStorage=false&f=pjson') as response:
            source = response.read()
            data = json.loads(source)
        y1 = data['candidates'][0].get("location",{}).get("y")
        x1 = data['candidates'][0].get("location",{}).get("x")
        return x1, y1
    except Exception as e:
        return 0,0


# In[18]:


df = pd.read_excel (r"D:\CCIR_Tracker.xlsx",'TAB 1',keep_default_na=True)


# In[19]:


df['status'] = 'Active'


# In[20]:


df = df.rename({df.columns[0]:'datereported','DODI/EDIPI Number':'dodi','MIL/DEP/   CIV/CTR':'role','CONUS/ OCONUS':'conus','Installation':'installation','City':'city','State':'state','Date Identified Infected':'dateidentified','Type of Case [C, P]':'typeofcase','In Quarantine':'inquarantine','Required Hospitalization':'requiredhospitalization','Required ICU':'requiredicu','Required  Ventilator':'requiredventilator','Currently  Hospitalized [Y, N]':'currentlyhospitalized','Currently  in ICU [Y, N]':'currentlyinicu','Currently  on Ventilator     [Y, N]':'currentlyonventilator','Date Recovered  [mm/dd/yyyy]':'daterecovered','Date Deceased [mm/dd/yyyy]':'datedeceased','Updates/Notes':'notes'}, axis=1)


# In[21]:


df = df[~df.dodi.isin(EXCLUDE.dodi)]
df = df.dropna(subset=['dodi']) 


# In[22]:


for index, row in df.iterrows():
    try:
        t_feature = [f for f in features if f.attributes['dodi']==row['dodi']][0]
        attributes_dict = {'objectid':t_feature.attributes['objectid']}
        attributes_dict['installation'] = row['installation']
        attributes_dict['role'] = row['role']
        attributes_dict['city'] = row['city']
        attributes_dict['conus'] = row['conus']
        try:
            attributes_dict['datereported'] = int(row['datereported'].replace(tzinfo=timezone.utc).timestamp())*1000+63200000
        except:
            pass
        try:
            attributes_dict['daterecovered'] = int(row['daterecovered'].replace(tzinfo=timezone.utc).timestamp())*1000+63200000
        except:
            pass
        try:
            attributes_dict['datedeceased'] = int(row['datedeceased'].replace(tzinfo=timezone.utc).timestamp())*1000+63200000
        except:
            pass
        attributes_dict['state'] = row['state']
        attributes_dict['typeofcase'] = row['typeofcase']
        attributes_dict['inquarantine'] = row['inquarantine']
        attributes_dict['requiredhospitalization'] = row['requiredhospitalization']
        attributes_dict['requiredicu'] = row['requiredicu']
        attributes_dict['requiredventilator'] = row['requiredventilator']
        attributes_dict['currentlyhospitalized'] = row['currentlyhospitalized']
        attributes_dict['currentlyinicu'] = row['currentlyinicu']
        attributes_dict['currentlyonventilator'] = row['currentlyonventilator']
        attributes_dict['notes'] = row['notes']
        if str(row['daterecovered']) != 'NaT':
            attributes_dict['status']='Recovered'
        elif str(row['datedeceased']) != 'NaT':
            attributes_dict['status']='Deceased'
        else:
            attributes_dict['status']='Active'
        
        updates_to_push = {"attributes": attributes_dict}
        update_result = flayer.edit_features(updates=[updates_to_push])
        if update_result['updateResults'][0]['success'] == False:
            print ('Error', row['dodi'])
        else:
            pass
    except Exception as e:
        if str(e) == 'list index out of range':
            try:
                print('Adding',row['dodi'])
                attributes_dict = {}
                attributes_dict['dodi'] = row['dodi']
                attributes_dict['installation'] = row['installation']
                attributes_dict['role'] = row['role']
                attributes_dict['city'] = row['city']

                attributes_dict['conus'] = row['conus']
                try:
                    attributes_dict['datereported'] = int(row['datereported'].replace(tzinfo=timezone.utc).timestamp())*1000+63200000
                except:
                    pass
                try:
                    attributes_dict['daterecovered'] = int(row['daterecovered'].replace(tzinfo=timezone.utc).timestamp())*1000+63200000
                except:
                    pass
                try:
                    attributes_dict['datedeceased'] = int(row['datedeceased'].replace(tzinfo=timezone.utc).timestamp())*1000+63200000
                except:
                    pass
                attributes_dict['state'] = row['state']
                attributes_dict['typeofcase'] = row['typeofcase']
                attributes_dict['inquarantine'] = row['inquarantine']
                attributes_dict['requiredhospitalization'] = row['requiredhospitalization']
                attributes_dict['requiredicu'] = row['requiredicu']
                attributes_dict['requiredventilator'] = row['requiredventilator']
                attributes_dict['currentlyhospitalized'] = row['currentlyhospitalized']
                attributes_dict['currentlyinicu'] = row['currentlyinicu']
                attributes_dict['currentlyonventilator'] = row['currentlyonventilator']
                attributes_dict['notes'] = row['notes']
                if str(row['daterecovered']) != 'NaT':
                    attributes_dict['status']='Recovered'
                elif str(row['datedeceased']) != 'NaT':
                    attributes_dict['status']='Deceased'
                else:
                    attributes_dict['status']='Active'
                
                x, y = geocode(row['city']+" "+str(row['state'])+" "+row['Country'])
                input_geometry = {'y':y,'x':x}
                output_geometry = geometry.project(geometries = [input_geometry],
                                           in_sr = 4326, 
                                           out_sr = 3857,
                                          gis = gis)
                updates_to_push = {"geometry":output_geometry[0],"attributes": attributes_dict}
                update_result = flayer.edit_features(adds=[updates_to_push])
                if update_result['addResults'][0]['success'] == False:
               
                    print ('Error',row['dodi'])
            except Exception as e:
                print(e)
        else:
            pass


# In[ ]:




