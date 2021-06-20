#!/usr/bin/env python
# coding: utf-8

# ## Escape from Tarkov Gun Mod Project -- Weapons Database ##

# In[1]:


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# ## Website thats being webscrapped for database ##

# In[2]:


urlWeapons = 'https://escapefromtarkov.gamepedia.com/Weapons'
tarkovURL = 'https://escapefromtarkov.gamepedia.com/'


# ## Requesting information ##

# In[3]:


print("Downloading Weapons Page %s..." %urlWeapons)
response = get(urlWeapons)
response.raise_for_status()


# ## Create obj ##

# In[4]:


WeaponSoup = BeautifulSoup(response.content,'lxml')


# In[5]:


WeaponsData=[]


for table in WeaponSoup.findAll('table',{"class":"wikitable sortable"}):

    WeaponsTable_body = table.find('tbody')

    WeaponsRows = WeaponsTable_body.find_all('tr')

    for row in WeaponsRows:
        WeaponCols = row.find_all('th')+ row.find_all('td')
        WeaponCols = [ele.text.strip() for ele in WeaponCols]
        WeaponsData.append([ele for ele in WeaponCols])

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


# ## Header Adjust And Adding Images ##

# In[7]:


WeaponsDf = pd.DataFrame(WeaponsData)

#WeaponsDf.head()

WeaponsDf = WeaponsDf.reset_index(drop=True)

headerAdjust = WeaponsDf.iloc[0]

WeaponsDf = WeaponsDf[1:]

WeaponsDf.columns = headerAdjust

#print(len(WeaponsDf.columns))

WeaponsDf.columns = ['Index','Name','Cartridge','Firing Modes','Rate of Fire','Description','Image']

WeaponsDf.reset_index(drop=True,inplace=True)
# WeaponsDf


# ## Adding images ##

# In[8]:



WeaponsDf.reset_index(drop=True, inplace=True)

Counter = 1

for item in range(0,len(imageData)):

    if WeaponsDf.loc[WeaponsDf.index[item],'Name'] != 'Name':

       # print(WeaponsDf.loc[item])

        WeaponsDf.loc[item,'Image'] = imageData.loc[Counter,'image']

        Counter+=1
# WeaponsDf


# ## Create csv ##

# In[9]:


WeaponsDf.to_csv("Weapons.csv")
WeaponsDf.to_excel("Weapons.xlsx")


# ## Link to Weapon stats ##

# In[10]:


import requests
import time
WeapLink = []
Temp = " "
for i in WeaponsDf['Name']:
    if(i != 'Image'):
        if(" " in i):
            Temp = i.replace(" ","_")
            WeapLink.append(tarkovURL + Temp)
        else:
            WeapLink.append(tarkovURL + i)
# WeapLink


# ## Grabbing Weapon Stats ## 

# In[11]:


weapStats = pd.DataFrame(columns=['Name','Mods'])
# weapStats


# In[12]:


infoBox = ''
Name = ''
Compatibility = ''
y=1
from tqdm.auto import tqdm
for i in tqdm(range(len(WeapLink)),desc="Loading..."):
    weapURL = requests.get(WeapLink[i])
    weapSource = weapURL.content.decode('utf-8')
    weapNewSoup = BeautifulSoup(weapSource,'lxml')
    time.sleep(1)
    
    Name += weapNewSoup.find('h1','firstHeading').text +(',')
    #print(Name)
    
    
    for x in weapNewSoup.find_all('div','tabbertab'):
        
        Compatibility += x.text + ','
    
    Compatibility += '***,'
    for x in weapNewSoup.find_all('td','va-infobox-content'):
        
        infoBox += x.text + ','
        
    infoBox += '***,'
    y+=1
    
   #print(infoBox)
   

    


# In[152]:


infobox2 = infoBox.split('***,')
tempDF = pd.DataFrame(infobox2)
tempDF.columns = ['Type']
tempDF = pd.DataFrame(tempDF.Type.str.split(',').tolist())
#tempDF.iloc[0]=tempDF.iloc[0].shift(periods=1,axis=0)
tempDF.columns = ['Type',
                  'slot',
                  'Weight',
                  'GridSize',
                  'SoldBy',
                  'Recoil',
                  'Distance',
                  'Ergo',
                  'FireMode',
                  'ROF',
                  'Sight',
                  'Caliber',
                  'DefaultMag',
                  'MuzzleVelocity',
                  'Ammo',
                  'fix1',
                  'fix2',
                  'fix3',
                  'fix4',
                  'fix5']

#for index in range(len(tempDF)):
    #df.loc[df['col'].str.contains("stringsearch", case=False)]
#print(tempDF.loc[tempDF['Weight'].str.contains("kg",case=False,na=False)==False])
#tempFix = tempDF.loc[25]
#tempFix2 = tempFix[:2]
#tempFix3 = tempFix[2:]
#tempFix3=tempFix3.shift(periods=1)
#tempFix4 = pd.concat([tempFix2,tempFix3])
#tempFix3
#tempFix4['Weight']
#tempDF.loc[25] = tempFix4
#tempDF.loc[25]


# In[153]:


#Weight Fix
fixedValues = [25,52]
x =1;
for number in fixedValues:
    tempFix = tempDF.loc[number]
    tempFix2 = tempFix[:2]
    tempFix3 = tempFix[2:]
    tempFix3=tempFix3.shift(periods=x)
    tempFix4 = pd.concat([tempFix2,tempFix3])
    tempDF.loc[number] = tempFix4
    tempDF.loc[number]
    x +=1
    
#GridSize fix
fixedValues =[49,50,51]
for number in fixedValues:
    tempFix = tempDF.loc[number]
    tempFix2 = tempFix[:3]
    tempFix3 = tempFix[3:]
    tempFix3=tempFix3.shift(periods=1)
    tempFix4 = pd.concat([tempFix2,tempFix3])
    tempDF.loc[number] = tempFix4
    tempDF.loc[number]
#SoldBy Fix
fixedValues =[13,18,37,39,64,72,79,85,89]
for number in fixedValues:
    tempFix = tempDF.loc[number]
    tempFix2 = tempFix[:4]
    tempFix3 = tempFix[4:]
    tempFix3=tempFix3.shift(periods=1)
    tempFix4 = pd.concat([tempFix2,tempFix3])
    tempDF.loc[number] = tempFix4
    tempDF.loc[number]

#Mag Fix
fixedValues =[49,50,51]
for number in fixedValues:
    tempFix = tempDF.loc[number]
    tempFix2 = tempFix[:13]
    tempFix3 = tempFix[13:]
    tempFix3=tempFix3.shift(periods=1)
    tempFix4 = pd.concat([tempFix2,tempFix3])
    tempDF.loc[number] = tempFix4
    tempDF.loc[number]
#MoA not needed
fixedValues =[25]
for number in fixedValues:
    tempFix = tempDF.loc[number]
    tempFix2 = tempFix[:10]
    tempFix3 = tempFix[10:]
    
    tempFix3 = tempFix3.shift(-1)
    tempFix4 = pd.concat([tempFix2,tempFix3])
    tempDF.loc[number] = tempFix4
    tempDF.loc[number]
#     print(tempDF.loc[number])


# In[143]:


Name2 = Name.split(',')
weapStats['Name'] = Name2
Compatibility2 = Compatibility.split('***,')
for x in range(len(Compatibility2)):
    weapStats.iloc[x].Mods = Compatibility2[x]


# In[ ]:





# In[156]:


weaponStats = pd.concat([weapStats,tempDF],axis=1)
weaponStats = weaponStats.drop(columns =['fix2','fix3','fix4','fix5'])
weaponStats['Ammo'] = weaponStats['Ammo'] + weaponStats['fix1']
weaponStats = weaponStats.drop(columns=['fix1'])
weaponStats.drop(weaponStats.index[163:201],inplace=True)
weaponStats.drop(weaponStats.index[155:162],inplace=True)
weaponStats.drop(weaponStats.index[90:154],inplace=True)
weaponStats.to_csv('weaponstats.csv')


# In[ ]:





# In[ ]:





# In[ ]:




