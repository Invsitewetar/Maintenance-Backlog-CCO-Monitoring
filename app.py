import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Maintenance Monitoring", layout="wide")
st.title("🛠️ Maintenance Backlog & CCO Monitoring")
st.markdown("---")

# MASUKKAN LINK CSV KAMU DI SINI
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyS_YZ3fhWcPNn9oNC75XF3WmUN2yQHsAD6Z-mm3vPGj7phA3jUVV9_v6GlRMlEDBxzowVy1nwwFdb/pub?gid=1771615802&single=true&output=csv"

def load_data():
    try:
        # SKIP 3 BARIS PERTAMA (None, None, None) agar baris 'ps' jadi judul
        df = pd.read_csv(SHEET_CSV_URL, skiprows=3)
        # Bersihkan kolom yang namanya mengandung 'Unnamed'
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Hapus baris yang benar-benar kosong
        df = df.dropna(how='all')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter Pencarian ---
    st.sidebar.header("🔍 Pencarian")
    search_wo = st.sidebar.text_input("Cari Nomor WO")
    search_part = st.sidebar.text_input("Cari Part Number")
    # TAMBAHAN: Pencarian Nomor Unit
    search_unit = st.sidebar.text_input("Cari Nomor Unit (Contoh: HT119)")

    # Logika Filter
    filtered_df = df.copy()
    
    if search_wo:
        # Menggunakan 'Wo Number' sesuai gambar image_037f00.png
        filtered_df = filtered_df[filtered_df['Wo Number'].astype(str).str.contains(search_wo, case=False, na=False)]
    
    if search_part:
        filtered_df = filtered_df[filtered_df['Part Number'].astype(str).str.contains(search_part, case=False, na=False)]

    if search_unit:
        # Menggunakan 'Unit Number' sesuai gambar image_037f00.png
        filtered_df = filtered_df[filtered_df['Unit Number'].astype(str).str.contains(search_unit, case=False, na=False)]

    # --- Dashboard Ringkasan ---
    st.metric("Total Data Ditemukan", len(filtered_df))

    # --- Tabel Utama ---
    st.subheader("📋 Rincian Monitoring")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ Menunggu link data dari Google Sheets...")
