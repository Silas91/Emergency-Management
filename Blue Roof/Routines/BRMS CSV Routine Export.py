from arcgis import GIS
import pandas as pd
from datetime import datetime
timestr = datetime.now().strftime("%Y%m%d_%H%M")
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
  
filename = 'ROE_Export_'+timestr+'.csv'
layer_item = gis.content.get('b1d4d1613d1340ed9ae416362a0a4730')
layers = layer_item.layers
flayer = layers[0]
df=flayer.query().sdf
df.to_csv(r'\\nwk-netapp2.nwk.ds.usace.army.mil\MISSIONFILES\MissionProjects\civ\Temporary Roofing\10.0 FMS\Exports/'+filename)
