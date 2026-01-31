import streamlit as st
import pandas as pd

# 1. Judul Aplikasi
st.set_page_config(page_title="Maintenance Monitoring", layout="wide")
st.title("🛠️ Maintenance Backlog & CCO Monitoring")
st.markdown("---")

# 2. Link CSV dari Google Sheets Admin Gudang
# Masukkan link CSV hasil 'Publish to Web' di sini
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyS_YZ3fhWcPNn9oNC75XF3WmUN2yQHsAD6Z-mm3vPGj7phA3jUVV9_v6GlRMlEDBxzowVy1nwwFdb/pub?gid=1771615802&single=true&output=csv"

def load_data():
    try:
        # Mengambil data langsung dari Google Sheets
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter Pencarian ---
    st.sidebar.header("🔍 Pencarian")
    search_wo = st.sidebar.text_input("Cari Nomor WO")
    search_part = st.sidebar.text_input("Cari Part Number")

    # Logika Filter
    filtered_df = df.copy()
    if search_wo:
        filtered_df = filtered_df[filtered_df['Wo Number'].astype(str).str.contains(search_wo, case=False)]
    if search_part:
        filtered_df = filtered_df[filtered_df['Part Number'].astype(str).str.contains(search_part, case=False)]

    # --- Dashboard Ringkasan ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Backlog", len(filtered_df))
    
    if 'Aging (Day)' in filtered_df.columns:
        critical_count = len(filtered_df[filtered_df['Aging (Day)'] > 14])
        col2.metric("Critical Aging (>14 Hari)", critical_count)
    
    col3.info("Data tersambung otomatis ke Google Sheets Gudang.")

    # --- Tabel Detail ---
    st.subheader("📋 Rincian Monitoring")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ Menunggu link data. Pastikan Google Sheets sudah di-'Publish to web' sebagai CSV.")
