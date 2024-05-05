import pymongo
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membuat koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["visualisasi-mongodb"]  
collection = db["spmotion"]  

# Ambil data dari MongoDB
data = list(collection.find())

# Konversi data menjadi DataFrame
df = pd.DataFrame(data)

# Konversi kolom 'tanggal' ke tipe data datetime
df['tanggal'] = pd.to_datetime(df['tanggal'])

# Tambahkan sidebar untuk filter rentang tanggal
st.sidebar.header("Filter Tanggal")
start_date = st.sidebar.date_input("Tanggal Awal", min_value=pd.to_datetime(df['tanggal']).min().date(), max_value=pd.to_datetime(df['tanggal']).max().date(), value=pd.to_datetime(df['tanggal']).min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", min_value=pd.to_datetime(df['tanggal']).min().date(), max_value=pd.to_datetime(df['tanggal']).max().date(), value=pd.to_datetime(df['tanggal']).max().date())

# Konversi variabel start_date dan end_date ke tipe datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Visualisasi data untuk pengguna
st.title("Performa Anda")

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = df[(df['tanggal'] >= start_date) & (df['tanggal'] <= end_date)]

# Jika ada data yang difilter
if not filtered_data.empty:
    user_performance = filtered_data.groupby('userID')['keterangan'].value_counts().unstack(fill_value=0)
    user_performance.plot(kind='bar', stacked=True)
    plt.xlabel('User ID')
    plt.ylabel('Jumlah Gerakan')
    plt.title('Performa Anda')
    st.pyplot(plt)
else:
    st.write("Maaf, belum ada data performa untuk rentang tanggal yang dipilih.")


#################################
# Filter data berdasarkan user_id
user_id = st.sidebar.text_input("Masukkan User ID", value='1')
user_data = df[df['userID'] == user_id]

# Jika ada data untuk user_id yang dimasukkan
if not user_data.empty:
    # Tampilkan performa gerakan dan keterangan jumlah sesuai/tidaknya
    st.title("Performa Gerakan dan Keterangan")
    st.subheader("Performa Gerakan dan Keterangan Jumlah Sesuai/Tidak")
    user_performance = user_data.groupby(['namaGerakan', 'keterangan']).size().unstack(fill_value=0)
    st.dataframe(user_performance)

    # Tampilkan grafik progres harian
    st.title("Progres Harian")
    st.subheader("Grafik Progres Harian")
    daily_progress = user_data.groupby('tanggal')['keterangan'].value_counts().unstack(fill_value=0)
    st.bar_chart(daily_progress)

else:
    st.write("Maaf, tidak ada data untuk User ID yang dimasukkan.")