# Laporan Proyek Machine Learning - Magrozan Qobus Zaidan

## Project Overview
Sistem rekomendasi telah menjadi bagian penting dalam berbagai aplikasi digital, mulai dari e-commerce, layanan streaming, hingga pengembangan aplikasi keseharian. Proyek ini bertujuan untuk membangun sistem rekomendasi aktivitas berbasis konten (content-based recommendation system) dengan menggunakan cosine similarity untuk menyarankan aktivitas yang sesuai dengan mood seseorang. Pendekatan ini sangat relevan, terutama untuk mendukung kesehatan mental atau kebugaran, di mana pemilihan aktivitas berdasarkan suasana hati dapat membantu meningkatkan produktivitas dan kesejahteraan individu.

Pentingnya proyek ini terletak pada bagaimana sistem dapat secara personal memberikan rekomendasi aktivitas yang tidak hanya relevan, namun juga adaptif terhadap kondisi emosional seseorang. Dengan menggunakan pendekatan ini, diharapkan sistem dapat membantu pengguna menemukan aktivitas yang bermanfaat dan menyenangkan sesuai suasana hati mereka.
  
  [Getting Started with a Movie Recommendation System](https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recomme) 

## Business Understanding

### Problem Statements

Menjelaskan pernyataan masalah:
- Bagaimana merekomendasikan aktivitas yang sesuai berdasarkan mood seseorang?
- Bagaimana membangun sistem rekomendasi yang bersifat personal dan dapat menangani berbagai jenis mood?

### Goals

Menjelaskan tujuan proyek yang menjawab pernyataan masalah:
- Menghasilkan daftar aktivitas yang direkomendasikan berdasarkan aktivitas lain yang relevan dengan mood pengguna.

    ### Solution statements
    - Menggunakan Content-Based Filtering dengan representasi TF-IDF dan cosine similarity untuk merekomendasikan aktivitas yang memiliki kemiripan konten dengan mood pengguna.
    - Membandingkan pendekatan content-based dengan pendekatan sederhana berbasis keyword matching untuk melihat efektivitas dari pendekatan berbasis similarity vector.

## Data Understanding
Dataset yang digunakan merupakan kumpulan data aktivitas yang dikategorikan berdasarkan mood. Data ini berisi pasangan antara jenis mood dengan daftar aktivitas yang direkomendasikan. Dataset berjumlah 900+ entri, dan setiap entri 
Dataset diperoleh dari Kaggle. Dataset ini berisi data mood harian dan aktivitas dari pengguna aplikasi Daylio.

[Daylio Mood Tracker](https://www.kaggle.com/datasets/kingabzpro/daylio-mood-tracker).  
- Jumlah data awal: 940
- Data yang digunakan setelah filtering : 840
  
Variabel-variabel pada dataset adalah sebagai berikut:
- mood : suasana hati pengguna (contoh: good, normal).
- activities : daftar aktivitas yang sesuai untuk mood tersebut, dipisahkan oleh tanda |.
  
EDA dilakukan dengan:
- Melihat distribusi mood menggunakan pie chart
  ![image](https://github.com/user-attachments/assets/db0e3485-b3ee-4dd1-8580-b705f0fc9d38)

- melihat aktivitas yang paling umum berdasarkan frekuensi menggunakan bar chart
  ![image](https://github.com/user-attachments/assets/7d9b1ffd-49ef-40e1-87b5-8a6aa47a6c04)

insght yang didapatkan :  
- Dataset memiliki berbagai mood seperti Amazing, Good, Normal, dll.
- Terdapat ratusan kombinasi aktivitas unik.
- Beberapa entri mengandung NaN, terutama pada kolom aktivitas

  
## Data Preparation
Beberapa tahapan data preparation yang dilakukan:

### Menghapus Kolom Tidak Perlu:

Menghapus kolom seperti date, weekday, sub_mood, dan lainnya.

### Memfilter data
Filter Data: Hanya aktivitas dengan mood positif yang digunakan untuk meningkatkan kualitas rekomendasi dan menghindari noise dari mood negatif.

### Membersihkan Nilai Kosong:

Menghapus entri yang memiliki missing value.

### Pra-pemrosesan Aktivitas:

Mengganti pemisah | menjadi spasi agar bisa diproses oleh TF-IDF.

Tokenisasi custom berbasis regex untuk membagi aktivitas dengan akurat.

### Vectorization:

Menggunakan TfidfVectorizer dengan tokenizer kustom untuk membuat representasi vektor dari aktivitas.

Setelah dilakukan data preparation Total data berjumlah 799 telah siap untuk modeling dengan data aktivitas yang bersih dan representatif.

## Modeling
Model utama yang digunakan adalah Content-Based Filtering dengan cosine similarity.
### Content-Based Filtering
- Transformasi data aktivitas menjadi matriks TF-IDF.
- Menghitung cosine similarity antar entri aktivitas.
- Untuk setiap input aktivitas, sistem mencari entri paling mirip berdasarkan similarity dan mengambil aktivitas lain dari sana.
### Kelebihan 
- Memberikan rekomendasi yang relevan berdasarkan kemiripan konten.
- Tidak membutuhkan data historis pengguna lain.
### Kekurangan
- Bergantung pada kualitas representasi teks.
- Tidak dapat belajar dari perilaku pengguna lain.

## Berikut hasi dari Top N rekomendasi
![image](https://github.com/user-attachments/assets/688afed1-5df1-42d2-8b60-bf74bddd823d)


## Evaluation
Untuk mengevaluasi sistem, digunakan metrik Precision@5, yang mengukur seberapa banyak aktivitas yang direkomendasikan muncul dalam aktivitas aktual pengguna.
langkah evaluasi :
 Setiap data aktivitas pengguna dibagi menjadi dua bagian: 70% sebagai **input aktivitas**, dan 30% sisanya sebagai **target aktivitas aktual**.
- Sistem menghasilkan rekomendasi Top-15 berdasarkan input aktivitas.
- Kemudian dihitung berapa dari 5 rekomendasi teratas (`Top-5`) yang terdapat dalam target.
- ![image](https://github.com/user-attachments/assets/a31a0129-408e-4c41-9b6e-6352dd2ee7d8)


Hasil 
- Sistem mampu memberikan rekomendasi relevan berdasarkan aktivitas sebelumnya.
- Rata-rata Precision@5 dari 3 contoh diatas >0, menunjukkan performa cukup baik dalam menyarankan aktivitas yang sesuai.
- Untuk meningkatkan performa, dapat dilakukan penguatan pada representasi vektor dan filtering aktivitas yang jarang muncul.
#### Apakah model menjawab semua problem & goal?
Ya. Model telah:
- berhasil memberikan rekomendasi yang secara personal relevan terhadap riwayat aktivitas pengguna.
- Menyediakan rekomendasi yang sesuai konteks.
- Menghasilkan daftar aktivitas yang direkomendasikan berdasarkan aktivitas lain yang relevan dengan mood pengguna
