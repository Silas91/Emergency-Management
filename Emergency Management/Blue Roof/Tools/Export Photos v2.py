from arcgis.gis import GIS
import os
import zipfile
from datetime import datetime
import pandas as pd
from arcgis.features import FeatureLayer
import csv

#import csv to pandas df with sites column as index
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')

# In[9]:
gis = GIS("home")
# In[4]:
#zipName=r"D:\ROE_Package.zip"
zipName = arcpy.GetParameterAsText(0)
limiter = arcpy.GetParameterAsText(1)
# In[5]:
timestr = datetime.now().strftime("%Y%m%d%H%M%S")
n=0
while os.path.split(os.getcwd())[1] != 'bin' and n <5:
    os.chdir(os.path.dirname(os.getcwd()))
    n=n+1
pathToDownload = os.path.join(os.getcwd(),timestr)
os.mkdir(pathToDownload)
os.chdir(pathToDownload)
# In[33]:
layer_item = gis.content.get('b081489f2f2e4b4d89b4fab6833d258e')
layers = layer_item.layers
flayer = layers[0]
fset=flayer.query(where="(downloaded <> 'Yes' or downloaded is null) and flagroe='Valid'")
features = fset.features
# In[38]:
roeList = []
failList = []
for f in features[:int(limiter)]:
    i=0
    x=0
    try:
        attList = flayer.attachments.get_list(oid=f.attributes['OBJECTID'])
        for att in attList:
            if "signature" not in att['name']:
                x=x+1
                flayer.attachments.download(f.attributes['OBJECTID'],attachment_id=att['id'],save_path = pathToDownload)
                if os.path.exists(pathToDownload + '/'+att['name']) == True:
                    i=i+1
                if 'workorder' in att['name'].lower() or 'report' in att['name'].lower():
                    ext = att['name'].split(".")[-1]
                    os.rename(pathToDownload + '/'+att['name'],pathToDownload + '/ROE_'+str(f.attributes['roeidpk'])+'_WO_'+str(i)+"."+ext.lower())
                else:
                    ext = att['name'].split(".")[-1]
                    os.rename(pathToDownload + '/'+att['name'],pathToDownload + '/ROE_'+str(f.attributes['roeidpk'])+'_'+str(i)+"."+ext.lower())
        if i == x:
            roeList.append(f.attributes['OBJECTID'])
        if i != x:
            failList.append(f.attributes['OBJECTID'])
    except Exception as e:
          arcpy.AddMessage(e)
# In[53]:
try:
    mapdict = {'roeidpk':'ROE IDPK','latitude':'Latitude','longitude':'Longitude','flagroe':'Work State','invoicenumber':'Invoice Number','appfirstname':'First Name','applastname':'Last Name','appaddress':'Address','appcityname':'City Name','appzipcode':'Zip','appcountyname':'County','appstate':'State','appprimaryphone':'Primary Phone','appprimaryemail':'Primary Email','appaltcontactname':'Alterate Contact Name','appaltphone':'Alternate Phone','appaltemail':'Alternate Email','apptwostory':'Two Story','apphasdogs':'Has Dogs','appdebris':'Debris','approecomments':'ROE Comments','appcomplaintnotes':'Complaint Notes','endoflifetype':'End of Life Type','dateapplied':'Date Applied','dateendoflife':'Date End of Life','datecomplaint':'Date Complaint','datecomplaintresolved':'Date Complaint Resolved','datesenttocontractor':'Date Sent to Contractor','dateqacomplete':'Date QA Complete','datecontractordispute':'Date Contractor Dispute','datedisputeresolved':'Date Dispute Resolved','dateroofinstalled':'Date Roof Installed','dateqccomplete':'Date QC Complete','datepassedreview':'Date Passed Review','datefailedreview':'Date Failed Review','datepassedfi':'Date Passed FI','datefailedfi':'Date Failed FI','datepaid':'Date Paid','qarooftype':'QA Roof Type','qaroofsteep':'QA Roof Steep','qaplasticsheeting':'QA Plastic Sheeting','qarafters':'QA Rafters','qastructurepanels':'QA Structure Panels','qametalroof':'QA Metal Roof','qamajordebris':'QA Major Debris','qaminordebris':'QA Minor Debris','qasmallroofrepair':'QA Small Roof Repair','qalocationverified':'QA Location Verified','qanotes':'QA Notes','avnotes':'AV Notes','qccontractorname':'QC Contractor Name','qcsubcontractorname':'QC Subcontractor Name','qcdisputetype':'QC Dispute Type','qcdisputenotes':'QC Dispute Notes','qcdisputeqaname':'QC Dispute QA Name','qcdisputeownername':'QC Dispute Owner Name','qcdisputeqcname':'QC Dispute QC Name','qcadjplasticsheeting':'QC Adj Plastic Sheeting','qcadjrafterrepair':'QC Adj Rafter Repair','qcadjstructurepanels':'QC Adj Structure Panels','qcadjmetalroofrepair':'QC Adj Metal Roof Repair','qcadjmajordebris':'QC Adj Major Debris','qcadjminordebris':'QC Adj Minor Debris','qcadjsmallroofrepair':'QC Adj Small Roof Repair','address_postal':'Address Postal','qcname':'QC Name'}
    df = fset.sdf.drop(columns =['OBJECTID', 'GlobalID','downloaded','SHAPE','dateendoflife','finumofworkers','fisafetyadequate','fisafetycomments','fiplastictaut','fiplasticcomments','fiplasticwrapped','fiwrappedcomments','fiwindbattens','fibattencomments','fieligibledamage','fidamagecomments','fistructuralrepairs','fistructuralcomments','firepairsmatch','firepairscomments','fiestimategood','fiestimatecomments','ficontractorclean','ficleancomments','fiinspcomments','created_user','created_date','last_edited_user','last_edited_date','firequestnewinsp','displaystatus'])
    df = df.rename(mapdict, axis=1)
    df = df.set_index('ROE IDPK')
    df['Date Applied']=df['Date Applied'].dt.strftime('%m/%d/%Y')
    df['Date Complaint']=df['Date Complaint'].dt.strftime('%m/%d/%Y')
    df['Date Complaint Resolved']=df['Date Complaint Resolved'].dt.strftime('%m/%d/%Y')
    df['Date Sent to Contractor']=df['Date Sent to Contractor'].dt.strftime('%m/%d/%Y')
    df['Date Contractor Dispute']=df['Date Contractor Dispute'].dt.strftime('%m/%d/%Y')
    df['Date Dispute Resolved']=df['Date Dispute Resolved'].dt.strftime('%m/%d/%Y')
    df = df.head(int(limiter))
    df.to_csv('roe_list.csv', quoting=csv.QUOTE_NONNUMERIC)
except Exception as e:
    arcpy.AddMessage(e)
# In[45]:
if len(failList) >0:
    try:
        with open('Error_List.txt', 'w') as f:
            f.write('The following ROEs failed to download due to connectivity issues and will be attempted again on the next export:')
            f.write('\n')
            for line in failList:
                f.write(str(line))
                f.write('\n')
    except:
        pass
# In[ ]:
filelist =os.listdir()
with zipfile.ZipFile(zipName, 'w') as zipMe:
    for file in filelist:
        zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
for f in filelist:
    os.remove(f)
urlpath = os.path.join(os.getcwd(),zipName)
history_item = gis.content.get('52dd55754e2442b0a0b1a53fdb58de3c')
history_layers = history_item.layers
history_flayer = history_layers[0]
try:
    c = int(len(df))
except:
    c = 0
history_flayer.edit_features(adds=[{'attributes':{'zipurl':urlpath.replace('E:\\arcgisserver','https://arcservices-ucop-partners.usace.army.mil/usacearcgis/rest'),'ktr':'ThomCo','numroes':c}}])
# In[ ]:
updates_to_push = []
for roe in roeList:
    feat = {'attributes':{'OBJECTID':int(roe),'downloaded':'Yes'}}
    updates_to_push.append(feat)
update_result = flayer.edit_features(updates=updates_to_push, rollback_on_failure=False)
