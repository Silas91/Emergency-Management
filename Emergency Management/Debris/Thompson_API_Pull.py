import json
import requests
import pandas as pd
from arcgis.gis import GIS


# %%
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
url = tokens.at['Thomspon','URL']
payload = {}
headers = {'Username': tokens.at['Thomspon','Username'], 'Password': tokens.at['Thomspon','Password']}
response = requests.request("GET", url, headers=headers, data=payload)
token = response.text.replace('"', '')

# %%

url = "https://test-ace.thompsoncs.net/api/mobiletickets"
payload = {}
headers = {'Authorization': 'Bearer ' + token}
response = requests.request("GET", url, headers=headers, data=payload)

# %%

tickets = json.loads(response.text)
df = pd.json_normalize(tickets, record_path=['LoadTicketList'])
df.columns = map(str.lower, df.columns)
df = df.set_index('ticketid')

# %%

numofrecords = tickets['Total']
i = int(numofrecords / 1000) + (numofrecords % 1000 > 0)

# %%

for n in range(i - 1):
    newurl = url + "/?skip=" + str((n + 1) * 1000)
    response = requests.request("GET", newurl, headers=headers, data=payload)
    tickets = json.loads(response.text)
    globals()['df' + str(n + 1)] = pd.json_normalize(tickets, record_path=['LoadTicketList'])
    globals()['df' + str(n + 1)].columns = map(str.lower, globals()['df' + str(n + 1)].columns)
    globals()['df' + str(n + 1)] = globals()['df' + str(n + 1)].set_index('ticketid')

# %%

for x in range(i - 1):
    df = df.append(globals()['df' + str(x + 1)])

# %%


gis = GIS(tokens.at['uCOP','URL'])
layer_item = gis.content.get('d97bbd8d17e2403c9f49f6b61382dad8')
layers = layer_item.layers
flayer = layers[0]
fset = flayer.query()
sdf = pd.DataFrame.spatial.from_layer(flayer)
feature_keys = {row['ticketnumber']: row['objectid'] for value, row in sdf.iterrows()}

# %%
sdf = sdf.set_index('ticketid')
sdf = sdf.drop(columns=['objectid', 'SHAPE', 'globalid'])
df = df.drop(columns=['disposaltime', 'loadtime', 'disposaltime', 'loadtime'])

# %%

df['loadcall'] = df['loadcall'].astype(float)
df['loadcall'] = df['loadcall'].astype(str)
df['distancefromroadmarker'] = df['distancefromroadmarker'].astype(str)

# %%

def get_different_rows(source_df, new_df):
    merged_df = source_df.merge(new_df, indicator=True, how='outer')
    changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
    return changed_rows_df.drop('_merge', axis=1)
updates_df = get_different_rows(sdf, df)

# %%

def assemble_updates(row):
    try:
        edit_feature = {'objectid': feature_keys[row['ticketnumber']]}
        for col in df.columns:
            if "Time" not in col:
                edit_feature[col.lower()] = row[col]
        feat = {'geometry': {'x': row['loadlongitude'], 'y': row['loadlatitude']}, 'attributes': edit_feature}
        updates_to_push.append(feat)
    except KeyError:
        add_feature = {'ticketid': row['ticketnumber']}
        for col in df.columns:
            if "Time" not in col:
                add_feature[col.lower()] = row[col]
        feat = {'geometry': {'x': row['loadlongitude'], 'y': row['loadlatitude']}, 'attributes': add_feature}
        adds_to_push.append(feat)

# %%

updates_to_push = []
adds_to_push = []
updates_df.apply(lambda row: assemble_updates(row), axis=1)
print('Total:', len(df), 'Updates:', len(updates_to_push), 'Adds:', len(adds_to_push))
update_result = flayer.edit_features(updates=updates_to_push, adds=adds_to_push, rollback_on_failure=False)
