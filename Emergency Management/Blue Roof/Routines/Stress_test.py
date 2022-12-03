n = 500
t = 2

import pandas as pd
from arcgis import GIS
import random
import time
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = gis = GIS(tokens.at['uCOP Partners','URL'],token = tokens.at['uCOP Partners','Token'])
layer_item = gis.content.get('e3d41326a5bf45a98279f23dfb1b1ecc')
layers = layer_item.layers
flayer = layers[0]

df = pd.read_csv(r'C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Laura.csv')

i = 1
for index, row in df.tail(n).iterrows():
    try:
        time.sleep(t)
        add_feature = {'appfirstname':row['appfirstname'],
                                            'applastname':row['applastname'],
                                            'appfullname':row['appfullname'],
                                            'appaddress':row['appaddress'],
                                            'roeidpk':index,
                                            'dateapplied':1649075304000,
                                            'flagroe':'Valid',
                                            'appcityname':row['appcityname'],
                                            'appstate':row['appstate'],
                                            'appzipcode':int(row['appzipcode']),
                                            'appcountyname':row['appcountyname'],
                                            'flagroe':row['flagroe'],
                                            'apphasdogs':row['apphasdogs'],
                                            'apptwostory':row['apptwostory'],
                                            'appelectronicrecords':'Yes',
                                            'appconsenttosign':'Yes',
                                            'signupsource':'Online',
                                            'apphasdebris':row['appdebris'],
                                            'apphasdogsicon':row['apphasdogshex'],
                                            'apptwostoryicon':row['apptwostoryhex'],
                                            'customerid':row['customerid'],
                                            'approecomments':row['approecomments'],
                                            'appprimaryphone':row['appprimaryphone'],
                                            'appprimaryemail':row['appprimaryemail'],
                                            'qatype':random.choice(['Field','Remote']),
                                            'fitype':random.choice(['Field','Remote'])}
        feat = {'geometry':{'x':row['longitude'],'y':row['latitude']},'attributes': add_feature}
        flayer.edit_features(adds=[feat], rollback_on_failure=False)
        print(str(i)+"/"+str(n), end = "\r")
        i=i+1
    except Exception:
        pass
