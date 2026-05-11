# Sistem Pakar Kerusakan iPhone (DS-PSO)

Sistem Pakar untuk mendiagnosa kerusakan hardware pada iPhone berdasarkan input gejala, menggunakan kombinasi metode **Dempster-Shafer (DS)** dan optimasi bobot menggunakan **Particle Swarm Optimization (PSO)**.

## Fitur Utama
*   **Pendeteksian Multikelas:** Mendukung diagnosis untuk 13 kerusakan hardware utama (LCD, IC Power, Baterai, Tombol, Body, dll).
*   **Dempster-Shafer (PCR):** Implementasi Proportional Conflict Redistribution (PCR) yang menjamin sistem kebal terhadap input gejala yang kontradiktif (mencegah benturan/total konflik).
*   **Optimalisasi PSO:** Mencari rentang belief (bobot) gejala terbaik dari dataset riwayat perbaikan secara otomatis untuk meningkatkan akurasi sistem (hingga 100%).
*   **Preprocessing Otomatis:** Memiliki algoritma NLP dan rule-based preprocessing untuk memisahkan kerusakan gabungan (combo damage) langsung dari file Excel.

## Struktur Folder
```text
Sistem Pakar/
├── data/
│   ├── data kerusakan iphone.xlsx   # Dataset mentah riwayat perbaikan
│   ├── knowledge_base.json          # Aturan dasar sistem pakar
│   └── processed/                   # Hasil split data latih & uji
├── modules/
│   ├── data_loader.py               # Modul pembacaan Excel
│   ├── dempster_shafer.py           # Logika perhitungan Dempster-Shafer
│   ├── evaluator.py                 # Modul evaluasi (Akurasi, F1, Matrix)
│   ├── knowledge_base.py            # Modul manipulasi KB
│   ├── preprocessor.py              # Parsing, filtering, label extraction
│   └── pso_optimizer.py             # Implementasi algoritma PSO
├── results/
│   └── (file-file hasil evaluasi, grafik, dan bobot optimal)
├── config.py                        # Pengaturan sistem dan dictionary klasifikasi
├── main.py                          # File utama eksekusi
├── requirements.txt                 # Dependensi Python
└── utils.py                         # Fungsi logger
```

## Persyaratan Sistem
*   Python 3.8+ disarankan
*   PIP Package Manager

## Cara Instalasi

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/nowarlove/Sistem-pakar-kerusakan-iphone.git
   cd Sistem-pakar-kerusakan-iphone
   ```

2. **Buat dan aktifkan Virtual Environment (Direkomendasikan):**
   *   **Windows:**
       ```bash
       python -m venv .venv
       .venv\Scripts\activate
       ```
   *   **Mac/Linux:**
       ```bash
       python3 -m venv .venv
       source .venv/bin/activate
       ```

3. **Install dependensi library:**
   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan Aplikasi

Anda dapat menggunakan beberapa opsi (*flags*) pada `main.py` sesuai kebutuhan:

**1. Menjalankan Penuh (Training, PSO, Evaluasi, Interaktif)**
Perintah ini akan membaca dataset baru dari Excel, membersihkannya, melatih bobot menggunakan PSO, melakukan evaluasi akurasi, dan langsung membuka tampilan interaktif.
```bash
python main.py --mode all
```

**2. Mode Interaktif (Langsung Bertanya ke Sistem)**
Jika Anda hanya ingin mencoba mendiagnosa kerusakan (memasukkan gejala dan melihat hasilnya) tanpa melatih ulang sistem:
```bash
python main.py --mode interactive
```

**3. Hanya Melatih Model dan Mengoptimalkan Bobot (Tanpa Interaktif)**
```bash
python main.py --mode train
```

## Cara Menggunakan Konsol Interaktif
Ketika masuk mode interaktif, sistem akan menampilkan **23 daftar gejala**. 
Pilih gejala yang dialami oleh iPhone Anda, lalu ketikkan angkanya dipisahkan oleh tanda koma.

*Contoh Input:*
```text
Masukkan nomor gejala (pisahkan dengan koma, contoh: 3,5,9):
> 5, 9, 7
```
*Sistem kemudian akan menganalisis gejala tersebut menggunakan perhitungan DS-PSO dan memberikan probabilitas persentase kerusakan dengan tingkat akurasi tinggi.*
