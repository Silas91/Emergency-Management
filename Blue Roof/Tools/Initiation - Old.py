#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import io, json
import urllib.request as request
from math import sin, cos, sqrt, atan2, radians
import numpy as np
from arcgis.gis import GIS
import arcgis as arcgis
from arcgis import geometry
from arcgis import features
from arcgis.features import SpatialDataFrame
import requests, json
import xml.etree.ElementTree as ET


# In[2]:


get_ipython().run_cell_magic('capture', '', 'from tqdm import tqdm_notebook as tqdm\ntqdm().pandas()')


# In[3]:


tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = gis = GIS(tokens.at['uCOP Partners','URL'],token = tokens.at['uCOP Partners','Token'])


# In[5]:


roe_layer_item = gis.content.get('8169ffb3c3d1414095d67bf8c1e400e4')
roe_layers = roe_layer_item.layers
roe_fset=roe_layers[0].query(where="apppapercopy='Yes' AND dateendoflife is null").sdf


# In[6]:


roe_fset.to_csv(r"D:\paper_copy_ROEs.csv")


# In[239]:


br_layer_item = gis.content.get('8169ffb3c3d1414095d67bf8c1e400e4')
#br_layer_item = gis.content.get('423bc3fea0454febbcfec588cb37cd57')
br_layers = br_layer_item.layers
br_fset=br_layers[0].query(where="initiated = 'No'")
br_features = br_fset.features
br_flayer = br_layers[0]
br_flayer


# In[240]:


def geocode(addressLine):
    addressLine = addressLine.replace(' ','%20')
    with request.urlopen(r'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?Address=' + addressLine + '&outFields=*&forStorage=false&f=pjson') as response:
        source = response.read()
        data = json.loads(source)
    y1 = data['candidates'][0].get("location",{}).get("y")
    x1 = data['candidates'][0].get("location",{}).get("x")
    number1 = data['candidates'][0].get("attributes",{}).get("AddNum")
    street1 = data['candidates'][0].get("attributes",{}).get("StName")
    city1 = data['candidates'][0].get("attributes",{}).get("City")
    state1 = data['candidates'][0].get("attributes",{}).get("Subregion")
    zip1 = data['candidates'][0].get("attributes",{}).get("Postal")
    if int(data['candidates'][0].get("score",{})) < 95:
        street1 = 'None'
        
    return x1, y1, number1, street1,  city1, state1, zip1


# In[241]:


def verifyaddress(vAddress,vCity,vZip):
    pushurl = '''http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=<AddressValidateRequest USERID="875USARM5277"><Address ID="1"><Address1></Address1><Address2>%s</Address2><City>%s</City><State></State><Zip5>%d</Zip5><Zip4></Zip4></Address></AddressValidateRequest>''' % (vAddress,vCity,vZip)
    x = requests.post(pushurl)
    return(x)


# In[242]:


recordList = []
addressHistory = []
for n in tqdm(br_features[:500]):
#for n in br_features[:1]:
    try:
        fList = []
        fList.append(n.attributes["objectid"])
        addressString = n.attributes["appaddress"]+' '+n.attributes["appcityname"]+' '+str(n.attributes["appzipcode"])
        sendAddress = addressString.replace('#','').replace("'",'')

        gX, gY, gNumber, gStreet, gCity, gState, gZipCode = geocode(sendAddress)
        #address, city, state, zipCode = reverseGeocode(fList[0],fList[1])
        fList.append(gNumber +" "+gStreet)

        fList.append(gCity)
        fList.append(gState.replace(' Parish','').replace(' County',''))
        gAddressString = gNumber + ' ' + gStreet + ' ' + gCity
        fList.append(gZipCode)
        gX1=gX
        gY1 =gY

        #if (addressString.lower() != gAddressString.lower()) or (gStreet == 'None') or (gNumber == 'None'):
        fList.append(gX)
        fList.append(gY)
        fList.append(n.attributes["objectid"])
        try:
            usps = verifyaddress(n.attributes["appaddress"],n.attributes["appcityname"],n.attributes["appzipcode"])
            fList.append(usps.text.split('Address2')[1].replace('>','').replace('</',''))
        except:
            fList.append('No Match')
        recordList.append(fList)
    except Exception as e:
        print(n.attributes["objectid"],e)


# In[243]:


for n in tqdm(recordList):
    try:
        attributes_dict = {}
        edit_feature = {}
        input_geometry = {'y':float(n[6]),
                       'x':float(n[5])}
        input_geometry = geometry.project(geometries = [input_geometry],
                                       in_sr = 4326, 
                                       out_sr = 102100,
                                       gis = gis)
        
      
        attributes_dict['objectid'] = n[7]
        attributes_dict['latitude'] = n[6]
        attributes_dict['longitude'] = n[5]
        attributes_dict['roeidpk'] = n[7]
        attributes_dict['appaddress_geocode'] = n[1]
        attributes_dict['appcityname_geocode'] = n[2]
        attributes_dict['appzipcode_geocode'] = int(n[4])
        attributes_dict['releaseroe'] = 'Active'
        attributes_dict['initiated'] = 'Yes'
        attributes_dict['address_postal'] = n[8]

        if 'None' not in n[1]:
            edit_feature['geometry'] = input_geometry[0]
        else:
            attributes_dict['flagroe'] = 'Geocode Error'
            attributes_dict['releaseroe'] = 'Inactive'
            edit_feature['geometry'] = input_geometry[0]
        
        edit_feature['attributes'] = attributes_dict
        update_result = br_flayer.edit_features(updates=[edit_feature])
        if update_result['updateResults'][0]['success'] == False:
            print('ROE#',n[7],update_result['updateResults'][0]['error'])
    except Exception as e:
        print(e)
        attributes_dict['flagroe'] = 'Geocode Error'
        attributes_dict['releaseroe'] = 'Inactive'
        edit_feature['attributes'] = attributes_dict
        update_result = br_flayer.edit_features(updates=[edit_feature])
        update_result


# In[4]:


brd_layer_item = gis.content.get('8169ffb3c3d1414095d67bf8c1e400e4')
brd_layers = brd_layer_item.layers
brd_fset=brd_layers[0].query()
brd_features = brd_fset.features
brd_flayer = brd_layers[0]
brd_flayer


# In[6]:


df = brd_fset.sdf
df = df[['roeidpk','latitude', 'longitude','releaseroe']]
df=df.sort_values('roeidpk')
df = df[df.duplicated(['latitude','longitude'])]
df = df[df.releaseroe != 'Inactive']


# In[246]:


for index, row in df.iterrows():
    attributes_dict = {}
    edit_feature = {}
    attributes_dict['objectid'] = int(row['roeidpk'])
    attributes_dict['flagroe'] = 'Duplicate'
    attributes_dict['releaseroe'] = 'Inactive'
    edit_feature['attributes'] = attributes_dict
    update_result = brd_flayer.edit_features(updates=[edit_feature])
    update_result


# In[247]:


len(recordList)


# In[ ]:




