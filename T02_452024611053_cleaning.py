import pandas as pd
import numpy as np

#1.MEMUAT DATA DARI CSV 
file_path = 'data_kotor.csv'
try:
    df = pd.read_csv(file_path)
    print("--- DATA AWAL (SEBELUM DIBERSIHKAN) ---")
    print(df.head())
    print("\n--- Info Awal (Tipe Data & Missing) ---")
    df.info()
    print("\n--- Jumlah Duplikat Awal ---")
    print(f"Total baris duplikat: {df.duplicated().sum()}")
except Exception as e:
    print(f"Error saat membaca file: {e}")
    exit()

#2.PEMBERSIHAN DATA (DATA CLEANING)

print("\n--- MEMULAI PEMBERSIHAN ---")

# Buat salinan agar data asli aman dan tidak terubah
df_clean = df.copy()

# A. Membersihkan Kolom 'Ref.' (Tidak Relevan)
if 'Ref.' in df_clean.columns:
    df_clean = df_clean.drop(columns=['Ref.'])
    print("1. Kolom 'Ref.' telah dihapus.")

# B. Membersihkan Kolom Teks/Object yang Seharusnya Angka
# Kolom seperti 'Peak' dan 'All Time Peak' punya teks [..]
# Kita .split() berdasarkan karakter '[' dan ambil bagian pertamanya [0]
if 'Peak' in df_clean.columns:
    # Ubah jadi string -> split -> ambil bagian pertama
    df_clean['Peak'] = df_clean['Peak'].astype(str).str.split('[').str[0]
    # Ubah jadi numerik
    df_clean['Peak'] = pd.to_numeric(df_clean['Peak'], errors='coerce')

if 'All Time Peak' in df_clean.columns:
    df_clean['All Time Peak'] = df_clean['All Time Peak'].astype(str).str.split('[').str[0]
    df_clean['All Time Peak'] = pd.to_numeric(df_clean['All Time Peak'], errors='coerce')
    
# Kolom mata uang ('Actual gross', 'Adjusted gross', 'Average gross')
# perlu menghapus '$' dan ','
currency_cols = ['Actual gross', 'Adjusted gross (in 2022 dollars)', 'Average gross']
for col in currency_cols:
    if col in df_clean.columns:
        # Hapus $ dan , secara berurutan.
        # Pastikan tipe data string agar bisa .str
        cleaned_col = df_clean[col].astype(str).str.replace('$', '')
        cleaned_col = cleaned_col.str.replace(',', '')
        
        # errors='coerce' akan mengubah data error (misal: kosong) jadi NaN
        df_clean[col] = pd.to_numeric(cleaned_col, errors='coerce')

# Pastikan kolom 'Shows' juga numerik
if 'Shows' in df_clean.columns:
     df_clean['Shows'] = pd.to_numeric(df_clean['Shows'], errors='coerce')

print("2. Kolom teks/mata uang telah dibersihkan dan diubah ke numerik (tanpa 're').")

# C. Menangani Missing Values (NaN)
# isi (impute) data yang hilang.

for col in df_clean.columns:
    if pd.api.types.is_numeric_dtype(df_clean[col]):
        # Jika kolomnya angka -> isi dengan MEDIAN
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)
    elif pd.api.types.is_object_dtype(df_clean[col]):
        # Jika kolomnya teks -> isi dengan MODUS
        mode_val = df_clean[col].mode()
        if not mode_val.empty:
            df_clean[col] = df_clean[col].fillna(mode_val[0])
        else:
            # Jika kolomnya kosong semua, isi dgn string "Unknown"
            df_clean[col] = df_clean[col].fillna("Unknown")

print("3. Missing values (NaN) telah diisi (imputed).")
print("\n--- Cek Missing Values (Setelah) ---")
print(df_clean.isnull().sum())

# D. Menghapus Data Duplikat
baris_duplikat_awal = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates(keep='first')
baris_duplikat_akhir = df_clean.duplicated().sum()

print(f"4. Data duplikat telah ditangani. (Dihapus: {baris_duplikat_awal} baris)")
print(f"   Jumlah duplikat sekarang: {baris_duplikat_akhir}")


#3.MENYIMPAN HASIL KEDALAM CSV BARU
output_file = 'student_scores_cleaned.csv'
try:
    df_clean.to_csv(output_file, index=False)
    print(f"\n--- BERHASIL DISIMPAN ---")
    print(f"Data bersih telah disimpan ke: {output_file}")

    print("\n--- DATA AKHIR (SETELAH DIBERSIHKAN) ---")
    print(df_clean.head())
    print("\n--- Info Akhir (Tipe Data & Missing) ---")
    df_clean.info()

except Exception as e:
    print(f"Error saat menyimpan file: {e}")