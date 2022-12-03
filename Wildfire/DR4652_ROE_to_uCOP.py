print('Importing Modules')
import pandas as pd
from arcgis import *
from arcgis.gis import server
from arcgis.features import FeatureLayerCollection
print('Connecting to NM ROE Layer')
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
server_base_url = tokens.at['EPA Fire','URL']
gis_server = server.Server(url=f"{server_base_url}/epar6gis/",
                    token_url=f"{server_base_url}/epar6gis/tokens/generateToken",
                    username= tokens.at['EPA Fire','Username'],
                    password= tokens.at['EPA Fire','Password'])

content_dir = gis_server.content
service = content_dir.get('R6NMWildfires_ROE_Properties_USACE',folder="NMFires2022_USACE_Share")
pd.set_option('display.max_rows', None)
print('Connecting to uCOP Layer')
sdf = pd.DataFrame.spatial.from_layer(service.layers[0])


gis = GIS(tokens.at['uCOP','URL'])
layer_item = gis.content.get('2a26825c21c34e3fb12aa51b2c42d529')
layers = layer_item.layers
flayer = layers[0]
sdf_ucop=flayer.query().sdf

feature_keys = {row['propertyunique_id']: row['OBJECTID'] for value, row in sdf_ucop.iterrows()}
apn_keys = {row['Property_Address']: row['PropertyUnique_ID'] for value, row in sdf.iterrows()}

# %%
print('Processing Data')
def assemble_updates(row):
    try:
        edit_feature = {'OBJECTID': feature_keys[row['PropertyUnique_ID']]}

    except Exception as e:
        print(e)
        add_feature = {'propertyunique_id': row['PropertyUnique_ID']}
        add_feature['secondary_id']=row['Secondary_ID']
        try:
            add_feature['property_address']=row['Property_Address']+' '+row['Porperty_Address_UnitNo']
        except:
            add_feature['property_address']=row['Property_Address']
        add_feature['city']=row['City']
        add_feature['county']=row['County']
        add_feature['latitude']=row['Latitude']
        add_feature['apn']=row['PropertyUnique_ID']
        add_feature['longitude']=row['Longitude']
        add_feature['parcel_status']=row['Operational_Status']
        try:
            add_feature['site_address_concern']=row['HealthSafety'].capitalize()
        except:
            pass
        feat = {'geometry': {'x': row['Longitude'], 'y': row['Latitude']}, 'attributes': add_feature}
        adds_to_push.append(feat)

# %%

updates_to_push = []
adds_to_push = []
sdf.apply(lambda row: assemble_updates(row), axis=1)
print('Total ROE Tracked:', len(sdf), '\nROEs to Add:', len(adds_to_push))
update_result = flayer.edit_features(adds=adds_to_push, rollback_on_failure=False)
print('Sync Complete')
adds_to_push
