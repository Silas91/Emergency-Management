#!/usr/bin/env python
# coding: utf-8
# In[26]:
from arcgis.gis import GIS
import os
from zipfile import ZipFile
from datetime import datetime
from collections import Counter
import time
from datetime import date
# In[2]:
gis = GIS("home")
# In[3]:

layer_item = gis.content.get('02d245c253be405cac9990fdddc39213')
layers = layer_item.layers
fset=layers[0].query()
flayer = layers[0]
# In[ ]:
n=0
while os.path.split(os.getcwd())[1] != 'bin' and n <5:
    os.chdir(os.path.dirname(os.getcwd()))
    n=n+1
# In[2]:
timestr = datetime.now().strftime("%Y%m%d%H%M%S")
pathToDownload = os.path.join(os.getcwd(),timestr)
os.mkdir(pathToDownload)
os.chdir(pathToDownload)
# In[3]:
inZip = arcpy.GetParameterAsText(0)
#inZip = r"D:\ROE_Package.zip"
# In[4]:
fileList = []
with ZipFile(inZip, 'r') as zip:
    for item in zip.namelist():
        fileList.append(item)
    zip.extractall()
# In[5]:
uploadlist = []
for img in fileList:
    roeidpk = img.split('_')[1]
    uploadlist.append(roeidpk)
    flayer.attachments.add(int(roeidpk), img,'qcPhotos')
    os.remove(img)
# In[20]:
photolist = dict(Counter(uploadlist))
qclist=[]
# In[22]:
for key, value in photolist.items():
    if value >2:
        qclist.append(key)
# In[27]:
updates_to_push = []
qcdate = int(time.mktime((datetime.now()).timetuple())*1000)
for roe in qclist:
    edit_feature = {'objectid': int(roe), 'dateqccomplete':qcdate}
    feat = {'attributes': edit_feature}
    updates_to_push.append(feat)
update_result = flayer.edit_features(updates=updates_to_push, rollback_on_failure=False)
