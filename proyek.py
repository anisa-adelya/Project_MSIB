import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Load the data from the Excel file
data = pd.read_excel('Data PT.xlsx')

# Normalize the 'Provinsi' column to handle case differences
data['Provinsi'] = data['Provinsi'].str.title()
#data['Provinsi'] = data['Provinsi'].str.replace(r'\bBanten\b', 'Banten', regex=True)

# Ensure 'Badan Penyelenggara' and 'Kode PTS' columns contain only strings
data['Badan Penyelenggara'] = data['Badan Penyelenggara'].astype(str)
data['Kode PTS'] = data['Kode PTS'].astype(str)

# Title of the dashboard
st.title('Dashboard Perguruan Tinggi')

# Filter form
st.sidebar.header('Filter')
selected_province = st.sidebar.selectbox('Pilih Provinsi', ['Semua'] + sorted(data['Provinsi'].unique()))
selected_badan = st.sidebar.selectbox('Pilih Badan Penyelenggara', ['Semua'] + sorted(data['Badan Penyelenggara'].unique()))
selected_university = st.sidebar.selectbox('Pilih Perguruan Tinggi', ['Semua'] + sorted(data['Nama Perguruan Tinggi'].unique()))

filtered_data = data.copy()

if selected_province != 'Semua':
    filtered_data = filtered_data[filtered_data['Provinsi'] == selected_province]
if selected_badan != 'Semua':
    filtered_data = filtered_data[filtered_data['Badan Penyelenggara'] == selected_badan]
if selected_university != 'Semua':
    filtered_data = filtered_data[filtered_data['Nama Perguruan Tinggi'] == selected_university]

# Add row numbers to the table
filtered_data.reset_index(drop=True, inplace=True)
filtered_data.index += 1

# Table 1: Nama perguruan tinggi, kode PTS, Badan penyelenggara, Akreditasi PT, dan jumlah prodi
st.header('Informasi Perguruan Tinggi')
st.dataframe(filtered_data[['Nama Perguruan Tinggi', 'Kode PTS', 'Badan Penyelenggara', 'Akreditasi PT', 'Jumlah Prodi']], height=200)

# Table 2: Informasi badan penyelenggara dan jumlah universitas yang berkaitan
st.header('Jumlah Perguruan Tinggi per Badan Penyelenggara')
badan_counts = filtered_data['Badan Penyelenggara'].value_counts().reset_index()
badan_counts.index = badan_counts.index + 1
badan_counts.columns = ['Badan Penyelenggara', 'Jumlah Perguruan Tinggi']
st.dataframe(badan_counts, height=200)

# Map: Informasi koordinat PT
st.header('Peta Perguruan Tinggi')
def parse_coordinates(coord_str):
    try:
        coord_str = coord_str.replace('(', '').replace(')', '')
        lat, lon = map(float, coord_str.split(','))
        return lat, lon
    except:
        return 0.0, 0.0

filtered_data['Lat'], filtered_data['Lon'] = zip(*filtered_data['Koordinat'].apply(parse_coordinates))
m = folium.Map(location=[-2.548926, 118.0148634], zoom_start=5)

for _, row in filtered_data.iterrows():
    lat, lon = row['Lat'], row['Lon']
    folium.Marker(
        location=[lat, lon],
        popup=f"{row['Nama Perguruan Tinggi']}<br>Alamat: {row['Alamat']}<br>Bentuk: {row['Bentuk Perguruan Tinggi']}<br>Rasio Mahasiswa/Dosen: {row['Rasio Dosen']}",
        tooltip=row['Nama Perguruan Tinggi']
    ).add_to(m)

st_folium(m, width=700, height=500)

# Additional information
st.header('Informasi Tambahan Perguruan Tinggi')

# Alamat PT
st.subheader('Alamat Perguruan Tinggi')
st.dataframe(filtered_data[['Nama Perguruan Tinggi', 'Alamat']], height=200)

# Bentuk PT
st.subheader('Bentuk Perguruan Tinggi')
st.dataframe(filtered_data[['Nama Perguruan Tinggi', 'Bentuk Perguruan Tinggi']], height=200)

# Rasio Mahasiswa dan Dosen
st.subheader('Rasio Mahasiswa dan Dosen')
st.dataframe(filtered_data[['Nama Perguruan Tinggi', 'Jumlah Mahasiswa', 'Jumlah Dosen', 'Rasio Dosen']], height=200)

# Jumlah Prodi
st.subheader('Jumlah Program Studi')
st.dataframe(filtered_data[['Nama Perguruan Tinggi', 'Jumlah Prodi']], height=200)

# Bar chart: Jumlah PT di Provinsi Jawa Barat dan Banten
st.header('Jumlah Perguruan Tinggi di Provinsi Jawa Barat dan Banten')
provinsi_counts = data[data['Provinsi'].isin(['Jawa Barat', 'Banten'])]['Provinsi'].value_counts()
fig, ax = plt.subplots()
provinsi_counts.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Perguruan Tinggi di Provinsi Jawa Barat dan Banten')
ax.set_xlabel('Provinsi')
ax.set_ylabel('Jumlah Perguruan Tinggi')
st.pyplot(fig)

# Bar chart: PT berdasarkan Bentuk PTnya
st.header('Jumlah Perguruan Tinggi Berdasarkan Bentuk Perguruan Tinggi')
bentuk_counts = data['Bentuk Perguruan Tinggi'].value_counts()
fig, ax = plt.subplots()
bentuk_counts.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Perguruan Tinggi Berdasarkan Bentuk Perguruan Tinggi')
ax.set_xlabel('Bentuk Perguruan Tinggi')
ax.set_ylabel('Jumlah Perguruan Tinggi')
st.pyplot(fig)

# Bar chart: PT berdasarkan Akreditasinya
st.header('Jumlah Perguruan Tinggi Berdasarkan Akreditasi')
akreditasi_counts = data['Akreditasi PT'].value_counts()
fig, ax = plt.subplots()
akreditasi_counts.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Perguruan Tinggi Berdasarkan Akreditasi')
ax.set_xlabel('Akreditasi')
ax.set_ylabel('Jumlah Perguruan Tinggi')
st.pyplot(fig)


