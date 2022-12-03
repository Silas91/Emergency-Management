#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
from arcgis.gis import GIS
#import arcgis as arcgis
from arcgis import geometry
from arcgis.features import SpatialDataFrame
import datetime as dt  
from copy import deepcopy
from functools import reduce
from datetime import datetime
from arcgis.features import FeatureLayer


# In[25]:


tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = gis = GIS(tokens.at['uCOP Partners','URL'],token = tokens.at['uCOP Partners','Token'])


# In[26]:


item = gis.content.get('8169ffb3c3d1414095d67bf8c1e400e4')
flayer = item.layers[0].query().sdf


# In[27]:


df = flayer[['releaseroe','dateapplied', 'dateavorqacomplete','qccontractorname','dateqccomplete','dateroofinstalled','datesenttocontractor','datesenttoav','dateavcomplete','dateendoflife','endoflifetype']]


# In[28]:


df['dateapplied'] = (df['dateapplied'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['dateavorqacomplete'] = (df['dateavorqacomplete'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['dateroofinstalled'] = (df['dateroofinstalled'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['datesenttocontractor'] = (df['datesenttocontractor'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['datesenttoav'] = (df['datesenttoav'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['dateavcomplete'] = (df['dateavcomplete'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['dateendoflife'] = (df['dateendoflife'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))
df['dateqccomplete'] = (df['dateqccomplete'].dt.tz_localize('UTC')
                                        .dt.tz_convert('America/Chicago')
                                        .dt.tz_localize(None))


# In[ ]:





# In[29]:


is_hdf = df['qccontractorname']=='Hughes'
hdf = df[is_hdf]
hughes_df = hdf[~hdf['releaseroe'].isin(['Inactive'])]
is_bdf = df['qccontractorname']=='Blue Tarpon'
bdf = df[is_bdf]
blue_df = bdf[~bdf['releaseroe'].isin(['Inactive'])]
active_df = df[~df['releaseroe'].isin(['Inactive'])]
total_df = df


# In[30]:


is_smadf = df['qccontractorname']=='S&M Associates'
smadf = df[is_smadf]
sma_df = smadf[~smadf['releaseroe'].isin(['Inactive'])]
sent_sma_df = sma_df['datesenttocontractor'].groupby(smadf['datesenttocontractor'].dt.to_period('D')).count()
install_sma_df = sma_df['dateroofinstalled'].groupby(smadf['dateroofinstalled'].dt.to_period('D')).count()

install_sma_df = install_sma_df.to_frame()
install_sma_df.index.names = ['Date']
install_sma_df.columns = ['SMA_Installed']
sent_sma_df = sent_sma_df.to_frame()
sent_sma_df.index.names = ['Date']
sent_sma_df.columns = ['Sent_to_SMA']


# In[31]:


is_Venegasdf = df['qccontractorname']=='Venegas'
Venegasdf = df[is_Venegasdf]
Venegas_df = Venegasdf[~Venegasdf['releaseroe'].isin(['Inactive'])]
sent_Venegas_df = Venegas_df['datesenttocontractor'].groupby(Venegasdf['datesenttocontractor'].dt.to_period('D')).count()
install_Venegas_df = Venegas_df['dateroofinstalled'].groupby(Venegasdf['dateroofinstalled'].dt.to_period('D')).count()

install_Venegas_df = install_Venegas_df.to_frame()
install_Venegas_df.index.names = ['Date']
install_Venegas_df.columns = ['Venegas_Installed']
sent_Venegas_df = sent_Venegas_df.to_frame()
sent_Venegas_df.index.names = ['Date']
sent_Venegas_df.columns = ['Sent_to_Venegas']


# In[32]:


is_Barloventodf = df['qccontractorname']=='Barlovento'
Barloventodf = df[is_Barloventodf]
Barlovento_df = Barloventodf[~Barloventodf['releaseroe'].isin(['Inactive'])]
sent_Barlovento_df = Barlovento_df['datesenttocontractor'].groupby(Barloventodf['datesenttocontractor'].dt.to_period('D')).count()
install_Barlovento_df = Barlovento_df['dateroofinstalled'].groupby(Barloventodf['dateroofinstalled'].dt.to_period('D')).count()

install_Barlovento_df = install_Barlovento_df.to_frame()
install_Barlovento_df.index.names = ['Date']
install_Barlovento_df.columns = ['Barlovento_Installed']
sent_Barlovento_df = sent_Barlovento_df.to_frame()
sent_Barlovento_df.index.names = ['Date']
sent_Barlovento_df.columns = ['Sent_to_Barlovento']


# In[33]:


is_swandf = df['qccontractorname']=='Swan'
swandf = df[is_swandf]
swan_df = swandf[~swandf['releaseroe'].isin(['Inactive'])]
sent_swan_df = swan_df['datesenttocontractor'].groupby(swandf['datesenttocontractor'].dt.to_period('D')).count()
install_swan_df = swan_df['dateroofinstalled'].groupby(swandf['dateroofinstalled'].dt.to_period('D')).count()

install_swan_df = install_swan_df.to_frame()
install_swan_df.index.names = ['Date']
install_swan_df.columns = ['Swan_Installed']
sent_swan_df = sent_swan_df.to_frame()
sent_swan_df.index.names = ['Date']
sent_swan_df.columns = ['Sent_to_Swan']


# In[34]:


is_ThomCodf = df['qccontractorname']=='ThomCo'
ThomCodf = df[is_ThomCodf]
ThomCo_df = ThomCodf[~ThomCodf['releaseroe'].isin(['Inactive'])]
sent_ThomCo_df = ThomCo_df['datesenttocontractor'].groupby(ThomCodf['datesenttocontractor'].dt.to_period('D')).count()
install_ThomCo_df = ThomCo_df['dateroofinstalled'].groupby(ThomCodf['dateroofinstalled'].dt.to_period('D')).count()

install_ThomCo_df = install_ThomCo_df.to_frame()
install_ThomCo_df.index.names = ['Date']
install_ThomCo_df.columns = ['ThomCo_Installed']
sent_ThomCo_df = sent_ThomCo_df.to_frame()
sent_ThomCo_df.index.names = ['Date']
sent_ThomCo_df.columns = ['Sent_to_ThomCo']


# In[35]:


is_pidf = df['qccontractorname']=='Power & Instrumentation'
pidf = df[is_pidf]
pi_df = pidf[~pidf['releaseroe'].isin(['Inactive'])]
sent_pi_df = pi_df['datesenttocontractor'].groupby(pidf['datesenttocontractor'].dt.to_period('D')).count()
install_pi_df = pi_df['dateroofinstalled'].groupby(pidf['dateroofinstalled'].dt.to_period('D')).count()

install_pi_df = install_pi_df.to_frame()
install_pi_df.index.names = ['Date']
install_pi_df.columns = ['pi_Installed']
sent_pi_df = sent_pi_df.to_frame()
sent_pi_df.index.names = ['Date']
sent_pi_df.columns = ['Sent_to_pi']


# In[36]:


is_Yerkesdf = df['qccontractorname']=='Yerkes South'
Yerkesdf = df[is_Yerkesdf]
Yerkes_df = Yerkesdf[~Yerkesdf['releaseroe'].isin(['Inactive'])]
sent_Yerkes_df = Yerkes_df['datesenttocontractor'].groupby(Yerkesdf['datesenttocontractor'].dt.to_period('D')).count()
install_Yerkes_df = Yerkes_df['dateroofinstalled'].groupby(Yerkesdf['dateroofinstalled'].dt.to_period('D')).count()

install_Yerkes_df = install_Yerkes_df.to_frame()
install_Yerkes_df.index.names = ['Date']
install_Yerkes_df.columns = ['Yerkes_Installed']
sent_Yerkes_df = sent_Yerkes_df.to_frame()
sent_Yerkes_df.index.names = ['Date']
sent_Yerkes_df.columns = ['Sent_to_Yerkes']


# In[37]:


is_Ceresdf = df['qccontractorname']=='Ceres Environmental'
Ceresdf = df[is_Ceresdf]
Ceres_df = Ceresdf[~Ceresdf['releaseroe'].isin(['Inactive'])]
sent_Ceres_df = Ceres_df['datesenttocontractor'].groupby(Ceresdf['datesenttocontractor'].dt.to_period('D')).count()
install_Ceres_df = Ceres_df['dateroofinstalled'].groupby(Ceresdf['dateroofinstalled'].dt.to_period('D')).count()

install_Ceres_df = install_Ceres_df.to_frame()
install_Ceres_df.index.names = ['Date']
install_Ceres_df.columns = ['Ceres_Installed']
sent_Ceres_df = sent_Ceres_df.to_frame()
sent_Ceres_df.index.names = ['Date']
sent_Ceres_df.columns = ['Sent_to_Ceres']


# In[38]:


is_Crowndf = df['qccontractorname']=='Crown'
Crowndf = df[is_Crowndf]
Crown_df = Crowndf[~Crowndf['releaseroe'].isin(['Inactive'])]
sent_Crown_df = Crown_df['datesenttocontractor'].groupby(Crowndf['datesenttocontractor'].dt.to_period('D')).count()
install_Crown_df = Crown_df['dateroofinstalled'].groupby(Crowndf['dateroofinstalled'].dt.to_period('D')).count()

install_Crown_df = install_Crown_df.to_frame()
install_Crown_df.index.names = ['Date']
install_Crown_df.columns = ['Crown_Installed']
sent_Crown_df = sent_Crown_df.to_frame()
sent_Crown_df.index.names = ['Date']
sent_Crown_df.columns = ['Sent_to_Crown']


# In[39]:


is_SLSCOdf = df['qccontractorname']=='SLSCO'
SLSCOdf = df[is_SLSCOdf]
SLSCO_df = SLSCOdf[~SLSCOdf['releaseroe'].isin(['Inactive'])]
sent_SLSCO_df = SLSCO_df['datesenttocontractor'].groupby(SLSCOdf['datesenttocontractor'].dt.to_period('D')).count()
install_SLSCO_df = SLSCO_df['dateroofinstalled'].groupby(SLSCOdf['dateroofinstalled'].dt.to_period('D')).count()

install_SLSCO_df = install_SLSCO_df.to_frame()
install_SLSCO_df.index.names = ['Date']
install_SLSCO_df.columns = ['SLSCO_Installed']
sent_SLSCO_df = sent_SLSCO_df.to_frame()
sent_SLSCO_df.index.names = ['Date']
sent_SLSCO_df.columns = ['Sent_to_SLSCO']


# In[40]:


is_Dynamicdf = df['qccontractorname']=='Dynamic'
Dynamicdf = df[is_Dynamicdf]
Dynamic_df = Dynamicdf[~Dynamicdf['releaseroe'].isin(['Inactive'])]
sent_Dynamic_df = Dynamic_df['datesenttocontractor'].groupby(Dynamicdf['datesenttocontractor'].dt.to_period('D')).count()
install_Dynamic_df = Dynamic_df['dateroofinstalled'].groupby(Dynamicdf['dateroofinstalled'].dt.to_period('D')).count()

install_Dynamic_df = install_Dynamic_df.to_frame()
install_Dynamic_df.index.names = ['Date']
install_Dynamic_df.columns = ['Dynamic_Installed']
sent_Dynamic_df = sent_Dynamic_df.to_frame()
sent_Dynamic_df.index.names = ['Date']
sent_Dynamic_df.columns = ['Sent_to_Dynamic']


# In[41]:


submits = active_df['dateapplied'].groupby(df['dateapplied'].dt.to_period('D')).count()
total = total_df['dateapplied'].groupby(df['dateapplied'].dt.to_period('D')).count()
qa = active_df['dateavorqacomplete'].groupby(df['dateavorqacomplete'].dt.to_period('D')).count()
ri = active_df['dateroofinstalled'].groupby(df['dateroofinstalled'].dt.to_period('D')).count()
sktr = active_df['datesenttocontractor'].groupby(df['datesenttocontractor'].dt.to_period('D')).count()
sent_hughes_df = hughes_df['datesenttocontractor'].groupby(hdf['datesenttocontractor'].dt.to_period('D')).count()
sent_blue_df = blue_df['datesenttocontractor'].groupby(bdf['datesenttocontractor'].dt.to_period('D')).count()
sav = active_df['datesenttoav'].groupby(df['datesenttoav'].dt.to_period('D')).count()
avc = active_df['dateavcomplete'].groupby(df['dateavcomplete'].dt.to_period('D')).count()
el = df['dateendoflife'].groupby(df['dateendoflife'].dt.to_period('D')).count()
install_hughes_df = hughes_df['dateroofinstalled'].groupby(hdf['dateroofinstalled'].dt.to_period('D')).count()
install_blue_df = blue_df['dateroofinstalled'].groupby(bdf['dateroofinstalled'].dt.to_period('D')).count()


# In[42]:


submits = submits.to_frame()
submits.index.names = ['Date']

submits.columns = ['New_ROEs']
submits.reset_index(inplace=True)
qa = qa.to_frame()
qa.index.names = ['Date']
qa.columns = ['QA_Complete']
ri = ri.to_frame()
ri.index.names = ['Date']
ri.columns = ['Roofs_Installed']
skr = sktr.to_frame()
skr.index.names = ['Date']
sktr.columns = ['Sent_to_Ktr']
sav = sav.to_frame()
sav.index.names = ['Date']
sav.columns = ['Sent_to_AV']
avc = avc.to_frame()
avc.index.names = ['Date']
avc.columns = ['AV_Complete']
el = el.to_frame()
el.index.names = ['Date']
el.columns = ['Dropped']
install_hughes_df = install_hughes_df.to_frame()
install_hughes_df.index.names = ['Date']
install_hughes_df.columns = ['Hughes_Installed']
install_blue_df = install_blue_df.to_frame()
install_blue_df.index.names = ['Date']
install_blue_df.columns = ['BR_Installed']
sent_blue_df = sent_blue_df.to_frame()
sent_blue_df.index.names = ['Date']
sent_blue_df.columns = ['Sent_to_BR']
sent_hughes_df = sent_hughes_df.to_frame()
sent_hughes_df.index.names = ['Date']
sent_hughes_df.columns = ['Sent_to_Hughes']
df = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],how='outer'), [submits,qa,ri,sktr,sav,avc,el,install_hughes_df,install_blue_df,sent_hughes_df,sent_blue_df,install_sma_df,sent_sma_df,install_Venegas_df,sent_Venegas_df,install_Barlovento_df,sent_Barlovento_df,install_swan_df,sent_swan_df,install_ThomCo_df,sent_ThomCo_df,install_pi_df,sent_pi_df,install_Yerkes_df,sent_Yerkes_df,install_Ceres_df,sent_Ceres_df,install_Crown_df,sent_Crown_df,install_SLSCO_df,sent_SLSCO_df,install_Dynamic_df,sent_Dynamic_df])
df=df.sort_values('Date')
df.set_index('Date', inplace=True)


# In[43]:


df = df.fillna(0)
df['New_ROEs'] = df['New_ROEs'].cumsum()
df['Roofs_Installed'] = df['Roofs_Installed'].cumsum()
df['QA_Complete'] = df['QA_Complete'].cumsum()
df['datesenttocontractor'] = df['datesenttocontractor'].cumsum()
df['Sent_to_AV'] = df['Sent_to_AV'].cumsum()
df['AV_Complete'] = df['AV_Complete'].cumsum()
df['Dropped'] = df['Dropped'].cumsum()
df['Hughes_Installed'] = df['Hughes_Installed'].cumsum()
df['BR_Installed'] = df['BR_Installed'].cumsum()
df['Sent_to_Hughes'] = df['Sent_to_Hughes'].cumsum()
df['Sent_to_BR'] = df['Sent_to_BR'].cumsum()
df['Sent_to_SMA'] = df['Sent_to_SMA'].cumsum()
df['SMA_Installed'] = df['SMA_Installed'].cumsum()

df['Sent_to_Venegas'] = df['Sent_to_Venegas'].cumsum()
df['Venegas_Installed'] = df['Venegas_Installed'].cumsum()

df['Sent_to_Barlovento'] = df['Sent_to_Barlovento'].cumsum()
df['Barlovento_Installed'] = df['Barlovento_Installed'].cumsum()

df['Sent_to_Swan'] = df['Sent_to_Swan'].cumsum()
df['Swan_Installed'] = df['Swan_Installed'].cumsum()

df['Sent_to_ThomCo'] = df['Sent_to_ThomCo'].cumsum()
df['ThomCo_Installed'] = df['ThomCo_Installed'].cumsum()

df['Sent_to_pi'] = df['Sent_to_pi'].cumsum()
df['pi_Installed'] = df['pi_Installed'].cumsum()

df['Sent_to_Yerkes'] = df['Sent_to_Yerkes'].cumsum()
df['Yerkes_Installed'] = df['Yerkes_Installed'].cumsum()

df['Sent_to_Ceres'] = df['Sent_to_Ceres'].cumsum()
df['Ceres_Installed'] = df['Ceres_Installed'].cumsum()

df['Sent_to_Crown'] = df['Sent_to_Crown'].cumsum()
df['Crown_Installed'] = df['Crown_Installed'].cumsum()

df['Sent_to_SLSCO'] = df['Sent_to_SLSCO'].cumsum()
df['SLSCO_Installed'] = df['SLSCO_Installed'].cumsum()

df['Sent_to_Dynamic'] = df['Sent_to_Dynamic'].cumsum()
df['Dynamic_Installed'] = df['Dynamic_Installed'].cumsum()


# In[44]:


layer_item = gis.content.get('f30cd5e8f6964f3dae1838c5bf496729')
#layer_item = gis.content.get('47bb0ca6440c4634b70be0261ce7e34e')
layers = layer_item.layers
fset=layers[0].query()
features = fset.features
flayer = layers[0]
flayer


# In[45]:


import time


# In[46]:


for index, row in df.iterrows():
    attributes_dict = {}
    push_feature = {}
    try:
        t_feature = [f for f in features if datetime.utcfromtimestamp(int(f.attributes['recorddate']/1000)).strftime('%Y-%m-%d')==str(index)][0]
        attributes_dict['objectid'] = t_feature.attributes['objectid']
        attributes_dict['roesubmitted'] = int(row['New_ROEs'])
        attributes_dict['qacomplete'] = int(row['QA_Complete'])
        attributes_dict['roofinstalledqc'] = int(row['Roofs_Installed'])
        attributes_dict['avcompleted'] = int(row['AV_Complete'])
        attributes_dict['dropped'] = int(row['Dropped'])
        attributes_dict['hughesinstalled'] = int(row['Hughes_Installed'])
        attributes_dict['bluetarponinstalled'] = int(row['BR_Installed'])
        attributes_dict['senttoav'] = int(row['Sent_to_AV'])
        attributes_dict['senttohughes'] = int(row['Sent_to_Hughes'])
        attributes_dict['senttobluetarpon'] = int(row['Sent_to_BR'])
        attributes_dict['senttobluetarpon'] = int(row['Sent_to_SMA'])
        attributes_dict['bluetarponinstalled'] = int(row['SMA_Installed'])

        attributes_dict['senttobluetarpon'] = int(row['Sent_to_Venegas'] )
        attributes_dict['bluetarponinstalled'] = int(row['Venegas_Installed'] )

        attributes_dict['senttobluetarpon'] = int(row['Sent_to_Barlovento'] )
        attributes_dict['bluetarponinstalled'] = int(row['Barlovento_Installed'] )

        attributes_dict['senttoswan'] = int(row['Sent_to_Swan'] )
        attributes_dict['swaninstalled'] = int(row['Swan_Installed'] )

        attributes_dict['senttothomco'] = int(row['Sent_to_ThomCo'] )
        attributes_dict['thomcoinstalled'] = int(row['ThomCo_Installed'] )

        attributes_dict['senttopi'] = int(row['Sent_to_pi'] )
        attributes_dict['piinstalled'] = int(row['pi_Installed'] )

        attributes_dict['senttoyerkes'] = int(row['Sent_to_Yerkes'] )
        attributes_dict['yerkesinstalled'] = int(row['Yerkes_Installed'] )

        attributes_dict['senttoceres'] = int(row['Sent_to_Ceres'] )
        attributes_dict['ceresinstalled'] = int(row['Ceres_Installed'] )
        attributes_dict['senttovenegas'] = int(row['Sent_to_Venegas'] )
        attributes_dict['venegasinstalled'] = int(row['Venegas_Installed'] )

        attributes_dict['senttocrown'] = int(row['Sent_to_Crown'] )
        attributes_dict['crowninstalled'] = int(row['Crown_Installed'] )

        attributes_dict['senttoslsco'] = int(row['Sent_to_SLSCO'] )
        attributes_dict['slscoinstalled'] = int(row['SLSCO_Installed'] )

        attributes_dict['senttodynamic'] = int(row['Sent_to_Dynamic'] )
        attributes_dict['dynamicinstalled'] = int(row['Dynamic_Installed'] )

        push_feature['attributes']=attributes_dict
        update_result = flayer.edit_features(updates=[push_feature])
        if update_result['updateResults'][0]['success'] ==True:
            print(str(index), 'Updated')
        else:
            print(str(index),update_result['updateResults'][0]['error'])
    except Exception as e:
        date_time = int(time.mktime(datetime.strptime(str(index), "%Y-%m-%d").timetuple()))*1000+43200000
        attributes_dict['recorddate'] = date_time
        attributes_dict['roesubmitted'] = int(row['New_ROEs'])
        attributes_dict['qacomplete'] = int(row['QA_Complete'])
        attributes_dict['roofinstalledqc'] = int(row['Roofs_Installed'])
        attributes_dict['avcompleted'] = int(row['AV_Complete'])
        attributes_dict['hughesinstalled'] = int(row['Hughes_Installed'])
        attributes_dict['bluetarponinstalled'] = int(row['BR_Installed'])
        attributes_dict['dropped'] = int(row['Dropped'])
        attributes_dict['senttoav'] = int(row['Sent_to_AV'])
        attributes_dict['senttohughes'] = int(row['Sent_to_Hughes'])
        attributes_dict['senttobluetarpon'] = int(row['Sent_to_BR'])
        attributes_dict['senttobluetarpon'] = int(row['Sent_to_SMA'] )
        attributes_dict['bluetarponinstalled'] = int(row['SMA_Installed'] )

        attributes_dict['senttobluetarpon'] = int(row['Sent_to_Venegas'] )
        attributes_dict['bluetarponinstalled'] = int(row['Venegas_Installed'] )

        attributes_dict['senttobluetarpon'] = int(row['Sent_to_Barlovento'] )
        attributes_dict['bluetarponinstalled'] = int(row['Barlovento_Installed'] )

        attributes_dict['senttoswan'] = int(row['Sent_to_Swan'] )
        attributes_dict['swaninstalled'] = int(row['Swan_Installed'] )

        attributes_dict['senttothomco'] = int(row['Sent_to_ThomCo'] )
        attributes_dict['thomcoinstalled'] = int(row['ThomCo_Installed'] )

        attributes_dict['senttopi'] = int(row['Sent_to_pi'] )
        attributes_dict['piinstalled'] = int(row['pi_Installed'] )

        attributes_dict['senttoyerkes'] = int(row['Sent_to_Yerkes'] )
        attributes_dict['yerkesinstalled'] = int(row['Yerkes_Installed'] )
        
        
        attributes_dict['senttovenegas'] = int(row['Sent_to_Venegas'] )
        attributes_dict['venegasinstalled'] = int(row['Venegas_Installed'] )

        attributes_dict['senttoceres'] = int(row['Sent_to_Ceres'] )
        attributes_dict['ceresinstalled'] = int(row['Ceres_Installed'] )

        attributes_dict['senttocrown'] = int(row['Sent_to_Crown'] )
        attributes_dict['crowninstalled'] = int(row['Crown_Installed'] )

        attributes_dict['senttoslsco'] = int(row['Sent_to_SLSCO'] )
        attributes_dict['slscoinstalled'] = int(row['SLSCO_Installed'] )

        attributes_dict['senttodynamic'] = int(row['Sent_to_Dynamic'] )
        attributes_dict['dynamicinstalled'] = int(row['Dynamic_Installed'] )

        push_feature['attributes']=attributes_dict
        update_result = flayer.edit_features(adds = [push_feature])
        if update_result['addResults'][0]['success'] ==True:
            print(str(index), 'Added')
        else:
            print(str(index),update_result['addResults'][0]['error'])


# In[ ]:




