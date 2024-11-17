#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import numpy as np
from surprise import Dataset, Reader
from surprise import SVD
from surprise import accuracy
import numpy as np
import random
import seaborn as sns
import re

# Load the Excel file
file_path = "Food_Data.xlsx"
excel_data = pd.ExcelFile(file_path)
recipies = pd.read_csv("Cleaned_Indian_Food_Dataset.csv", on_bad_lines='skip', encoding="latin-1")


# List all sheets
#print(excel_data.sheet_names)

# Load a specific sheet
df = pd.read_excel(file_path, sheet_name="ALL")  # Replace with your sheet name
df.head()
#print(df.head())


# In[32]:


df.columns


# In[33]:


#df['Required'] = df['Food code'].apply(lambda x: 1 if 'A' in x else 0)
#df.head(100)
df['Moisture'] = df['Moisture'].dropna().astype(str).str.split('±').str[0]
df['Protein'] = df['Protein'].dropna().astype(str).str.split('±').str[0]
df['Total Fat'] = df['Total Fat'].dropna().astype(str).str.split('±').str[0]
df['Total'] = df['Total'].dropna().astype(str).str.split('±').str[0]
df['Insoluble'] = df['Insoluble'].dropna().astype(str).str.split('±').str[0]
df['Soluble'] = df['Soluble'].dropna().astype(str).str.split('±').str[0]
df['Carbohydrate'] = df['Carbohydrate'].dropna().astype(str).str.split('±').str[0]
df['Energy'] = df['Energy'].dropna().astype(str).str.split('±').str[0]
df['Ash'] = df['Ash'].dropna().astype(str).str.split('±').str[0]

df['Protein'] = pd.to_numeric(df['Protein'],errors = 'coerce')
df['Carbohydrate'] = pd.to_numeric(df['Carbohydrate'],errors = 'coerce')
df['Energy'] = pd.to_numeric(df['Energy'],errors = 'coerce')
df['Total Fat'] = pd.to_numeric(df['Total Fat'],errors = 'coerce')
df.fillna(0,inplace=True)
df.head()


# In[34]:


#df['Non Veg'] = df['Food code'].apply(lambda x: 10 if 'N' in x else (1 if 'M' in x else 0))
#df['Simulated Rating'] =  (df['Energy']/df['Energy'].max())*100
#df['Simulated Rating'] = np.clip(df['Simulated Rating'],1,100)

#For Basic Vegetables
#df['Vegetables'] = df['Food code'].apply(lambda x: 10 if 'D' in x else(5 if 'C' in x else 0))

#Profile 1 Bulk + Non veg(chicken,egg,fish)
#N for chicken, M for egg
#df['Non Veg'] = df['Food code'].apply(lambda x: 10 if 'N' in x else (5 if 'M' in x else 0))
#df['Simulated Rating'] =  ((df['Carbohydrate']/df['Carbohydrate'].max())+(df['Protein']/df['Protein'].max())*0.5+df['Non Veg']/6-(df['Total Fat']/df['Total Fat'].max()))*100
#df['Simulated Rating'] = np.clip(df['Simulated Rating'],1,100)
'''
#For multiple Users

#User_priorities
user_priorities = {
    'User2': {'Energy': 0, 'Total Fat': 1, 'Carbohydrate': 0},
    'User3': {'Energy': 0, 'Total Fat': 0, 'Carbohydrate': 1},
}

#Compute personalized ratings for each user
user_ratings = []
for user, priorities in user_priorities.items():
    for _, row in df.iterrows():
        rating = (
            row['Energy']*priorities['Energy']+
            row['Total Fat']*priorities['Total Fat']+
            row['Carbohydrate']*priorities['Carbohydrate']
        )
        ratings = np.clip(rating/sum(priorities.values()),1,100)
        user_ratings.append({'user':user,'item':row['Food code'],'rating':ratings})
ratings_df = pd.DataFrame(user_ratings)#Users with ratings

#df.head(200)
ratings_df.head(1000)
'''


# In[35]:


#print(ratings_df.iloc[5])
#print(ratings_df.iloc[308])
#df['Total Fat'].max()
#ratings_pivot = ratings_df.pivot_table(columns='user',index='item',values='rating')
#ratings_pivot.fillna(0,inplace=True)


# In[36]:


'''
from scipy.sparse import csr_matrix
diet_sparse = csr_matrix(ratings_pivot)
from sklearn.neighbors import NearestNeighbors
model = NearestNeighbors(algorithm='brute')
model.fit(diet_sparse)
'''
'''
ratings_data = {
    'user': ['user1'] * len(df),
    'item': df['Food code'].tolist(),
    'rating': df['Simulated Rating'].tolist()
}
rating_df = pd.DataFrame(ratings_data)
'''


# In[37]:


'''
reader = Reader(rating_scale=(1, 100))  # Ratings are between 1 and 10
data = Dataset.load_from_df(rating_df[['user', 'item', 'rating']], reader)
trainset = data.build_full_trainset()

model = SVD()
model.fit(trainset)
'''


# In[38]:


'''
#Predections
predictions = []

for content in df['Food code']:
    prediction = model.predict('user1',content)
    predictions.append((content, prediction.est))

# Sort predictions based on predicted ratings
predictions.sort(key=lambda x: x[1], reverse=True)
names = df['Food Name'].tolist()
codes = df['Food code'].tolist()
top_codes = []
top_10_recommended = predictions[:20]
for con,rating in top_10_recommended:
    print(f"{con}:{rating:.2f}")
    top_codes.append(con)
for i in top_codes:
    _r = df[df['Food code']==i]['Food Name'].values[0]
    print(_r," ",i)
#print(ind)
#for k in ind:
    #print(names[k])
'''
#Universal Set
names = df['Food Name'].tolist()
codes = df['Food code'].tolist()

def _add(inc,source,week=1):
    for i in source[:14]:
        r = df[df['Food code']==i]['Food Name'].values[0]
        #print(r)
        temp_lst = re.split(r'[,\s(]+',r)
        if(temp_lst[0] in ['Red','Green','Black']):
            #print("Yes")
            inc.add(temp_lst[1])
            continue
        #print(temp_lst[0])
        inc.add(temp_lst[0])

def generate(SR,key='ABCDEFGHIJKLMNPQRS',number=10):
    df[SR] = np.clip(df[SR],1,100)
    ratings_data = {
    'user': ['user1'] * len(df),
    'item': df['Food code'].tolist(),
    'rating': df[SR].tolist()
    }
    rating_df = pd.DataFrame(ratings_data)
    reader = Reader(rating_scale=(1, 100))  # Ratings are between 1 and 10
    data = Dataset.load_from_df(rating_df[['user', 'item', 'rating']], reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)

    #Predections
    predictions = []

    for content in df['Food code']:
        if(content[0] in key):
            prediction = model.predict('user1',content)
            predictions.append((content, prediction.est))

    # Sort predictions based on predicted ratings
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_codes = []
    top_10_recommended = predictions[:number]
    for con,rating in top_10_recommended:
        #print(f"{con}:{rating:.2f}")
        top_codes.append(con)
    for i in top_codes:
        _r = df[df['Food code']==i]['Food Name'].values[0]
        #print(_r," ",i)
    del df[SR]
    return top_codes

incridents = set()
def diet(protein,fat,carbohydrate,nonveg,nonvegfact=1):
    #Profile 1 Bulk + Non veg(chicken,egg,fish)
    #N for chicken, M for egg
    df['Non Veg'] = df['Food code'].apply(lambda x: 10 if 'N' in x else (5 if 'M' in x else 0))
    df['Rating1'] =  ((df['Carbohydrate']/df['Carbohydrate'].max())*carbohydrate+(df['Protein']/df['Protein'].max())*protein+(df['Non Veg']/6)*nonveg*nonvegfact-(df['Total Fat']/df['Total Fat'].max())*fat)*100
    #df['Rating1'] = np.clip(df['Simulated Rating'],1,100)
    main = []
    if nonveg:
        main = generate('Rating1',number=20)
    else:
        main = generate('Rating1','ABCDEFGHJKL',number=20)
    print()
    _add(incridents,main)
    #print(main)
    #Vegetables
    df['Vegetables'] = df['Food code'].apply(lambda x: 10 if 'D' in x else (10 if 'C' in x else 0))
    df['RatingVeg'] = ((df['Carbohydrate']/df['Carbohydrate'].max())*carbohydrate+(df['Protein']/df['Protein'].max())*protein+(df['Non Veg']/6)*nonveg*nonvegfact-(df['Total Fat']/df['Total Fat'].max())*fat)*100
    veges = generate('RatingVeg','DC',20)
    print()
    #Fruits
    df['Fruits'] = df['Food code'].apply(lambda x:10 if 'E' in x else 0)
    df['RatingFruit'] = ((df['Carbohydrate']/df['Carbohydrate'].max())*carbohydrate+(df['Protein']/df['Protein'].max())*protein+(df['Non Veg']/6)*nonveg*nonvegfact-(df['Total Fat']/df['Total Fat'].max())*fat)*100
    fruit = generate('RatingFruit','E',5)

    #Weekly Plan
    for day in range(1,8):
        print("\n",day,":")
        print("Main Course: ")
        print("1. ",df[df['Food code']==main[0]]['Food Name'].values[0],main.pop(0)," ","\n2. ",df[df['Food code']==main[0]]['Food Name'].values[0]," ",main.pop(0))
        print("Vegetables: ")
        print("1. ",df[df['Food code']==veges[0]]['Food Name'].values[0]," ",veges.pop(0),"\n2. ",df[df['Food code']==veges[0]]['Food Name'].values[0]," ",veges.pop(0))
    #Fruits to eat
    print("\nFruits")
    for i in fruit:
        print(df[df['Food code']==i]['Food Name'].values[0],fruit.pop(0))
def recipy(content):
    index = set()
    _r = recipies['TranslatedRecipeName'].tolist()
    _i = recipies['TranslatedIngredients'].tolist()
    count=0
    for i in _i:
        lst = re.split(r'[,\s(]+',i)
        lower_case_lambda = lambda x: [i.lower() for i in x]
        lower_case_strings = lower_case_lambda(lst)
        if('chicken' in lower_case_strings):
            count+=1
            continue
        for k in content:
            if(k.lower() in lower_case_strings):
                index.add(count)
        count+=1
    return index


diet(1,0,0,1,12)
#print(incridents)
print(len(recipy(incridents)))


# In[ ]:




