#!/usr/bin/env python
# coding: utf-8

# In[1]:


from arcgis.gis import GIS
import pandas as pd


# In[2]:


tokens = pd.read_csv(r"C:\Users\M3ECHJJJ\Documents\Tokens.csv", index_col='Site')
gis = gis = GIS(tokens.at['uCOP Partners','URL'],token = tokens.at['uCOP Partners','Token'])


# In[14]:


df = pd.read_csv(r'D:\brms_users.csv')
df= df.sort_values(by=['QA Name'])


# In[15]:


br_layer_item = gis.content.get('8169ffb3c3d1414095d67bf8c1e400e4')
br_layers = br_layer_item.layers
br_layer = br_layers[0]


# In[16]:


avqa_groups = gis.groups.search(query='title:DCO - Blue Roof - Remote QA', max_groups=1)


# In[27]:


qa_list = []
avqa_list = []
qas_list=[]
fi_list=[]


# In[24]:


df = df.dropna(subset=['AV QA Username','AV QA Name'])
df = df.sort_values('AV QA Name')


# In[28]:


for index, row in df.iterrows():
    #avqa_groups[0].add_users([row['AV QA Username']])
    avqacode = {"code": "%s" % (row['AV QA Username']),"name": "%s" % (row['AV QA Name'])}
    avqa_list.append(avqacode)


# In[26]:


for index, row in df.iterrows():
    #qacode = {"code": "%s" % (row['QA Username']),"name": "%s" % (row['QA Name'])}
    
    avqacode = {"code": "%s" % (row['AV QA Username']),"name": "%s" % (row['AV QA Name'])}
    #avqa_groups.add_users([row['AV QA Username']])
    #qascode = {"code": "%s" % (row['QAS Username']),"name": "%s" % (row['QAS Name'])}
    #ficode = {"code": "%s" % (row['FI Username']),"name": "%s" % (row['FI Name'])}

    
    #qa_list.append(qacode)
    avqa_list.append(avqacode)
    #qas_list.append(qascode)
    #fi_list.append(ficode)
    
    
    


# In[29]:


update_dict = {
  "fields": [
    {
      "name": "Field_Name",
      "domain": {
        "type": "codedValue",
        "name": "Domain_Name",
        "codedValues": avqa_list
      }
    }
  ]
}
#br_layer.manager.update_definition(update_dict)


# In[31]:


update_dict = {"fields": [{"name": "avqaname","domain": {"name": "BRMS_avqaname_b61a0b11-3ef6-4ff6-8572-e59b35dec89c","type": "codedValue","codedValues": avqa_list}}]}
#br_layer.manager.update_definition(update_dict)


# In[34]:


br_layer.manager.update_definition(update_dict)


# In[33]:


update_dict


# In[ ]:




