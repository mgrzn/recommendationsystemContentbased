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
import matplotlib.pyplot as plt
import os
import zipfile

from google.colab import files
files.upload()

# Buat folder .kaggle dan pindahkan file ke sana
os.makedirs("/root/.kaggle", exist_ok=True)
!mv kaggle.json /root/.kaggle/kaggle.json

# Ubah permission
!chmod 600 /root/.kaggle/kaggle.json

"""Pada tahap ini, dilakukan import library yang dibutuhkan untuk proses:
- Manipulasi data (`pandas`, `collections.Counter`)
- Vektorisasi teks dan perhitungan kemiripan (`TfidfVectorizer`, `cosine_similarity`)
- Visualisasi data (`matplotlib`)
- Pengelolaan file dan akses data dari Kaggle.

## 2. Load dataset from kaggle
"""

!kaggle datasets download kingabzpro/daylio-mood-tracker

!unzip daylio-mood-tracker.zip

"""Dataset diunduh dari Kaggle dengan tautan:  
`https://www.kaggle.com/datasets/kingabzpro/daylio-mood-tracker`

Setelah diunduh, file ZIP diekstrak dan dataset `Daylio_Abid.csv` dibaca menggunakan `pandas.read_csv()`.

## 3. Data understanding
"""

dataf = pd.read_csv('Daylio_Abid.csv')
dataf.head()

dataf.info()

dataf.shape

dataf.describe()

mood_counts = dataf['mood'].value_counts()

plt.figure(figsize=(5, 5))
plt.pie(mood_counts, labels=mood_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Moods')
plt.axis('equal')
plt.show()

"""insight
Mood didominasi oleh good normal dan amazing
"""

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

"""insight
Aktivitas yang paling sering muncul adalah 'youtube', 'streaming', dan 'good meal'

#### Data Understanding
Pada tahap ini dilakukan:
- Pengecekan jumlah data (baris dan kolom),
- Identifikasi fitur yang tersedia seperti `mood`, `activities`, `date`, dll.
- Visualisasi distribusi mood dan aktivitas unik.

**Insight:**
- Dataset memiliki berbagai mood seperti Amazing, Good, Normal, dll.
- Terdapat ratusan kombinasi aktivitas unik.
- Beberapa entri mengandung `NaN`, terutama pada kolom aktivitas.

## 4. Data preparation

Tahapan ini mencakup:
- Menghapus kolom tidak relevan.
- Memfilter data berdasarkan mood positif.
- Menghapus missing value.
- Tokenisasi aktivitas agar bisa diproses oleh TF-IDF.
"""

#drop tabel yang tidak dibutuhkan
dataf = dataf.drop(['full_date', 'date', 'weekday', 'time', 'sub_mood'], axis=1)

dataf.head()

#ambil data dengan skala good, amazing, normal saja
dataFrame = dataf[dataf['mood'].isin(['Good', 'Amazing', 'Normal'])]

dataFrame.info()

dataFrame.head()

#cek missing value
dataFrame.isnull().sum()

dataFrame = dataFrame.dropna(subset=['activities'])

dataFrame.isnull().sum()

#tokenisasi
def custom_tokenizer(text):
    tokens = re.split(r'[^a-zA-Z0-9]', text)
    tokens = [token for token in tokens if token.strip() != '']
    return tokens

data = dataFrame
df = pd.DataFrame(data)

df['processed_activities'] = df['activities'].str.replace('|', ' ', regex=False)

"""Mengganti pemisah '|' dngan spasi agar memudahkan proses modeling"""

df.head()

df.info()

"""Total data yang di gunakan berjumlah 799 setelah dilakukan data cleaning

berikut langkah-langkah persiapan data yang dilakukan:

- Menghapus kolom yang tidak dibutuhkan (`full_date`, `time`, `weekday`, dll.)
- Memfilter data agar hanya mengambil mood positif (`Amazing`, `Good`, `Normal`).
- Menghapus nilai kosong (missing value).
- Melakukan tokenisasi dan praproses aktivitas (mengganti ‘|’ menjadi spasi agar dapat diproses oleh TF-IDF).

**Filter Data:**
Hanya aktivitas dengan mood positif yang digunakan untuk meningkatkan kualitas rekomendasi dan menghindari noise dari mood negatif.

**Hasil:**
Dataset telah siap untuk modeling dengan data aktivitas yang bersih dan representatif.

## 5. Modeling &  Results
"""

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
    sim_scores = sim_scores[1:top_n + 2]

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

"""Evaluasi dilakukan dengan menghitung Precision@K."""

input_activities = 'fasting'
recommendations = recommend_activities(input_activities, df, cosine_sim)
recommendations

"""Top N recommendation dari fasting:
'prayer',
 'streaming',
 'youtube',
 'walk',
 'meditation',
 'Audio books',
 'News Update

Pendekatan yang digunakan adalah Content-Based Filtering dengan langkah-langkah:

- Aktivitas dikonversi ke dalam bentuk vektor menggunakan TF-IDF.
- Kemiripan antar aktivitas dihitung menggunakan cosine similarity.
- Model akan merekomendasikan aktivitas yang mirip dengan input pengguna namun belum dilakukan.

**Hasil:**
Matrix TF-IDF berhasil dibentuk dengan ukuran sesuai jumlah data. Cosine similarity digunakan untuk menemukan aktivitas yang relevan.

## 6. Evaluation
Untuk mengevaluasi sistem, digunakan metrik `Precision@5`, yang mengukur seberapa banyak aktivitas yang direkomendasikan muncul dalam aktivitas aktual pengguna.
"""

def precision_at_k(recommended, actual, k=5):
    recommended_k = recommended[:k]
    relevant_items = set(actual)
    recommended_set = set(recommended_k)
    precision = len(recommended_set & relevant_items) / k
    return precision

def split_and_evaluate(index, top_n=5):
    all_acts = [a.strip() for a in df.iloc[index]['activities'].split('|')]
    if len(all_acts) < 3:
        return None

    split_idx = int(0.7 * len(all_acts))
    input_acts = ' | '.join(all_acts[:split_idx])
    target_acts = all_acts[split_idx:]

    recs = recommend_activities(input_acts, df, cosine_sim, top_n=top_n)
    precision = precision_at_k(recs, target_acts, k=top_n)

    return {
        'Input': input_acts,
        'Target': target_acts,
        'Recommendation': recs,
        'Precision@5': precision
    }

# Contoh evaluasi ulang
for i in [0, 10, 50]:
    result = split_and_evaluate(i)
    if result:
        print(f"Data ke-{i}")
        print("Input:", result['Input'])
        print("Target:", result['Target'])
        print("Rekomendasi:", result['Recommendation'])
        print("Precision@5:", result['Precision@5'])
        print("-" * 30)

"""- Sistem mampu memberikan rekomendasi relevan berdasarkan aktivitas sebelumnya.
- Rata-rata Precision@5 dari 3 contoh diatas >0, menunjukkan performa cukup baik dalam menyarankan aktivitas yang sesuai.
- Untuk meningkatkan performa, dapat dilakukan penguatan pada representasi vektor dan filtering aktivitas yang jarang muncul.

#### Apakah model menjawab semua problem & goal?
Ya. Model telah:
- Menyediakan rekomendasi yang sesuai konteks.
Menghasilkan daftar aktivitas yang direkomendasikan berdasarkan aktivitas lain yang relevan dengan mood pengguna
"""

