# -*- coding: utf-8 -*-
"""recommendationsystemCosinesimilarity

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zN5fhE5eElssGQo-ZicIl1Y1icmhZ_Y1

## 1. Import library
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter

from google.colab import files
files.upload()

import os
import zipfile

# Buat folder .kaggle dan pindahkan file ke sana
os.makedirs("/root/.kaggle", exist_ok=True)
!mv kaggle.json /root/.kaggle/kaggle.json

# Ubah permission
!chmod 600 /root/.kaggle/kaggle.json

"""## 2. Load dataset from kaggle"""

!kaggle datasets download kingabzpro/daylio-mood-tracker

!unzip daylio-mood-tracker.zip

"""## 3. Data Loading"""

dataf = pd.read_csv('Daylio_Abid.csv')
dataf.head()

"""## 4. Data understanding"""

dataf.info()

dataf.shape

dataf.describe()

import matplotlib.pyplot as plt

mood_counts = dataf['mood'].value_counts()

plt.figure(figsize=(5, 5))
plt.pie(mood_counts, labels=mood_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Moods')
plt.axis('equal')
plt.show()

activity_counts = Counter()
for activities_str in dataf['activities']:
    try:
        activities = activities_str.split('|')
        for activity in activities:
            activity = activity.strip()
            if activity:
              activity_counts[activity] += 1
    except AttributeError:
        pass
print(activity_counts.most_common())

activity_names = [activity[0] for activity in activity_counts.most_common()]
activity_frequencies = [activity[1] for activity in activity_counts.most_common()]

plt.figure(figsize=(12, 4))
plt.bar(activity_names, activity_frequencies)
plt.xlabel("Activities")
plt.ylabel("Frequency")
plt.title("Unik Aktivitas")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

"""## 5. Data preparation"""

#drop tabel yang tidak dibutuhkan
dataf = dataf.drop(['full_date', 'date', 'weekday', 'time', 'sub_mood'], axis=1)

dataf.head()

#ambil data dengan skala good, amazing, normal saja
dataFrame = dataf[dataf['mood'].isin(['Good', 'Amazing', 'Normal'])]

dataFrame.info()

dataFrame.head()

#cek missing value
dataFrame.isnull().sum()

dataFrame = dataFrame.dropna()
dataFrame.isnull().sum()

#tokenisasi
def custom_tokenizer(text):
    tokens = re.split(r'[^a-zA-Z0-9]', text)
    tokens = [token for token in tokens if token.strip() != '']
    return tokens

data = dataFrame
df = pd.DataFrame(data)

df['processed_activities'] = df['activities'].str.replace('|', ' ', regex=False)

df.head()

"""## 6. Modeling"""

#ubah ke matrix TF-IDF
vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
tfidf_matrix = vectorizer.fit_transform(df['processed_activities'])

vectorizer

#lihat ukuran matrix
tfidf_matrix.shape

#hitung cosine similar
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

cosine_sim_df = pd.DataFrame(cosine_sim, index=df['activities'], columns=df['activities'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada activities
cosine_sim_df.sample(10, axis=1).sample(10, axis=0)

def recommend_activities(input_activities, df, cosine_sim,top_n=1):
    input_vector = vectorizer.transform([input_activities])
    input_cosine_sim = cosine_similarity(input_vector, tfidf_matrix)

    sim_scores = list(enumerate(input_cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]

    activity_indices = [i[0] for i in sim_scores]

    similar_activities_df = df.iloc[activity_indices][['activities']].copy()
    similar_activities_df['activities_list'] = similar_activities_df['activities'].apply(
        lambda x: [activity.strip() for activity in x.split('|')]
    )

    all_activities = [activity for sublist in similar_activities_df['activities_list'] for activity in sublist]
    input_activities_list = [activity.strip() for activity in input_activities.split('|')]
    filtered_activities = [activity for activity in all_activities if activity not in input_activities_list]

    activity_counts = Counter(filtered_activities)
    sorted_activities = sorted(activity_counts.keys(), key=lambda x: activity_counts[x], reverse=True)

    return sorted_activities

score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
score

input_activities = 'fasting'
recommendations = recommend_activities(input_activities, df, cosine_sim)
recommendations

