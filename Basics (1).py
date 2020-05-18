#!/usr/bin/env python
# coding: utf-8

# # Characteristics of Free Android and iOS apps
# 
# For this project, I wish to invesitgate what characteristics the most populat free Android and iOS apps have. Tproject is meant to help me, or any else who is interested, in developing an app that is most likely to have a large audience. 

# In[7]:


from csv import reader

# opens iOS app data
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios_apps_data = list(read_file)
ios_header = ios_apps_data[0]
ios = ios_apps_data[1:]

# opens Android app data
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android_apps_data = list(read_file)
android_header = android_apps_data[0]
android = android_apps_data[1:]


# The code below helps us explore the data set. We have 4 parameters: dataset (list of lists), start (integer), end (integer), and rows_and_columns (Boolean). Start and end tell us the starting and ending indices from a slice of the data set. If the Boolean is true, the function prints the number of rows and columns. 

# In[8]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[9]:


print(android_header)
explore_data(android, 0, 2, rows_and_columns = True)


# The Android data set has 10841 rows and 13 columns. Information about this data set can be found [here](https://www.kaggle.com/lava18/google-play-store-apps). To help with our analysis, the following columns may be helpful: 'App' [0], 'Category' [1], 'Reviews' [3], 'Installs' [5], 'Type' [6], 'Price' [7], and 'Genres' [9]

# In[10]:


print(ios_header)
explore_data(ios, 0, 2, rows_and_columns = True)


# The iOS data set has 7197 rows and 16 columns. Information about this data set can be found [here](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps). To help with our analysis, the following columns may be helpful: 'track_name' [1], 'currency' [3], 'price' [4], 'rating_count_tot' [5], 'rating_count_ver' [6], and 'prime_genre' [9].  

# To prepare our data for analysis, I must first clean the data. I plan on removing inaccurate and duplicate data. Also, since I am focusing this study on free English apps, I will need to adjust my data to focus on those. First, 

# First, from [this](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015) Google Play discussion, I will remove the row with an error. 

# In[11]:


print(android[10472])
print('\n')
print(len(android))
print('\n')
del android[10472]
print('\n')
print(len(android))


# The Android data set now has 10840 rows. 

# I will now search for and delete duplicates

# In[12]:


unique_apps = []
duplicate_apps = []
duplicate_indices = []

for i in android:
    name = i[0]
    if name in unique_apps:
        duplicate_apps.append(name)
        duplicate_indices.append(i)
    else:
        unique_apps.append(name)
        
print('There are ', len(unique_apps), 'unique android apps')
print('\n')
print('There are ', len(duplicate_apps), 'duplicate apps')
print('\n')
print('To double check my work, the number of duplicate apps should match the number of duplicate indices, which is', len(duplicate_indices))


# I now need to delete the duplicate apps and just keep one. To decide which to keep, I will closely inspect one of the duplicates, Instagram. 

# In[13]:


for i in android:
    name = i[0]
    if name == 'Instagram':
        print(i)


# It looks like the difference in these rows is the 3rd index, reviews. I will keep the row with the most reviews since I assume that that is the most recent data. I will do the same with the other duplicates as well. To remove the duplictaes, I will create a dictionary where the key is the unique app name and the value is the highest number of reviews for that app. I will then use the information in the dictionary to create a new data set with only unique apps. 

# In[14]:


reviews_max = {}

for i in android:
    name = i[0]
    n_reviews = float(i[3])
    if (name in reviews_max) and (reviews_max[name] < n_reviews):
        reviews_max[name] = n_reviews #keeps only the greatest number of reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
len(reviews_max)
    


# The length of the dictionary matches what I expected. I will now use the dictionary I created to remove the duplicate rows. 

# In[15]:


android_clean = []
already_added = []

for i in android:
    name = i[0]
    n_reviews = float(i[3])
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(i)
        already_added.append(name)

len(android_clean)


# android_clean will be my clean set of data, and has the correct number of rows. 

# I know want to include only English apps. I will use the range of English text in ASCII (0-127). I will build a function that detects if a character is part of this range. 

# In[16]:


def Eng_detect(string):
    count = 0
    for i in string:
        if ord(i) > 127:
            count += 1
    if count > 3: #if there are more than 3 non_English characters, the string is probably not in English
        return(False)
    else: 
        return(True)


# In[17]:


android_clean_non_Eng = []
android_English = []
ios_English = []
ios_clean_non_Eng = []

for i in android_clean:
    name = i[0]
    if (Eng_detect(name) != True):
        android_clean_non_Eng.append(i)
    else:
        android_English.append(i)
        
for j in ios:
    name = j[1]
    if (Eng_detect(name) != True):
        ios_clean_non_Eng.append(j)
    else:
        ios_English.append(j)
        
print('The number of clean English apps is ', len(android_English))
print('\n')
print('The number of clean iOS apps is ', len(ios_English))
print('\n')
print('The number of non-English Android and iOS apps is ', len(android_clean_non_Eng), ' and ', len(ios_clean_non_Eng))


# Since I am only focusing on free apps, I will isolate the data for free apps. 

# In[18]:


android_final = []
android_paid_Eng = []

ios_final = []
ios_paid_Eng = []

for i in android_English:
    price = i[7]
    if price == '0':
        android_final.append(i)
    else:
        android_paid_Eng.append(i)
        
for j in ios_English:
    price = j[4]
    if price == '0.0':
        ios_final.append(j)
    else:
        ios_paid_Eng.append(j)
        
print('The number of free English apps is ', len(android_final))
print('\n')
print('The number of free iOS apps is ', len(ios_final))
print('\n')
print('The number of paid English Android and iOS apps is ', len(android_paid_Eng), ' and ', len(ios_paid_Eng))


# For our final analysis, we have 8864 and 3222 free English Android and iOS apps respectively. 

# # Analysis
# 
# Now that our data is clean, we can now begin our analysis. As a reminder, our end goal is to find what types of apps are most successful on iOS and Android platforms. 
# 
# We will begin our analysis by seeing which types of genres are most comment. To do this, we will build some frequency tables. 

# In[19]:


#This function builds a frequency table that counts the number of values. 
def freq_table(data_set, index):
    table = {}
    total = 0
    for i in data_set:
        total += 1
        value = i[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percent = {}
    for j in table:
        val_percent = (table[j] / total) * 100
        table_percent[j] = val_percent
        
    return table_percent


# In[20]:


#This function takes the table above and puts it in descending order.

def freq_table_descend(data_set, index):
    table = freq_table(data_set, index)
    disp_table = []
    for i in table:
        key_tuple = (table[i], i)
        disp_table.append(key_tuple)
    final_table = sorted(disp_table, reverse = True)
    for j in final_table:
        print(j[1], ':', j[0])


# In[21]:


freq_table_descend(android_final, 1)


# We see that for Android, the most popular category of apps is family apps, followed by games. 

# In[22]:


freq_table_descend(ios_final, -5)


# We see from the iOS data that the most popular genre by far is games followed by entertainment. The results here and from our Android data suggest that games would be the most popular genre of free apps overall. 

# Now, I wish to look through the data and determine which genres have the most users. I will begin with the Android data

# In[23]:


genres_android = freq_table(android_final, 1)

for i in genres_android:
    total = 0 #stores the sum of the user ratings
    len_category = 0 #store the number of apps specific to genre
    for j in android_final:
        category_app = j[1]
        if category_app == i:            
            n_installs = j[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_num_installs = total / len_category
    print(i, ':', avg_num_installs)


# It looks like communication apps have the most installations, followed by photography, games, tools, entertainment, video players, social, and productivity. 

# Let's now do the same with the iOS data. Unfortuntaly, there is no information regarding the number of installations. Instead, I will look at rating_count_tot, which will tell me how many ratings an app received. 

# In[26]:


prime_genre_ios = freq_table(ios_final, -5)

for i in prime_genre_ios:
    total = 0
    len_genre = 0
    for j in ios_final:
        genre_app = j[-5]
        if genre_app == i:
            num_ratings = float(j[5])
            total += num_ratings
            len_genre += 1
    avg_num_ratings = total / len_genre
    print(i, ':', avg_num_ratings)


# From looking at this data, we see that Navigation, Social Networking, Music, Weather, and Book are the most popular apps. 

# # Conclusion
# 
# From this exploratory project, we can see that the most popular free English apps are those that serve a purpose, rather than just games (which may be saturated in the market). 
