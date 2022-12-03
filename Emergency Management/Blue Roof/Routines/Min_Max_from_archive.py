from arcgis import GIS
import pandas as pd
import numpy as np
#%%
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
br_layer_item = gis.content.get('de15660be50c43beb29aad01fe4f86f4')
br_layers = br_layer_item.layers
df=br_layers[0].query().sdf
flayer = br_layers[0]
df = df.set_index('roeidpk')

df1 = df[df.datecontractordispute.isnull() & ~df.datefailedfi.isnull()]
df
index_list = list(df1.index.values)

arc = pd.read_csv(r"C:\Users\M3ECHJJJ\Downloads\axim.csv")
arc1 = arc[arc.roeidpk.isin(index_list)]
arc['dateqccomplete']=arc['dateqccomplete'].astype('datetime64[ns]')
arc4=pd.concat([arc2,arc3],axis=1)

arc2=arc.groupby(['roeidpk'], sort=False)['dateqccomplete'].min()
arc3=arc.groupby(['roeidpk'], sort=False)['dateqccomplete'].max()
arc2 = arc2.to_frame()
arc2['datecontractordisputeint'] = pd.to_datetime(arc2['datecontractordispute']).astype(np.int64)/1e6

arc2
def assemble_updates(row):
    edit_feature = {'objectid': row.name}
    edit_feature['datecontractordispute'] = int(row['datecontractordisputeint'])
    feat = {'attributes': edit_feature}
    updates_to_push.append(feat)


updates_to_push = []
adds_to_push = []
arc2.apply(lambda row: assemble_updates(row), axis=1)
update_result = flayer.edit_features(updates=updates_to_push, rollback_on_failure=False)

update
arc3=pd.to_datetime(arc3).astype(np.int64)/1e6
arc2.describe()
arc2.to_csv(r"C:\Users\M3ECHJJJ\Downloads\qccomplete.csv")
arc3 = arc2[~arc2.isnull()]
for i, v in arc3.head().items():
    flayer.edit_features(updates=[{'attributes': {'OBJECTID':i,'datefailedfi':int(v)}}], rollback_on_failure=False)
    print()
arc3

arc3.head()

arc4.columns= ['min','max']
arc4 = arc4.dropna()

arc4 = arc4[arc4['min'] !=arc4['max']]



arc4.to_csv(r"C:\Users\M3ECHJJJ\Downloads\qccomplete.csv")

arc4
