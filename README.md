# Sistem Pakar Diagnosis Kerusakan iPhone
### Hibridisasi Dempster-Shafer & Particle Swarm Optimization (DS-PSO)

---

## 📁 Struktur Proyek

```
.
├── 1. preprocessing.ipynb        ← [MODEL] Prapemrosesan data & normalisasi slang
├── pso.ipynb                     ← [MODEL] Optimasi bobot belief dengan DS-PSO
├── data/
│   ├── belief.json               ← Aturan pakar awal (15 aturan)
│   ├── optimal_knowledge_base.json ← OUTPUT PSO (basis pengetahuan optimal)
│   ├── data toko 2.xlsx          ← Data mentah toko 2
│   ├── data utama.xlsx           ← Data mentah utama
│   ├── dataLatih/                ← CSV latih (diabaikan git)
│   └── dataUji/                  ← CSV uji (diabaikan git)
├── app/                          ← Antarmuka Web (UI)
│   └── ...
└── referensi/
    └── usulanPenelitianMuh_Renaldi.pdf
```

---

## ⚠️ Catatan Penting

> **`1. preprocessing.ipynb` dan `pso.ipynb` adalah berkas model inti yang TIDAK BOLEH dimodifikasi setelah tag `v1.0-model`.**
> Untuk memulihkan versi model yang telah diuji penguji, gunakan:
> ```bash
> git checkout v1.0-model
> ```

---

## 🚀 Cara Menjalankan Model

### Langkah 1: Preprocessing
Jalankan semua sel di `1. preprocessing.ipynb`
- **Input:** `data/data toko 2.xlsx`, `data/data utama.xlsx`
- **Output:** `data/dataLatih/dataLatih-YYYY-MM-DD-HH-MM.csv`, `data/dataUji/dataUji-YYYY-MM-DD-HH-MM.csv`

### Langkah 2: Optimasi DS-PSO
Jalankan semua sel di `pso.ipynb`
- **Input:** CSV latih/uji terbaru + `data/belief.json`
- **Output:** `data/optimal_knowledge_base.json`
- **Durasi:** ~40 detik (100 iterasi, 30 partikel)

---

## 📊 Hasil Model (v1.0)
- **Akurasi Data Uji:** ~87.57%
- **Fungsi Fitness:** Brier Score (kontinu)
- **Algoritma:** Dempster-Shafer + PSO
- **Dimensi Partikel:** 23 parameter belief
- **Kelas Diagnosis:** 13 kategori kerusakan hardware iPhone

---

## 🌐 Antarmuka Web (app/)
Antarmuka web membaca langsung dari `data/optimal_knowledge_base.json`.
**Notebook model tidak pernah dimodifikasi oleh kode UI.**
