import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Maintenance Monitoring", layout="wide")
st.title("🛠️ Maintenance Backlog & CCO Monitoring")
st.markdown("---")

# LINK CSV FINAL
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyS_YZ3fhWcPNn9oNC75XF3WmUN2yQHsAD6Z-mm3vPGj7phA3jUVV9_v6GlRMlEDBxzowVy1nwwFdb/pub?gid=1771615802&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Menghapus kolom 'Unnamed'
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # MENGHAPUS KOLOM TES & TES 2 (Agar tidak muncul di web)
        cols_to_drop = ['Tes', 'Tes 2']
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
        
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter Pencarian ---
    st.sidebar.header("🔍 Pencarian")
    search_unit = st.sidebar.text_input("Cari Nomor Unit (Contoh: GR004)")
    search_wo = st.sidebar.text_input("Cari Nomor WO")
    search_part = st.sidebar.text_input("Cari Part Number")

    # Logika Filter Berdasarkan Gambar Terbaru
    filtered_df = df.copy()
    
    if search_unit:
        # Mencari di kolom 'Unit Number' sesuai image_02f7a0
        filtered_df = filtered_df[filtered_df['Unit Number'].astype(str).str.contains(search_unit, case=False, na=False)]
    
    if search_wo:
        # Mencari di kolom 'Wo Number' sesuai image_02f7a0
        filtered_df = filtered_df[filtered_df['Wo Number'].astype(str).str.contains(search_wo, case=False, na=False)]
    
    if search_part:
        filtered_df = filtered_df[filtered_df['Part Number'].astype(str).str.contains(search_part, case=False, na=False)]

    # --- Dashboard Ringkasan ---
    st.metric("Total Data", len(filtered_df))

    # --- Tabel Utama ---
    st.subheader("📋 Rincian Monitoring Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ Menunggu data dari Google Sheets...")
