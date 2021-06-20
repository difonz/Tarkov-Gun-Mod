#!/usr/bin/env python
# coding: utf-8

# ## Escape from Tarkov Gun Mod Project -- Mod Database ##

# In[2]:


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# ## Website thats being webscrapped for database ##

# In[3]:


urlGunMods= 'https://escapefromtarkov.gamepedia.com/Weapon_mods'
tarkovURL = 'https://escapefromtarkov.gamepedia.com/'


# ## Requesting information ##

# In[4]:


print("Downloading Gun Mods Page %s..." %urlGunMods)
response2 = get(urlGunMods)
response2.raise_for_status()


# ## Create obj ##

# In[5]:


ModSoup = BeautifulSoup(response2.content,'lxml')


# ## Weapon Mods Data ##

# In[6]:


ModData=[]
for table in ModSoup.findAll('table',{"class":"wikitable sortable"}):

    ModTable_body = table.find('tbody')

    ModRows = ModTable_body.find_all('tr')

    for row in ModRows:
        ModCols = row.find_all('th')+ row.find_all('td')

        ModCols = [ele.text.strip() for ele in ModCols]

        ModData.append([ele for ele in ModCols])

    #print(ModData) 
#print(ModCols)


# ## Retrieve Image ## 

# In[7]:


imageNewData = pd.DataFrame()
for tableNew in ModSoup.findAll('table',{"class":"wikitable sortable"}):
    tableNewRows = tableNew.findAll('tr')
    for rowNew in tableNewRows :
        for imageNew in rowNew.select('img'):
            if imageNew.has_attr('src'):
                dataNew = imageNew['src']
                imageNewData = imageNewData.append({'image':dataNew},ignore_index=True)
imageNewData.index = np.arange(1,len(imageNewData)+1)
#imageNewData


# ## ADJUST MOD TABLE ##

# In[8]:


ModDf = pd.DataFrame(ModData)
adjustHeader = ModDf.iloc[0]
ModDf = ModDf[1:]
#functional mod = 3,30,33,49,75 
#muzzle devices(functional) = 108,210,262
#sights (functional) = 271,289,296,375,391,396
#Gear mods = 416,555,682,819
#vital parts = 915,936,1042,1110

#ModDf.columns = adjustHeader
#ModDf.columns = ['Name','Recoil %','Ergonomics','Accuracy %','Muzzle Velocity','Icon','Remove']
#ModDf = ModDf.drop(columns=["Remove"])
#ModDf = ModDf.drop([3,30,33,49,108,210,271,289,296,375,391,416,555,682,915,936,1042])
ModDf.reset_index()
ModDf.index +1
ModDf.columns = ['Name','Recoil %', 'Ergonomics','Accuracy','Muzzle Velocity','sight','Mag']
ModDf['Icon'] = 'None'
#ModDf


# ## Adding Images ##

# In[9]:


ModDf.reset_index(drop=True, inplace=True)
Counter = 1
for item in range(0,len(imageNewData)):
    if ModDf.loc[ModDf.index[item],'Name'] != 'Icon':
       # print(ModDf.loc[item])
        ModDf.loc[item,'Icon'] = imageNewData.loc[Counter,'image']
        Counter+=1
#ModDf


# ## Filling none values with 0's ##

# In[10]:


ModDf= ModDf.fillna(value=np.nan)
ModDf = ModDf.fillna(0)
#ModDf


# ## exporting ##

# In[11]:


ModDf.to_csv("Mods.csv")
ModDf.to_excel("Mods.xlsx")


# ## adjust table for table split ##

# In[12]:


bipods = pd.DataFrame()
foregrips = pd.DataFrame()
flashlights = pd.DataFrame()
tacticalComboDevices = pd.DataFrame()
AuxiliaryParts = pd.DataFrame()
MuzzleAdapters = pd.DataFrame()
FlashHiders = pd.DataFrame()
Suppressors = pd.DataFrame()
AsScope = pd.DataFrame()
ReflexScope = pd.DataFrame()
CompactScope = pd.DataFrame()
IronSight = pd.DataFrame()
Scopes = pd.DataFrame()
SpecialScope = pd.DataFrame()
ChargingHandles = pd.DataFrame()
Mags = pd.DataFrame()
Mounts = pd.DataFrame()
Stocks = pd.DataFrame()
Barrels = pd.DataFrame()
GasBlocks = pd.DataFrame()
HandGuards = pd.DataFrame()
PistolGrips = pd.DataFrame()
Receivers = pd.DataFrame()
lastIndex = 0
split = pd.DataFrame()
Counter = 0
for index in ModDf.index:
    if ModDf.loc[index].Name == 'Icon':
        
        split = ModDf[lastIndex:index]
        
        lastIndex = index+1
        if Counter == 0:
            bipods = split
        elif Counter == 1:
            foregrips = split
        elif Counter == 2:
            flashlights = split
        elif Counter == 3:
            tacticalComboDevices = split
        elif Counter == 4:
            AuxiliaryParts = split
        elif Counter == 5:
            MuzzleAdapters = split
        elif Counter == 6:
            FlashHiders = split
        elif Counter == 7:
            Suppressors = split
        elif Counter == 8:
            AsScope = split
        elif Counter == 9:
            ReflexScope = split
        elif Counter == 10:
            CompactScope = split
        elif Counter == 11:
            IronSight = split
        elif Counter == 12:
            Scopes = split
        elif Counter == 13:
            SpecialScope = split
        elif Counter ==14:
            ChargingHandles = split
        elif Counter == 15:
            Mags = split
        elif Counter == 16:
            Mounts = split
        elif Counter == 17:
            Stocks = split
        elif Counter == 18:
            Barrels = split
        elif Counter == 19:
            GasBlocks=split
        elif Counter == 20:
            HandGuards = split
        elif Counter == 21:
            PistolGrips = split
            lastIndex = index+1
            split = ModDf[lastIndex:]
            Receivers =split
        
        Counter +=1
#Receivers


# ## Stats fix ##

# In[13]:


if(len(bipods.columns)== 8):
    bipods = bipods.rename(columns ={'Name': 'Index','Recoil %':'Name','Ergonomics':'Recoil %',        'Accuracy':'Ergonomic','Muzzle Velocity':'Accuracy'})
    bipods = bipods.drop(columns=['sight','Mag'])
# bipods


# In[14]:


if(len(foregrips.columns)== 8):
    foregrips = foregrips.rename(columns ={'Name': 'Index','Recoil %':'Name','Ergonomics':'Recoil %',        'Accuracy':'Ergonomic','Muzzle Velocity':'Accuracy'})
    foregrips = foregrips.drop(columns=['Accuracy','sight','Mag'])
# foregrips


# In[15]:


if(len(flashlights.columns)== 8):
    flashlights = flashlights.rename(columns ={'Name': 'Index','Recoil %':'Name','Ergonomics':'Recoil %',        'Accuracy':'Ergonomic','Muzzle Velocity':'Accuracy'})
    flashlights = flashlights.drop(columns=['Recoil %','Accuracy','sight','Mag'])
# flashlights


# In[16]:


if(len(tacticalComboDevices.columns)== 8):
    tacticalComboDevices = tacticalComboDevices.drop(columns=['Ergonomics','Muzzle Velocity','sight','Mag'])
    tacticalComboDevices = tacticalComboDevices.rename(columns={'Name':'Index','Recoil %':'Name','Accuracy':'Ergonomics'})

# tacticalComboDevices


# In[17]:


if(len(AuxiliaryParts.columns)== 8):
    AuxiliaryParts = AuxiliaryParts.drop(columns=['Muzzle Velocity','sight','Mag'])
    AuxiliaryParts = AuxiliaryParts.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'})
# AuxiliaryParts


# In[18]:


if(len(MuzzleAdapters.columns)== 8):
    MuzzleAdapters = MuzzleAdapters.drop(columns=                                    ['Mag'])
    MuzzleAdapters = MuzzleAdapters.rename        (columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics','Muzzle Velocity':'Accuracy','sight':'Muzzle Velocity'})

# MuzzleAdapters


# In[19]:


if(len(FlashHiders.columns)== 8):
    FlashHiders = FlashHiders.drop(columns=['Mag'])
    FlashHiders = FlashHiders.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Muzzle Velocity'})
# FlashHiders


# In[20]:


if(len(Suppressors.columns)== 8):
    Suppressors = Suppressors.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Muzzle Velocity','Mag':'Loudness'})
# Suppressors


# In[21]:


if((len(AsScope.columns)== 8) and (len(ReflexScope.columns == 8)) and (len(CompactScope.columns)== 8) and    (len(IronSight.columns) ==8) and (len(Scopes.columns) == 8)):
    
    AsScope = AsScope.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'         ,'Muzzle Velocity': 'Accuracy','sight':'Sight','Mag':'Magnification'})
        
    ReflexScope = ReflexScope.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Sight','Mag':'Magnification'})
    
    CompactScope = CompactScope.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Sight','Mag':'Magnification'})
    
    IronSight = IronSight.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Sight','Mag':'Magnification'})
    
    Scopes = Scopes.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Sight','Mag':'Magnification'})
    
    SpecialScope = SpecialScope.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Sight','Mag':'Magnification'})
# IronSight


# In[22]:


if(len(ChargingHandles.columns)== 8):
    ChargingHandles = ChargingHandles.drop(columns=                                    ['Accuracy','Muzzle Velocity','sight','Mag'])
    ChargingHandles = ChargingHandles.rename        (columns= {'Name':'Index','Recoil %':'Name'})

# ChargingHandles


# In[23]:


if(len(Mags.columns)==8):
    Mags = Mags.rename(columns = {'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics',                                 'Muzzle Velocity':'Check Speed','sight':'Load Modifier','Mag':'Capacity'})
Mags


# In[24]:


if(len(Mounts.columns)==8):
    Mounts = Mounts.drop(columns=['Muzzle Velocity','sight','Mag'])
    Mounts = Mounts.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'})
# Mounts


# In[25]:


if(len(Mounts.columns)==8):
    Mounts
# Mounts


# In[26]:


if(len(Stocks.columns)==8):
    Stocks = Stocks.drop(columns=['Mag'])
    Stocks = Stocks.rename(columns={'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'        ,'Muzzle Velocity': 'Accuracy','sight':'Muzzle Velocity'})
# Stocks


# In[27]:


if(len(Barrels.columns)==8):
    Barrels = Barrels.drop(columns=['Mag'])
    Barrels = Barrels.rename(columns={
        'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics','Muzzle Velocity':'Accuracy'\
        ,'sight':'Muzzle Velocity'})
# Barrels


# In[28]:


if(len(GasBlocks.columns)==8):
    GasBlocks = GasBlocks.drop(columns=['Muzzle Velocity','sight','Mag'])
    GasBlocks = GasBlocks.rename(columns={
        'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'
    })
# GasBlocks


# In[29]:


if(len(HandGuards.columns)==8):
    HandGuards = HandGuards.drop(columns=['Muzzle Velocity','sight','Mag'])
    HandGuards = HandGuards.rename(columns={
        'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'
    })
# HandGuards


# In[30]:


if(len(PistolGrips.columns)==8):
        PistolGrips = PistolGrips.drop(columns=['Muzzle Velocity','sight','Mag'])
        PistolGrips = PistolGrips.rename(columns={
        'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics'
        })
# PistolGrips


# In[31]:


if(len(Receivers.columns)==8):
        Receivers = Receivers.drop(columns=['Mag'])
        Receivers = Receivers.rename(columns={
        'Name':'Index','Recoil %':'Name','Ergonomics':'Recoil %','Accuracy':'Ergonomics',\
        'Muzzle Velocity':'Accuracy','sight':'Muzzle Velocity'})
# Receivers


# ## Files to CSV ##

# In[32]:


bipods.to_csv("Bipods.csv")
foregrips.to_csv("Foregrips.csv")
flashlights.to_csv("Flashlights.csv")
tacticalComboDevices.to_csv("TacticalDevices.csv")
AuxiliaryParts.to_csv("AuxiliaryParts.csv")
MuzzleAdapters.to_csv("MuzzleAdapters.csv")
FlashHiders.to_csv("Flashhiders.csv")
Suppressors.to_csv("Suppressors.csv")
AsScope.to_csv("AssaultScopes.csv")
ReflexScope.to_csv("ReflexScope.csv")
CompactScope.to_csv("CompactScope.csv")
IronSight.to_csv("IronSight.csv")
Scopes.to_csv("Scopes.csv")
SpecialScope.to_csv("SpecialScope.csv")
ChargingHandles.to_csv("ChargeHandles.csv")
Mags.to_csv("Magazines.csv")
Mounts.to_csv("Mounts.csv")
Stocks.to_csv("Stocks.csv")
Barrels.to_csv("Barrels.csv")
GasBlocks.to_csv("GasBlocks.csv")
HandGuards.to_csv("HandGuards.csv")
PistolGrips.to_csv("PistolGrips.csv")
Receivers.to_csv("Receivers.csv")


# In[ ]:




