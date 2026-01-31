import streamlit as st
import pandas as pd

st.set_page_config(page_title="Maintenance Monitoring", layout="wide")
st.title("🛠️ Maintenance Backlog & CCO Monitoring")
st.markdown("---")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyS_YZ3fhWcPNn9oNC75XF3WmUN2yQHsAD6Z-mm3vPGj7phA3jUVV9_v6GlRMlEDBxzowVy1nwwFdb/pub?gid=1771615802&single=true&output=csv"

def load_data():
    try:
        # Kita skip 3 baris awal supaya judul 'ps', 'Unit Type', dll jadi baris paling atas
        df = pd.read_csv(SHEET_CSV_URL, skiprows=3)
        # Menghapus kolom yang isinya kosong semua jika ada
        df = df.dropna(how='all', axis=1)
        return df
    except:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filter Pencarian ---
    st.sidebar.header("🔍 Pencarian")
    search_wo = st.sidebar.text_input("Cari Nomor WO")
    search_part = st.sidebar.text_input("Cari Part Number")
    search_unit = st.sidebar.text_input("Cari Nomor Unit (Contoh: HT119)") # Tambah filter Unit

    # Logika Filter (Kita sesuaikan nama kolomnya dengan gambar kamu)
    filtered_df = df.copy()
    
    if search_wo:
        # Gunakan 'Wo Number' (W huruf besar, o huruf kecil sesuai gambar kamu)
        filtered_df = filtered_df[filtered_df['Wo Number'].astype(str).str.contains(search_wo, case=False)]
    
    if search_part:
        filtered_df = filtered_df[filtered_df['Part Number'].astype(str).str.contains(search_part, case=False)]

    if search_unit:
        # Kita filter berdasarkan kolom 'Unit Number'
        filtered_df = filtered_df[filtered_df['Unit Number'].astype(str).str.contains(search_unit, case=False)]

    # --- Dashboard Ringkasan ---
    st.metric("Total Backlog", len(filtered_df))

    # --- Tabel Detail ---
    st.subheader("📋 Rincian Monitoring")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("Menunggu link data...")
else:
    st.warning("⚠️ Menunggu link data. Pastikan Google Sheets sudah di-'Publish to web' sebagai CSV.")
