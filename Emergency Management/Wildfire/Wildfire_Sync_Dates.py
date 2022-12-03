from arcgis import GIS
import pandas as pd
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
layer_item = gis.content.get('2a26825c21c34e3fb12aa51b2c42d529')
layers = layer_item.layers
flayer = layers[0]
sdf=flayer.query(where = "first_visit_date is null AND number_of_visits > 0").sdf
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
tables = layer_item.tables
ftable = tables[0]
sdf_visits=ftable.query().sdf
feature_keys = {row['GlobalID']: row['OBJECTID'] for value, row in sdf.iterrows()}
for index, row in sdf.iterrows():
    try:
        rel = sdf_visits[sdf_visits['parentglobalid']==row['GlobalID']]
        maxd = rel['visit_date'].max()
        mind = rel['visit_date'].min()
        maxd = int(maxd.timestamp())*1000
        mind = int(mind.timestamp())*1000
        edit_feature = {'OBJECTID': feature_keys[rel.iloc[0]['parentglobalid']],'first_visit_date':mind,'last_visit_date':maxd}
        feat = {'attributes': edit_feature}
        updates_to_push.append(feat)
    except Exception as e:
        print(e,row['OBJECTID'])
updates_to_push = []
feature_keys
update_result = flayer.edit_features(updates=updates_to_push, rollback_on_failure=False)

updates_to_push
rel.iloc[0]['parentglobalid']
