#%% combine two pdfs into single file
import PyPDF2
import pandas as pd
import os
#%%

df = pd.read_csv(r"C:\Users\M3ECHJJJ\Downloads\Mails_fixed_address.csv")
page1file = r"C:\Users\M3ECHJJJ\Downloads\Blue-Roof-Mailer-Cover-Letter.pdf"
#%%

for index, row in df.iterrows():
    try:
        page2id = row['roeidpk']
        page2file = os.path.join(r'B:\10.0 FMS\Mail_Outs_Ian',str(page2id) + '.pdf')

        mergeFile = PyPDF2.PdfFileMerger()

        mergeFile.append(PyPDF2.PdfFileReader(page1file, 'rb'))

        mergeFile.append(PyPDF2.PdfFileReader(page2file, 'rb'))

        mergeFile.write(os.path.join(r'C:\Users\M3ECHJJJ\Downloads\Merges',str(page2id) + '.pdf'))
    except:
        pass


# %%
