import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

from app import sentistrength, config  # Pastikan class sentistrength & config ini benar

# Inisialisasi sentistrength
senti = sentistrength(config)

# Judul dan deskripsi
st.set_page_config(page_title="Analisis Sentimen Komentar", layout="wide")
st.title("📘 Analisis Sentimen Komentar DB Reguler")
st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

# Baca file CSV langsung (tanpa upload)
DATA_PATH = "komentar_dbs_reguler.csv"

try:
    df = pd.read_csv(DATA_PATH)

    # Validasi kolom
    if len(df.columns) < 3:
        st.error("❌ Dataset harus memiliki minimal 3 kolom. Komentar dianggap berada di kolom ke-3.")
    else:
        komentar = df.iloc[:, 2].dropna().astype(str).tolist()

        # Analisis Sentimen
        hasil_klasifikasi = [senti.main(text) for text in komentar]
        df["Sentimen"] = hasil_klasifikasi

        # Tampilkan hasil
        st.subheader("📄 Tabel Hasil Sentimen")
        st.dataframe(df[["Sentimen"]].value_counts().reset_index(name="Jumlah"))

        # Hitung distribusi
        counter = Counter(hasil_klasifikasi)
        labels = ["Positif", "Negatif", "Netral"]
        values = [counter.get(l, 0) for l in labels]

        # Pie Chart
        # Visualisasi Pie Chart - Sudah Diperbaiki
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        explode = [0.05, 0.05, 0.05]
        colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

        ax1.pie(values,
                labels=labels,
                autopct='%1.1f%%',
                startangle=140,
                explode=explode,
                colors=colors,
                textprops={'fontsize': 12})
        ax1.axis('equal')

        st.subheader("📊 Pie Chart Distribusi Sentimen (Rapi)")
        st.pyplot(fig1)


        # Bar Chart
        st.subheader("📊 Bar Chart Distribusi Sentimen")
        bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
        st.bar_chart(bar_df)

except FileNotFoundError:
    st.error(f"❌ File `{DATA_PATH}` tidak ditemukan.")
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan saat membaca file: {e}")
