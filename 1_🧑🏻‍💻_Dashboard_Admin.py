import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="SpineMotion App",
    page_icon="👋",
)

# ---- MAINPAGE -----
st.title(":bar_chart: Admin Dashboard")
st.markdown("##")
st.header('Data Users')

import streamlit as st
import pymongo
import pandas as pd


# Membuat koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["visualisasi-mongodb"]  
collection = db["spmotion"]  

# Ambil data dari MongoDB
data = list(collection.find())

# Konversi data menjadi DataFrame
df = pd.DataFrame(data)

# Hapus kolom _id dari dataframe jika ada
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# Visualisasi data untuk admin
# st.dataframe(df)

#----- SIDEBAR FILTER ------
st.sidebar.header("Please Filter Here:")

user = st.sidebar.multiselect(
    "Select the User:",
    options=df["userID"].unique(),
    default=df["userID"].unique()
)

gerakan = st.sidebar.multiselect(
    "Select the Nama Gerakan:",
    options=df["namaGerakan"].unique(),
    default=df["namaGerakan"].unique()
)

ket = st.sidebar.multiselect(
    "Select the Nama Keterangan:",
    options=df["keterangan"].unique(),
    default=df["keterangan"].unique()
)

tgl = st.sidebar.multiselect(
    "Select the Nama Tanggal:",
    options=df["tanggal"].unique(),
    default=df["tanggal"].unique()
)

# Print nilai-nilai filter
# st.write("Nilai Nama Gerakan yang Dipilih:", gerakan)
# st.write("Nilai Nama Keterangan yang Dipilih:", ket)
# st.write("Nilai Nama Tanggal yang Dipilih:", tgl)

# Filter dataframe berdasarkan pilihan sidebar
df_selection = df.query("userID in @user & namaGerakan in @gerakan & keterangan in @ket & tanggal in @tgl")

# Print hasil query
st.dataframe(df_selection)


 
# # TOP KPI's

# Group the DataFrame by 'namaGerakan'
movement = ('namaGerakan')
grouped_by_movement = df.groupby('namaGerakan')

# Initialize an empty dictionary to store the counts
users_count_sesuai = {}

# Iterate over each group
for name, group in grouped_by_movement:
    # Filter the group to include only rows with 'keterangan' column equal to 'sesuai'
    group_sesuai = group[group['keterangan'] == 'Sesuai']
    
    # Count the number of unique users for this movement with 'sesuai' keterangan
    users_count_sesuai[name] = group_sesuai['userID'].nunique()

# Sort movements based on the number of users in descending order
sorted_movements = sorted(users_count_sesuai.items(), key=lambda x: x[1], reverse=True)

# Display the sorted results
st.subheader("Gerakan yang Paling Sering Dilakukan dengan 'Sesuai':")
for movement, count in sorted_movements:
    st.write(f"{movement}: {count} pengguna")




###################


# # Data contoh
# nama_gerakan = movement
# jumlah_pengguna = users_count_sesuai

# # Buat DataFrame dari data contoh
# data = pd.DataFrame({'Nama Gerakan': nama_gerakan, 'Jumlah Pengguna': jumlah_pengguna})

# # Tampilkan diagram pie chart menggunakan Streamlit
# st.subheader("Diagram Pie Chart")

# fig, ax = plt.subplots()
# ax.pie(data['Jumlah Pengguna'], labels=data['Nama Gerakan'], autopct='%1.1f%%', startangle=140)
# ax.axis('equal')  # Pastikan pie chart tergambar sebagai lingkaran
# st.pyplot(fig)


#################PERFORMA

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
st.subheader("Grafik Performa Pengguna")

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



####USER BY GERAKAN [BAR CHART]
user_by_movement_line = (
    df_selection.groupby(by=["namaGerakan"]).sum()[["userID"]].sort_values(by="userID")
)
fig_movement_user = px.bar(
    user_by_movement_line,
    x="userID",
    y=user_by_movement_line.index,
    orientation="h",
    title="<b>User by Nama Gerakan</b>",
    color_discrete_sequence=["#0083B8"] * len(user_by_movement_line),
    template="plotly_white",
    
)
fig_movement_user.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_movement_user)