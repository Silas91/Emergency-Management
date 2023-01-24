#%%
PDF_FOLDER_PATH = r"C:\Users\M3ECHJJJ\Downloads\UNPROCESSED_PDF"
PROCESSED_PDF_FOLDER_PATH = r"C:\Users\M3ECHJJJ\Downloads\PROCESSED_PDF"

from PyPDF2 import PdfReader
import re, os, shutil
import pandas as pd
from arcgis.gis import GIS

df = pd.DataFrame()

columns={'ma':'MA  Task','rrf':'Other Tracking','ddt':'Date  Time Received',
    'requestor':'Requestor','telephone':'Telephone','description':'Description of Task',
    'acctoff':'Accepting Official Federal Agency Action Officer','fedaddress':'Address',
    'phone':'Phone','fax':'FaxEMail','comments':'COMMENTS use back or separate page for additional space','mano':'DR',
    'begin':'Beginning Date','comp':'Completion Date','cost':'Cost Estimate','email':'Email','supporting':'Check Box1',
    'ofa':'OFA','manager':"Project Officer's"}

priority_map = {'Check Box3': 'Normal', 'Check Box4': 'High', 'Check Box5': 'Life Saving', 'Check Box6': 'Life Sustaining'}

#%% get files in folder and loop through them
for file in os.listdir(PDF_FOLDER_PATH):
    #read pdf
    if file.endswith(".pdf"):
        inputFile = os.path.join(PDF_FOLDER_PATH, file)
    else:
        continue
    fo = open(inputFile, "rb")
    pdf_reader = PdfReader(fo)
    data = pdf_reader.get_fields()
    print(inputFile)
    #loop through columns
    for key, value in columns.items():
        try:
            locals()[key] = data[value]['/V']
        except:
            locals()[key] = None

    # get priority

    for c, p in priority_map.items():
        try:
            if data[c]['/V'] == '/Yes':
                priority = p
                break
        except:
            pass

    tasks = description.split('Location')
    for i in tasks[1:]:
        coordinate_pair = re.findall(r'\((.*?)\)',i)[0].split(' ')
        lat = float(coordinate_pair[0])
        lon = abs(float(coordinate_pair[-1]))*-1
        addr = re.findall(r':(.*?)\(',i)[0].strip()
        poc = i.split('POC: ')[-1].split(',')
        name = poc[0].strip()
        phone = poc[1].strip()
        email = poc[2].strip()
        df = df.append({'site_lat':lat,'site_lon':lon,'site_address':addr,'site_poc':name,'site_phone':phone,'site_email':email,'ma':ma,'rrf':rrf,'ddt':ddt,'requestor':requestor,'telephone':telephone,'description':description,'acctoff':acctoff,'fedaddress':fedaddress,'phone':phone,'fax':fax,'comments':comments,'mano':mano,'begin':begin,'comp':comp,'cost':cost,'email':email,'supporting':supporting,'priority':priority,'file_location':inputFile.replace(PDF_FOLDER_PATH,PROCESSED_PDF_FOLDER_PATH)},ignore_index=True)
    fo.close()
    shutil.move(inputFile,os.path.join(PROCESSED_PDF_FOLDER_PATH,file))
    #%% move the inputfile to the processed folder

    
    
#%% connect to layer 5c704bf32954460f9b96a7b136d7164b in ucop

gis = GIS("https://arcportal-ucop-corps.usace.army.mil/s0portal")
layer = gis.content.get('5c704bf32954460f9b96a7b136d7164b')
flayer = layer.layers[0]
#%%


def assemble_updates(row):  
    add_feature = {}  
    for col in df.columns: 
        add_feature[col] = row[col]  
    feat = {'geometry':{'x':row['site_lon'],'y':row['site_lat']},'attributes': add_feature} #append object into list  
    adds_to_push.append(feat) #append object into list  
  
updates_to_push = [] #Create list of all update objects to push  
adds_to_push = [] #Create list of all insert objects to push  
df.apply(lambda row: assemble_updates(row), axis=1) #apply the assumble updates function to DF

#%%
update_result = flayer.edit_features( adds=adds_to_push, rollback_on_failure=False) #Commit the update and insert lists
# %%
update_result
# %%
update_result
# %%
