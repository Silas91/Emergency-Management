import pandas as pd
from sodapy import Socrata
from datetime import date, timedelta
from arcgis import GIS

today = date.today()
offset = (today.weekday() - 3) % 7
querydate = today - timedelta(days=offset)
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')

client = Socrata(tokens.at['Data.cdc','URL'],
                 tokens.at['Data.cdc','API Key'],
                 username=tokens.at['Data.cdc','Username'],
                 password=tokens.at['Data.cdc','Password'])


results = client.get("3nnm-4jni", date_updated=str(querydate)+'T00:00:00.000', limit=4000)

# Convert to pandas DataFrame
df = pd.DataFrame.from_records(results)

gis = GIS(tokens.at['uCOP','URL'])
layer_item = gis.content.get('0bb1067e29b1446699ffdc80e46aa576')
layers = layer_item.layers
flayer = layers[0]
sdf = flayer.query().sdf
feature_keys = {row['fips']: row['objectid'] for value, row in sdf.iterrows()} #get objectids for counties
updates_to_push = [] #Create container for updates


def assemble_updates(row):
    try:
        edit_feature = {'objectid': feature_keys[row['county_fips']]}
        edit_feature['communitylevelcdc'] = row['covid_19_community_level']
        edit_feature['hospadmper100k'] = row['covid_cases_per_100k']
        edit_feature['casesper100k'] = row['covid_hospital_admissions_per_100k']
        try:
            edit_feature['hospbedsoccupied'] = float(row['covid_inpatient_bed_utilization'].replace('%',''))
        except:
            edit_feature['hospbedsoccupied'] = row['covid_inpatient_bed_utilization']
        feat = {'attributes': edit_feature}
        updates_to_push.append(feat)
    except Exception as e:
        print(row['county']+','+row['state'], e)


df.apply(lambda row: assemble_updates(row), axis=1)
update_result = flayer.edit_features(updates=updates_to_push, rollback_on_failure=False) #push the updates

office_layer_item = gis.content.get('1a85d7a8c7654036b5940d4f78a2671a')
office_layers = office_layer_item.layers
office_flayer = office_layers[0]
office_sdf = office_flayer.query().sdf
sdf = pd.merge(df, office_sdf,  how='left', left_on=['county_fips'], right_on = ['fips'])
sdf = sdf.dropna(subset=['objectid'])
updates_to_push = [] #Create container for updates

#%%

def assemble_office_updates(row):
    try:
        edit_feature = {'objectid': int(row['objectid'])}
        edit_feature['communitylevelcdc'] = row['covid_19_community_level']

        feat = {'attributes': edit_feature}
        updates_to_push.append(feat)
    except Exception as e:
        print(e)


sdf.apply(lambda row: assemble_office_updates(row), axis=1)
update_result = office_flayer.edit_features(updates=updates_to_push, rollback_on_failure=False) #push the updates
updates_to_push
