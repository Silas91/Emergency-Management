import pandas as pd
import plotly.express as px
import os
import plotly.express as px
from plotly.subplots import make_subplots
pd.set_option('display.max_rows', None)
# %% Prep  Data

ida_data = pd.read_csv(r'C:/Users/jason/github/GIS_Tasks/Data_Science/Ida_Blue_Roof.csv')
ida_data['dateapplied'] = pd.to_datetime(ida_data['dateapplied'])
ida_data['dateendoflife'] = pd.to_datetime(ida_data['dateendoflife'])
ida_data['dateroofinstalled'] = pd.to_datetime(ida_data['dateroofinstalled'])
ida_data['dateqacomplete'] = pd.to_datetime(ida_data['dateqacomplete'])
ida_data['dateavqacomplete'] = pd.to_datetime(ida_data['dateavqacomplete'])
# %%
laura_data = pd.read_csv(r'C:/Users/jason/github/GIS_Tasks/Data_Science/Laura_Blue_Roof.csv')
laura_data['creationdate'] = pd.to_datetime(laura_data['creationdate'])
laura_data['date_endoflife'] = pd.to_datetime(laura_data['date_endoflife'])
laura_data['qcroofinstalledqcdate'] = pd.to_datetime(laura_data['qcroofinstalledqcdate'])
laura_data['qacompletedate'] = pd.to_datetime(laura_data['qacompletedate'])

# %% Go ahead and get dates in order to set mission dates
laura_date_applied = laura_data.groupby(laura_data['creationdate'].dt.date).size()
ida_date_applied = ida_data.groupby(ida_data['dateapplied'].dt.date).size()


laura_endoflife = laura_data.groupby(laura_data['date_endoflife'].dt.date).size()
ida_endoflife = ida_data.groupby(ida_data['dateendoflife'].dt.date).size()


laura_installs = laura_data.groupby(laura_data['qcroofinstalledqcdate'].dt.date).size()
ida_installs = ida_data.groupby(ida_data['dateroofinstalled'].dt.date).size()


laura_qa = laura_data.groupby(laura_data['qacompletedate'].dt.date).size()
ida_qa = ida_data.groupby(ida_data['dateqacomplete'].dt.date).size()


# %% Set Mission Dates
laura_idx = pd.date_range(laura_date_applied.index[0], laura_installs.index[-1])
ida_idx = pd.date_range(ida_date_applied.index[0], ida_installs.index[-1])


laura_date_applied = laura_date_applied.reindex(laura_idx, fill_value=0)
laura_date_applied = laura_date_applied.reset_index(drop=True)
ida_date_applied = ida_date_applied.reindex(ida_idx, fill_value=0)
ida_date_applied = ida_date_applied.reset_index(drop=True)
laura_endoflife = laura_endoflife.reindex(laura_idx, fill_value=0)
laura_endoflife = laura_endoflife.reset_index(drop=True)
ida_endoflife = ida_endoflife.reindex(ida_idx, fill_value=0)
ida_endoflife = ida_endoflife.reset_index(drop=True)
laura_installs = laura_installs.reindex(laura_idx, fill_value=0)
laura_installs = laura_installs.reset_index(drop=True)
ida_installs = ida_installs.reindex(ida_idx, fill_value=0)
ida_installs = ida_installs.reset_index(drop=True)
ida_avqa = ida_data.groupby(ida_data['dateavqacomplete'].dt.date).size()
ida_avqa = ida_avqa.reindex(ida_idx, fill_value=0)
ida_avqa = ida_avqa.reset_index(drop=True)
ida_qa = ida_qa.reindex(ida_idx, fill_value=0)
ida_qa = ida_qa.reset_index(drop=True)

# %% Plot total applications


ida_date_applied_df=ida_date_applied.to_frame()
ida_date_applied_df['event'] = 'Ida'
ida_date_applied_df.reset_index(inplace=True)
ida_date_applied_df.columns = ['Mission Day', 'Per Day', 'Event']
laura_date_applied_df=laura_date_applied.to_frame()
laura_date_applied_df['event'] = 'Laura'
laura_date_applied_df.reset_index(inplace=True)
laura_date_applied_df.columns = ['Mission Day', 'Per Day', 'Event']
applications = pd.concat([ida_date_applied_df, laura_date_applied_df])
applications['Total'] = applications.groupby('Event')['Per Day'].cumsum()

subfig = make_subplots(specs=[[{"secondary_y": True}]])
fig1 = px.line(applications, y="Per Day", x="Mission Day", color="Event", title="Applications")
fig1.data[0].name = 'Ida Per Day'
fig1.data[1].name = 'Laura Per Day'
fig2 = px.line(applications, y="Total", x="Mission Day", color="Event", title="Applications")
fig2.data[0].name = 'Ida Total'
fig2.data[1].name = 'Laura Total'
fig1.update_traces(patch={"line": {"dash": 'dot'}})
subfig.add_traces(fig1.data + fig2.data)


# %% Plot total cancelled ROEs


plt.figure(figsize=(15, 8))
plt.plot(ida_endoflife.index, ida_endoflife.values,
         color='green', label="Ida Per Day")
plt.plot(ida_endoflife.cumsum().index,
         ida_endoflife.cumsum().values, color='blue', label="Ida Total")
plt.plot(laura_endoflife.index, laura_endoflife.values,
         color='green', ls='--', label="Laura Per Day")
plt.plot(laura_endoflife.cumsum().index,
         laura_endoflife.cumsum().values, color='blue', ls='--', label="Laura Total")
plt.axvline(x=laura_endoflife.idxmax(), color='black', ls='--',
            label='Max Laura Cancels @ D+' + str(laura_endoflife.idxmax()))
plt.axvline(x=ida_endoflife.idxmax(), color='black',
            label='Max Ida Cancels @ D+' + str(ida_endoflife.idxmax()))
plt.legend()
plt.title("Cancellations")
plt.xlabel("Mission Day")
plt.ylabel("Count")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/Cancellations.png'),
            facecolor='white', transparent=False)
plt.yscale("log")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/Cancellations_Log.png'),
            facecolor='white', transparent=False)


# %% Plot total installs



plt.figure(figsize=(15, 8))
plt.plot(ida_installs.index, ida_installs.values,
         color='green', label="Ida Per Day")
plt.plot(ida_installs.cumsum().index,
         ida_installs.cumsum().values, color='blue', label="Ida Total")
plt.plot(laura_installs.index, laura_installs.values,
         color='green', ls='--', label="Laura Per Day")
plt.plot(laura_installs.cumsum().index,
         laura_installs.cumsum().values, color='blue', ls='--', label="Laura Total")
plt.axvline(x=laura_installs.idxmax(), color='black', ls='--',
            label='Max Laura Installs @ D+' + str(laura_installs.idxmax()))
plt.axvline(x=ida_installs.idxmax(), color='black',
            label='Max Ida Active @ D+' + str(ida_installs.idxmax()))
plt.legend()
plt.title("Roof Installs")
plt.xlabel("Mission Day")
plt.ylabel("Count")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/Roof_Installs.png'),
            facecolor='white', transparent=False)
plt.yscale("log")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/Roof_Installs_Log.png'),
            facecolor='white', transparent=False)


# %% plot total active

ida_active = ida_date_applied.cumsum().subtract(
    ida_endoflife.cumsum()).subtract(ida_installs.cumsum())
laura_active = laura_date_applied.cumsum().subtract(
    laura_endoflife.cumsum()).subtract(laura_installs.cumsum())

plt.figure(figsize=(15, 8))
plt.plot(ida_active.index, ida_active.values, label="Ida", color='blue')
plt.plot(laura_active.index, laura_active.values,
         label="Laura", ls='--', color='blue')

plt.title("Total Active")
plt.xlabel("Date")
plt.ylabel("Count")
plt.axvline(x=laura_active.idxmax(), color='black', ls='--',
            label='Max Laura Active @ D+' + str(laura_active.idxmax()))
plt.axvline(x=ida_active.idxmax(), color='black',
            label='Max Ida Active @ D+' + str(ida_active.idxmax()))
plt.legend()
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/Total_Active.png'),
            facecolor='white', transparent=False)
plt.yscale("log")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/Total_Active_Log.png'),
            facecolor='white', transparent=False)

# %%



plt.figure(figsize=(15, 8))
plt.plot(ida_avqa.index, ida_avqa.values, color='green',
         ls='--', label="Remote QA Per Day")
plt.plot(ida_avqa.cumsum().index,
         ida_avqa.cumsum().values, color='blue', ls='--', label="Total Remote QA")
plt.plot(ida_qa.index, ida_qa.values, color='green', label="Field QA Per Day")
plt.plot(ida_qa.cumsum().index,
         ida_qa.cumsum().values, color='blue', label="Total Field QA")
plt.axvline(x=ida_qa.idxmax(), color='black',
            label='Max Field QA @ D+' + str(ida_qa.idxmax()))
plt.axvline(x=ida_avqa.idxmax(), color='black', ls='--',
            label='Max Remote QA @ D+' + str(ida_avqa.idxmax()))
plt.legend()
plt.title("Ida QA Assessments")
plt.xlabel("Mission Day")
plt.ylabel("Count")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/QA.png'),
            facecolor='white', transparent=False)
plt.yscale("log")
plt.savefig(os.path.join(os.getcwd(), 'GIS_Tasks/Data_Science/BR_Images/QA_Log.png'),
            facecolor='white', transparent=False)


len(applications)


applications.groupby(['Mission Day','Event']).sum().groupby(level=0).cumsum()
