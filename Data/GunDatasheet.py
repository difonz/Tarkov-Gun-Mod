#!/usr/bin/env python
# coding: utf-8

# ## Escape from Tarkov Gun Mod Project Database ##

# In[1]:

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# ## Website thats being webscrapped for database ##

# In[2]:


urlWeapons = 'https://escapefromtarkov.gamepedia.com/Weapons'
urlGunMods= 'https://escapefromtarkov.gamepedia.com/Weapon_mods'
tarkovURL = 'https://escapefromtarkov.gamepedia.com/'


# ## Requesting information ##

# In[3]:


print("Downloading Weapons Page %s..." %urlWeapons + "Completed")
response = get(urlWeapons)
print("Downloading Gun Mods Page %s..." %urlGunMods + "Completed")
response2 = get(urlGunMods)
response.raise_for_status()
response2.raise_for_status()


# ## Create obj ##

# In[4]:


WeaponSoup = BeautifulSoup(response.content,'lxml')
ModSoup = BeautifulSoup(response2.content,'lxml')


# ## Weapons Data ##

# In[5]:


WeaponsData=[]

for table in WeaponSoup.findAll('table',{"class":"wikitable sortable"}):

    WeaponsTable_body = table.find('tbody')

    WeaponsRows = WeaponsTable_body.find_all('tr')

    for row in WeaponsRows:

        WeaponCols = row.find_all('th')+ row.find_all('td')

        WeaponCols = [ele.text.strip() for ele in WeaponCols]
        
        WeaponsData.append([ele for ele in WeaponCols if ele])
    #print(WeaponsData) 
#print(WeaponsData[-1])


# ## Grabbing URLs ## 

# In[6]:


imageData = pd.DataFrame()
for table in WeaponSoup.findAll('table',{"class":"wikitable sortable"}):
    tableRows = table.findAll('tr')
    for row in tableRows :
        for image in row.select('img'):
            if image.has_attr('src'):
                data = image['src']
                imageData = imageData.append({'image':data},ignore_index=True)
imageData.index = np.arange(1,len(imageData)+1)
#imageData


# ## Header Adjust  And Adding  Images##

# In[7]:


WeaponsDf = pd.DataFrame(WeaponsData)
#WeaponsDf.head()
WeaponsDf.drop(WeaponsDf.index[[31,35,37,55,63,70,78,80,97,99,101,116,122,124,126,183,197,205,206,209]],inplace=True)
WeaponsDf = WeaponsDf.reset_index(drop=True)
headerAdjust = WeaponsDf.iloc[0]
WeaponsDf = WeaponsDf[1:]
WeaponsDf.columns = headerAdjust
#print(len(WeaponsDf.columns))
WeaponsDf
deleteCols = len(WeaponsDf.columns)
for cols in range(deleteCols+1):
    if(cols <=6):
        continue
    WeaponsDf = WeaponsDf.drop(WeaponsDf.columns[[cols-1]],axis=1)
    
WeaponsDf.columns = ['Name','Cartridge','Fire Mode'
                     ,'Fire Rate','Description','Image']
WeaponsDf['Image'] = imageData['image']
#WeaponsDf


# ## Fixing unknown Characters##

# In[8]:


WeaponsDf['Fire Mode'].unique()


# ## Create csv ##

# In[9]:


WeaponsDf.to_csv("Weapons.csv")
WeaponsDf.to_excel("Weapons.xlsx")


# ## Weapon Mods Data ##

# In[10]:


ModData=[]

for table in ModSoup.findAll('table',{"class":"wikitable sortable"}):

    ModTable_body = table.find('tbody')

    ModRows = ModTable_body.find_all('tr')

    for row in ModRows:
        ModCols = row.find_all('th')+ row.find_all('td')

        ModCols = [ele.text.strip() for ele in ModCols]
        
        ModData.append([ele for ele in ModCols if ele])
    #print(ModData) 
#print(ModData)


# ## Retrieve Image ## 

# In[11]:


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

# In[12]:


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
ModDf


# ## Adding Images ##

# In[13]:


#3 30 33 49 75 108 210 262 271 289 296 375 391 396 416 555 682 819 915 936 1042 1110

ModDf['Icon'] = imageNewData
ModDf['Icon'].iloc(2).shift(1)

print("Image Assignment...Completed")
# ## Filling none values with 0's ##

# In[14]:


#ModDf= ModDf.fillna(value=np.nan)
#ModDf = ModDf.fillna(0)
#ModDf


# ## exporting ##

# In[15]:



ModDf.to_csv("Mods.csv")
ModDf.to_excel("Mods.xlsx")


# ## adjust table for table split ##

# In[16]:


#functional mod = 3,30,33,49,75 
#muzzle devices(functional) = 108,210,262
#sights (functional) = 271,289,296,375,391,396
#Gear mods = 416,555,682,819
#vital parts = 915,936,1042,1110
#ModDf = ModDf.drop([3,30,33,49,108,210,271,289,296,
#375,391,416,555,682,915,936,1042])

#bipods = pd.DataFrame()
#bipods = ModDf.iloc[:2]

#foregrips = pd.DataFrame()
#foregrips = ModDf.iloc[3:28]

#flashlights=pd.DataFrame()
#flashlight = ModDf.iloc[29:31]


#functionalModTable = pd.DataFrame()
#functionalModTable = ModDf.iloc[:69]


#muzzleModTable = pd.DataFrame()
#muzzleModTable=ModDf.iloc[71:256]
#muzzleModTable.columns = (ModDf.iloc[70])

#sightModTable = pd.DataFrame()
#sightModTable = ModDf.iloc[256:383]
#sightModTable.columns = ModDf.iloc[255]

#needs some fixing
#gearModTable = pd.DataFrame()
#gearModTable = ModDf.iloc[385:803]
#gearModTable.columns = ModDf.iloc[384]

#needs adjusting ()
#vitalModTable = pd.DataFrame()
#vitalModTable = ModDf.iloc[805:1110]
#vitalModTable.columns = ModDf.iloc[70]

#used to test column headers
#flashlight


# In[ ]:


print("Excuting Finished.")

