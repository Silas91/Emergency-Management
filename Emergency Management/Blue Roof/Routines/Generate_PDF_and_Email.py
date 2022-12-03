import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import docx, datetime, os, shutil, smtplib, string, ssl
from docx import Document
from docx.shared import Inches
from docxtpl import DocxTemplate
import win32com.client as client
import pandas as pd
from arcgis import GIS
from tqdm.notebook import tqdm_notebook
from tqdm import tqdm
pathToDownload = r'C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Signatures'
template = r"C:\Users\M3ECHJJJ\Downloads\ROE.docx"
roeFolder = r'C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Reports'


host = 'SMTP.USACE.ARMY.MIL'
port = 25
sender = 'no-reply@usace.army.mil'
#%%
tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = GIS(tokens.at['uCOP','URL'])
br_layer_item = gis.content.get('7b8ecfaf5c2b43cba2adfd0a86bbef06')
br_layers = br_layer_item.layers
df=br_layers[0].query(where="flagroe <>'Deleted'").sdf

#df=br_layers[0].query(where="flagroe <>'Deleted'").sdf
flayer = br_layers[0]
#%%

df = df.set_index('roeidpk')
len(df)
#%%
existingROE = os.listdir(r"\\nwk-netapp2.nwk.ds.usace.army.mil\MISSIONFILES\MissionProjects\civ\Temporary Roofing\10.0 FMS\Mail_Outs_Ian")
existingROE = [int(s.replace('.pdf','').replace('.docx','').replace('~$','')) for s in existingROE]
df=df.loc[~df.index.isin(existingROE)]

existingROE = os.listdir(r"\\nwk-netapp2.nwk.ds.usace.army.mil\MISSIONFILES\MissionProjects\civ\Temporary Roofing\10.0 FMS\Mail_Outs_Ian")
existingROE = [f for f in existingROE if os.path.isfile(r"\\nwk-netapp2.nwk.ds.usace.army.mil\MISSIONFILES\MissionProjects\civ\Temporary Roofing\10.0 FMS\Mail_Outs_Ian/"+f)]
existingROE = [int(s.replace('.pdf','').replace('.docx','').replace('~$','')) for s in existingROE]
df=df.loc[~df.index.isin(existingROE)]

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        try:
            attList = flayer.attachments.get_list(oid=index)
            for att in attList:
                if "signature" in att['name']:
                    flayer.attachments.download(index,attachment_id=att['id'],save_path = pathToDownload)
            picpath =os.path.join(r'C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Signatures',os.listdir(pathToDownload)[0])
        except:
            pass
        dest_file = os.path.join(roeFolder,str(index)+'.docx')
        #shutil.copy(template, dest_file)
        dic = {"appfirstname": row['appfirstname'],"applastname": row['applastname'],
                      "roeidpk": str(index),"appmatchedaddress": row['appmatchedaddress'],
                      "appcountyname": row['appcountyname'],"appstate": row['appstate'],
                      "appaltphone": row['appaltphone'],"appprimaryphone": row['appprimaryphone'],
                      "appcityname": row['appcityname'],"dateapplied":row['dateapplied'].strftime('%Y-%m-%d'),
                      "appzipcode": row['appzipcode']}
        doc = DocxTemplate(template)
        context = dic
        doc.render(context)
        try:
            doc.add_picture(picpath, width=Inches(2), height=Inches(1))
            files = os.listdir(pathToDownload)
            for f in files:
                pass
                os.remove(os.path.join(pathToDownload,f))
        except:
            pass
        doc.save(dest_file)
        word = client.DispatchEx("Word.Application")

        target_path = dest_file.replace(".docx", r".pdf")
        word_doc = word.Documents.Open(dest_file)
        word_doc.SaveAs(target_path, FileFormat=17)
        word_doc.Close()
        word.Quit()

        os.remove(dest_file)

        receivers=''
        receivers = row['appprimaryemail']
        to = '{} {} <{}>'.format(row['appfirstname'],row['applastname'],row['appprimaryemail'])
        text = """  {} {},

    Thank you for utilizing the Blue Roof Management Systems to sign up for Operation Blue Roof.  Attached to this email is a copy of your Right Of Entry (ROE) for your records.

    Your CUSTOMER REFERENCE NUMBER is: {} \r
    Your PIN is:{} \r
    YOUR ROE Number is: {} \r

    You may use the above information to access the online status website at: https://arcg.is/DWuW8 \r\n
    This link allows you to check on your ROE Status or to cancel your ROE.  If you have already canceled your ROE either using the above link or through our call center, you may disregard this email.

    For additional information on the Blue Roof Program, please visit blueroof.us or call the Blue Roof Call Center at: 888-ROOF-BLU (888-766-3258)


    This is a NO-REPLY EMAIL and is not monitored.
    """.format(row['appfirstname'],row['applastname'],row['applicationnumber'],row['apppinnumber'],str(index))


        msg = MIMEMultipart()
        msg['From'] = 'Operation Blue Roof <no-reply@usace.army.mil>'
        msg['To'] = to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'Operation Blue Roof Application Confirmation'
        #msg['Body']="""This is a test e-mail message generated with Python."""

        msg.attach(MIMEText(text))
        fil=''
        f=os.path.join(r"C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Reports",str(index)+'.pdf')

        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
                )
            # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

        # smtp = smtplib.SMTP(host, port)
        # smtp.sendmail(sender, [receivers,'roe-signup@usace.army.mil'], msg.as_string())
        # smtp.close()
        #shutil.copyfile(f, os.path.join(r"C:\Users\M3ECHJJJ\Documents\ArcGIS\Projects\BRMS_SDE\Sent_Reports",str(index)+'.pdf'))
    except Exception as e:
        try:
            gis = GIS("https://arcportal-ucop-corps.usace.army.mil/s0portal")
            br_layer_item = gis.content.get('7b8ecfaf5c2b43cba2adfd0a86bbef06')
            br_layers = br_layer_item.layers
            flayer = br_layers[0]
            files = os.listdir(pathToDownload)
            for f in files:
                os.remove(os.path.join(pathToDownload,f))
        except:
            print(e)
