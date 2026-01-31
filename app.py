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
        # Langsung baca tanpa skiprows karena baris 1 sudah jadi judul (Header)
        df = pd.read_csv(SHEET_CSV_URL)
        # Menghapus kolom 'Unnamed' jika masih tersisa di kanan
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter Pencarian ---
    st.sidebar.header("🔍 Pencarian Maintenance")
    # Filter 1: Nomor Unit (Contoh: GR004, HT119)
    search_unit = st.sidebar.text_input("Cari Nomor Unit")
    # Filter 2: Nomor WO (Contoh: 567306)
    search_wo = st.sidebar.text_input("Cari Nomor WO")
    # Filter 3: Part Number
    search_part = st.sidebar.text_input("Cari Part Number")

    # Logika Filter
    filtered_df = df.copy()
    
    if search_unit:
        filtered_df = filtered_df[filtered_df['Unit Number'].astype(str).str.contains(search_unit, case=False, na=False)]
    
    if search_wo:
        filtered_df = filtered_df[filtered_df['Wo Number'].astype(str).str.contains(search_wo, case=False, na=False)]
    
    if search_part:
        filtered_df = filtered_df[filtered_df['Part Number'].astype(str).str.contains(search_part, case=False, na=False)]

    # --- Tampilan Dashboard ---
    col1, col2 = st.columns(2)
    col1.metric("Total Item Ditemukan", len(filtered_df))
    
    # Menampilkan tabel data yang sudah rapi
    st.subheader("📋 Rincian Monitoring Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ Menunggu data. Pastikan Google Sheets sudah di-publish ke web sebagai CSV.")
else:
    st.warning("⚠️ Menunggu link data dari Google Sheets...")
