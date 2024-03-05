import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Fungsi untuk membaca file CSV
def load_data(file):
    df = pd.read_csv(file)
    return df


# Fungsi untuk pertanyaan bisnis 1: Pola musiman dalam penggunaan sepeda (count) berdasarkan jam atau musim
def explore_hourly_count(df):
    hourly_count = df.groupby('hr')['cnt'].mean()
    st.subheader("Pertanyaan Bisnis 1: Pola musiman dalam penggunaan sepeda (count) berdasarkan jam")
    st.write("Rata-rata penggunaan sepeda per jam dalam sehari:")
    st.write(hourly_count)
    st.write("Visualisasi:")
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_count.plot(kind='line', marker='o', color='skyblue', ax=ax)
    ax.set_title('Average Bike Usage per Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Average Count')
    ax.set_xticks(range(24))
    ax.grid(True)
    st.pyplot(fig)

# Fungsi untuk pertanyaan bisnis 2: Hubungan antara temperatur dan kepadatan penggunaan sepeda (count) setiap jam
def explore_temp_vs_bike(df):
    st.subheader("Pertanyaan Bisnis 2: Hubungan antara temperatur dan kepadatan penggunaan sepeda (count) setiap jam")
    correlation = df['temp'].corr(df['cnt'])
    st.write(f"Korelasi antara temperatur dan penggunaan sepeda: {correlation:.2f}")
    if correlation > 0:
        st.write("Terdapat korelasi positif antara temperatur dan penggunaan sepeda.")
    elif correlation < 0:
        st.write("Terdapat korelasi negatif antara temperatur dan penggunaan sepeda.")
    else:
        st.write("Tidak ada korelasi antara temperatur dan penggunaan sepeda.")
    st.write("Visualisasi:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='temp', y='cnt', alpha=0.5, ax=ax)
    ax.set_title('Temperature vs Bike Usage')
    ax.set_xlabel('Temperature')
    ax.set_ylabel('Count')
    st.pyplot(fig)

# Memuat data
st.title("Analisis Data Bike Sharing")
file = st.file_uploader("Upload file CSV:")
st.checkbox("Mau Menggunakan Data Default ?", False, key='use_default_data')
if file is not None or st.session_state.use_default_data:
    if st.session_state.use_default_data:
        file = "./dashboard/all_data.csv" e
    df = load_data(file)
    # Data Wrangling
    st.subheader("Data Wrangling")
    st.write("\nBeberapa Baris Pertama Dataset:")
    st.write(df.head())
    missing_values = df.isnull().sum()
    st.write("\nJumlah Missing Values per Kolom:")
    st.write(missing_values)
    st.write("\nTipe Data untuk Setiap Kolom:")
    st.write(df.dtypes)

    # Exploratory Data Analysis (EDA)
    st.subheader("Exploratory Data Analysis (EDA)")

    # Handle the date column separately
    date_col = 'dteday'

    # Convert the date column to datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Distribusi Data Variabel Numerik
    st.write("Distribusi Data Variabel Numerik:")
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.boxplot(data=df.drop(columns=[date_col]), ax=ax)
    ax.set_title('Distribusi Data Variabel Numerik')
    ax.set_xlabel('Variabel')
    ax.set_ylabel('Nilai')
    st.pyplot(fig)

    # Korelasi antar fitur numerik
    st.write("Korelasi antar Fitur Numerik:")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(df.drop(columns=[date_col]).corr(), annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Korelasi antar Fitur Numerik')
    st.pyplot(fig)

    # Distribusi data untuk setiap kolom kategorikal
    st.write("Distribusi Data untuk Kolom Kategorikal (Musim):")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(data=df, x='season', palette='coolwarm', hue='season', legend=False, ax=ax)
    ax.set_title('Distribusi Data untuk Kolom Kategorikal (Musim)')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Data')
    st.pyplot(fig)

    # Melihat tren penggunaan sepeda seiring waktu
    st.write("Tren Penggunaan Sepeda Seiring Waktu:")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(data=df, x=date_col, y='cnt', ax=ax)
    ax.set_title('Tren Penggunaan Sepeda Seiring Waktu')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Peminjaman Sepeda')
    st.pyplot(fig)

    # Eksplorasi Pertanyaan Bisnis 1
    explore_hourly_count(df)

    # Eksplorasi Pertanyaan Bisnis 2
    explore_temp_vs_bike(df)

    # Kesimpulan
    st.subheader("Conclusion")
    st.write("""
    #### Conclution pertanyaan 1
    **Pertanyaan Bisnis 1: Pola Musiman dalam Penggunaan Sepeda (Count) Berdasarkan Jam**

    Berdasarkan hasil analisis pertanyaan bisnis 1, kita dapat menyimpulkan pola musiman dalam penggunaan sepeda (count) berdasarkan jam sebagai berikut:

    * Penggunaan sepeda (count) cenderung rendah pada jam-jam awal pagi (00:00 - 05:00) dengan rata-rata di bawah 20.
    * Jumlah penggunaan sepeda mulai meningkat seiring berjalannya waktu setelah jam 06:00, mencapai puncaknya pada jam 17:00 (5:00 PM) dengan rata-rata lebih dari 450.
    * Setelah jam 17:00, penggunaan sepeda mulai menurun secara bertahap hingga larut malam.
    Hal ini menunjukkan adanya pola musiman dalam penggunaan sepeda, dengan puncak penggunaan terjadi pada sore hari dan jumlah penggunaan yang lebih rendah pada jam-jam awal pagi dan larut malam.

    #### Conclution pertanyaan 2
    **Pertanyaan Bisnis 2: Hubungan antara Temperatur dan Kepadatan Penggunaan Sepeda (Count) Setiap Jam**
    Berdasarkan hasil analisis pertanyaan bisnis 2, kita dapat menyimpulkan tentang hubungan antara temperatur dan kepadatan penggunaan sepeda (count) setiap jam sebagai berikut:

    * **Korelasi**: Terdapat korelasi positif antara temperatur dan penggunaan sepeda dengan nilai korelasi sebesar 0.40. Hal ini menunjukkan bahwa semakin tinggi suhu, semakin tinggi juga kepadatan penggunaan sepeda.
    * **Interpretasi Korelasi**: Korelasi positif yang signifikan menunjukkan bahwa ketika suhu meningkat, jumlah penggunaan sepeda juga cenderung meningkat. Hal ini dapat diinterpretasikan sebagai penggunaan sepeda yang lebih tinggi saat cuaca lebih hangat atau pada hari-hari musim panas.

    Dengan demikian, dapat disimpulkan bahwa suhu memiliki pengaruh yang positif terhadap penggunaan sepeda, dan analisis ini memberikan wawasan tambahan tentang faktor-faktor yang mempengaruhi pola penggunaan sepeda.
    """)
