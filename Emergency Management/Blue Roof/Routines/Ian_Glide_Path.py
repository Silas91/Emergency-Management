import pandas as pd
import plotly.express as px
import os
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from arcgis import GIS
pd.set_option('display.max_rows', None)
# %% Prep  Data

tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
item = gis.content.get('15be8f369317463cb19a619c5bcc7c60')
layers = item.layers
flayer = layers[0]
df= flayer.query().sdf


df['dateapplied'] = pd.to_datetime(df['dateapplied']).dt.tz_localize('UTC').tz_convert("US/Eastern")
df['dateendoflife'] = pd.to_datetime(df['dateendoflife'])
df['dateqccomplete'] = pd.to_datetime(df['dateqccomplete'])
df['dateqacomplete'] = pd.to_datetime(df['dateqacomplete'])
df['dateavqacomplete'] = pd.to_datetime(df['dateavqacomplete'])
df['dateavqafail'] = pd.to_datetime(df['dateavqafail'])
df['datesenttoav'] = pd.to_datetime(df['datesenttoav'])
df['dateavcomplete'] = pd.to_datetime(df['dateavcomplete'])
df['dateavfail'] = pd.to_datetime(df['dateavfail'])

df['datesenttocontractor'] = pd.to_datetime(df['datesenttocontractor'])
df['datepaid'] = pd.to_datetime(df['datepaid'])
df['datepassedfi'] = pd.to_datetime(df['datepassedfi'])


# %%


# %% Go ahead and get dates in order to set mission dates
Ian_date_applied = df.groupby(df['dateapplied'].dt.date).size()
Ian_endoflife = df.groupby(df['dateendoflife'].dt.date).size()
Ian_installs = df.groupby(df['dateqccomplete'].dt.date).size()
Ian_qa = df.groupby(df['dateqacomplete'].dt.date).size()
Ian_avqa = df.groupby(df['dateavqacomplete'].dt.date).size()
Ian_avqafail = df.groupby(df['dateavqafail'].dt.date).size()
Ian_sentav = df[df['avcontractorname']=='CMC'].groupby(df['datesenttoav'].dt.date).size()
Ian_av = df[df['avcontractorname']=='CMC'].groupby(df['dateavcomplete'].dt.date).size()
Ian_avfail = df.groupby(df['dateavfail'].dt.date).size()

Ian_sentqc = df.groupby(df['datesenttocontractor'].dt.date).size()
Ian_paid = df.groupby(df['datepaid'].dt.date).size()
Ian_fi = df.groupby(df['datepassedfi'].dt.date).size()

# %% Set Mission Dates
#Ian_idx = pd.date_range(Ian_date_applied.index[0], Ian_installs.index[-1])
Ian_idx = pd.date_range(start='10-3-2022', periods=30,freq='D')

#%%
Ian_date_applied = Ian_date_applied.reindex(Ian_idx, fill_value=0)
Ian_date_applied = Ian_date_applied.reset_index(drop=True)
Ian_date_applied=Ian_date_applied.to_frame()
Ian_date_applied.columns=['applied']

Ian_endoflife = Ian_endoflife.reindex(Ian_idx, fill_value=0)
Ian_endoflife = Ian_endoflife.reset_index(drop=True)
Ian_endoflife=Ian_endoflife.to_frame()
Ian_endoflife.columns=['endoflife']

Ian_installs = Ian_installs.reindex(Ian_idx, fill_value=0)
Ian_installs = Ian_installs.reset_index(drop=True)
Ian_installs=Ian_installs.to_frame()
Ian_installs.columns=['qcomplete']

Ian_qa = Ian_qa.reindex(Ian_idx, fill_value=0)
Ian_qa = Ian_qa.reset_index(drop=True)
Ian_qa=Ian_qa.to_frame()
Ian_qa.columns=['qacomplete']

Ian_avqa = Ian_avqa.reindex(Ian_idx, fill_value=0)
Ian_avqa = Ian_avqa.reset_index(drop=True)
Ian_avqa=Ian_avqa.to_frame()
Ian_avqa.columns=['remoteqacomplete']

Ian_avqafail = Ian_avqafail.reindex(Ian_idx, fill_value=0)
Ian_avqafail = Ian_avqafail.reset_index(drop=True)
Ian_avqafail=Ian_avqafail.to_frame()
Ian_avqafail.columns=['remoteqafail']

Ian_sentav = Ian_sentav.reindex(Ian_idx, fill_value=0)
Ian_sentav = Ian_sentav.reset_index(drop=True)
Ian_sentav=Ian_sentav.to_frame()
Ian_sentav.columns=['sentav']

Ian_av = Ian_av.reindex(Ian_idx, fill_value=0)
Ian_av = Ian_av.reset_index(drop=True)
Ian_av=Ian_av.to_frame()
Ian_av.columns=['avcompl']

Ian_avfail = Ian_avfail.reindex(Ian_idx, fill_value=0)
Ian_avfail = Ian_avfail.reset_index(drop=True)
Ian_avfail=Ian_avfail.to_frame()
Ian_avfail.columns=['avfail']

Ian_sentqc = Ian_sentqc.reindex(Ian_idx, fill_value=0)
Ian_sentqc = Ian_sentqc.reset_index(drop=True)
Ian_sentqc=Ian_sentqc.to_frame()
Ian_sentqc.columns=['sentqc']

Ian_paid = Ian_paid.reindex(Ian_idx, fill_value=0)
Ian_paid = Ian_paid.reset_index(drop=True)
Ian_paid=Ian_paid.to_frame()
Ian_paid.columns=['paid']

Ian_fi = Ian_fi.reindex(Ian_idx, fill_value=0)
Ian_fi = Ian_fi.reset_index(drop=True)
Ian_fi=Ian_fi.to_frame()
Ian_fi.columns=['fipassed']


inner_merged = pd.concat([Ian_fi, Ian_paid,Ian_sentqc,Ian_avfail,Ian_av,Ian_sentav,Ian_avqafail,Ian_avqa,Ian_qa,Ian_installs,Ian_date_applied], axis=1)

Ian_date_applied
