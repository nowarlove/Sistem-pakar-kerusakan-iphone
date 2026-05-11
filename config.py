from dataclasses import dataclass, field
from typing import List
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR        = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR    = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR   = os.path.join(DATA_DIR, "processed")
RESULTS_DIR     = os.path.join(BASE_DIR, "results")
MODULES_DIR     = os.path.join(BASE_DIR, "modules")

RAW_EXCEL_PATH  = os.path.join(DATA_DIR, "data kerusakan iphone.xlsx")

TRAIN_CSV_PATH  = os.path.join(PROCESSED_DIR, "train_data.csv")
TEST_CSV_PATH   = os.path.join(PROCESSED_DIR, "test_data.csv")

KB_INITIAL_PATH = os.path.join(DATA_DIR, "knowledge_base.json")
KB_OPTIMAL_PATH = os.path.join(RESULTS_DIR, "knowledge_base_optimal.json")

GBEST_CSV_PATH      = os.path.join(RESULTS_DIR, "gbest_convergence.csv")
CONFUSION_IMG_PATH  = os.path.join(RESULTS_DIR, "confusion_matrix.png")
EVAL_REPORT_PATH    = os.path.join(RESULTS_DIR, "evaluation_report.csv")


COL_NAMA        = "NAMA"
COL_TIPE_HP     = "TIPE HP"
COL_KERUSAKAN   = "KERUSAKAN"
COL_TEKNISI     = "TEKNISI"
COL_HARGA       = "HARGA"
COL_KETERANGAN  = "KETERANGAN"

REQUIRED_COLUMNS = [COL_KERUSAKAN]


DAMAGE_CLASSES = [
    "Baterai Rusak",
    "LCD Rusak",
    "Speaker Rusak",
    "IC Power Rusak",
    "IC Cas Rusak",
    "IC WTR Rusak",
    "Antena Signal Rusak",
    "Kamera Rusak",
    "Mikrofon Rusak",
    "Port Pengisian Rusak",
    "IC Audio Rusak",
    "Tombol Rusak",
    "Body Rusak",
]

SYMPTOM_LIST = [
    "Signal Hilang Total",
    "Baterai Kembung",
    "Baterai Daya Tahan Rendah",
    "LCD Greenscreen",
    "LCD Blank",
    "Layar Retak",
    "Layar Bergaris",
    "Layar Redup",
    "Touch Tidak Responsif",
    "Suara Pecah",
    "Tidak Ada Suara",
    "Perangkat Tidak Menyala",
    "Perangkat Hang",
    "Restart Sendiri",
    "Tidak Bisa Mengisi Daya",
    "Port Longgar",
    "Kabel Tidak Terdeteksi",
    "Kamera Tidak Terbuka",
    "Hasil Foto Buram",
    "Mikrofon Tidak Berfungsi",
    "Sinyal Lemah",
    "Tombol Tidak Berfungsi",
    "Casing Retak",
]

DAMAGE_TO_SYMPTOMS = {
    "Baterai Rusak":        ["Baterai Kembung", "Baterai Daya Tahan Rendah"],
    "LCD Rusak":            ["LCD Blank", "LCD Greenscreen", "Layar Retak", "Layar Bergaris", "Layar Redup", "Touch Tidak Responsif"],
    "Speaker Rusak":        ["Suara Pecah", "Tidak Ada Suara"],
    "IC Power Rusak":       ["Perangkat Tidak Menyala", "Perangkat Hang", "Restart Sendiri", "LCD Blank"],
    "IC Cas Rusak":         ["Tidak Bisa Mengisi Daya"],
    "IC WTR Rusak":         ["Signal Hilang Total"],
    "Antena Signal Rusak":  ["Sinyal Lemah"],
    "Kamera Rusak":         ["Kamera Tidak Terbuka", "Hasil Foto Buram"],
    "Mikrofon Rusak":       ["Mikrofon Tidak Berfungsi"],
    "Port Pengisian Rusak": ["Port Longgar", "Kabel Tidak Terdeteksi", "Tidak Bisa Mengisi Daya"],
    "IC Audio Rusak":       ["Tidak Ada Suara"],
    "Tombol Rusak":         ["Tombol Tidak Berfungsi"],
    "Body Rusak":           ["Casing Retak"],
}

STANDARDIZE_DICT = {
    "Ganti Lcd":                        "LCD Rusak",
    "Ganti Lcd Oled":                   "LCD Rusak",
    "Ganti  Lcd":                       "LCD Rusak",
    "Pasang Lcd":                       "LCD Rusak",
    "Lem Ulang Lcd":                    "LCD Rusak",
    "Lemulang Lcd":                     "LCD Rusak",
    "Lcd Ngefreezee":                   "LCD Rusak",
    "Lcd Blank":                        "LCD Rusak",
    "Lcd Garis Ganti":                  "LCD Rusak",
    "Lcd Ungu Ganti Biasa":             "LCD Rusak",
    "Lcd Kadang Respon Kdg Enggk":      "LCD Rusak",
    "Lcd":                              "LCD Rusak",
    "Lcd Buka":                         "LCD Rusak",
    "Ngefreezee":                       "LCD Rusak",
    "Ngefrezee":                        "LCD Rusak",
    "Ngrfreeze":                        "LCD Rusak",
    "Ngfreeze":                         "LCD Rusak",
    "Ngehang Mati":                     "IC Power Rusak",
    "Layar Redup":                      "LCD Rusak",
    "Greenscreen":                      "LCD Rusak",
    "Jumper Greenscreen":               "LCD Rusak",
    "Jumper Lcd":                       "LCD Rusak",
    "Blackscreen":                      "LCD Rusak",
    "Whitescreen":                      "LCD Rusak",
    "Cek Panel Backlight":              "LCD Rusak",
    "Jumper Lcd Whitescreen":           "LCD Rusak",
    "Soket Lcd":                        "LCD Rusak",
    "Ganti Backdoor":                   "Body Rusak",
    "Ganti Backglass":                  "Body Rusak",
    "Ganti Housing":                    "Body Rusak",
    "Backdoor":                         "Body Rusak",
    "Lem Bckdor":                       "Body Rusak",
    "Pasang Plat Dan Baut":             "Body Rusak",
    "Mati Masuk Airganti Lcd":          "LCD Rusak",
    "Mati Kena Air Cek Lcd":            "LCD Rusak",
    "Mati Lcd Pecah":                   "LCD Rusak",
    "Mati Cek Lcd":                     "LCD Rusak",
    "Mati Cek Lcd Oled":                "LCD Rusak",
    "Mati Habis Ganti Lcd":             "LCD Rusak",
    "Cek Ganti Lcd":                    "LCD Rusak",
    "Lcd, Masuk Air":                   "LCD Rusak",
    "Ganti Lcd Biasa":                  "LCD Rusak",
    "Jalur Lampu":                      "LCD Rusak",

    "Ganti Batrai":                     "Baterai Rusak",
    "Ganti Baterai":                    "Baterai Rusak",
    "Pasang Batrai":                    "Baterai Rusak",
    "Cabut Pasang Baterai":             "Baterai Rusak",
    "Fuse Batrai":                      "Baterai Rusak",
    "Cek Mati Ganti Batrai":            "Baterai Rusak",
    "Mati Cek Batrai":                  "Baterai Rusak",
    "Mati Cek Baterai":                 "Baterai Rusak",
    "Mati Cek Ganti Btrai":             "Baterai Rusak",
    "Tembak Batrai":                    "Baterai Rusak",
    "Tembak Baterai":                   "Baterai Rusak",
    "Batre Drop Ganti":                 "Baterai Rusak",
    "Batrai":                           "Baterai Rusak",
    "Soket Baterai":                    "Baterai Rusak",
    "Pasang Plat Baterai":              "Baterai Rusak",
    "Cek Baterai Tidak Naik":           "Baterai Rusak",
    "Dicas Tak Naik":                   "Baterai Rusak",

    "Mati Cek":                         "IC Power Rusak",
    "Mati Cek Cpu":                     "IC Power Rusak",
    "Mati Cek Ic Power":                "IC Power Rusak",
    "Cek Mati":                         "IC Power Rusak",
    "Cek Ic Power":                     "IC Power Rusak",
    "Cekic Power":                      "IC Power Rusak",
    "Ic Power":                         "IC Power Rusak",
    "Mati":                             "IC Power Rusak",
    "Mati Total":                       "IC Power Rusak",
    "Nyala Cek":                        "IC Power Rusak",
    "Mati Masuk Air":                   "IC Power Rusak",
    "Mati Cek Kena Air":                "IC Power Rusak",
    "Mati Kenak Air":                   "IC Power Rusak",
    "Cek Mati Kena Air":                "IC Power Rusak",
    "Korosi":                           "IC Power Rusak",
    "Masuk Air Korosi":                 "IC Power Rusak",
    "Servis Jalur Vcc Main":            "IC Power Rusak",
    "Restart-Restart":                  "IC Power Rusak",
    "Stuck Logo":                       "IC Power Rusak",
    "Maticek":                           "IC Power Rusak",
    "Matot Cek":                         "IC Power Rusak",
    "Mati ( On Off Konslet )":           "Tombol Rusak",
    "Mati Hidup Cek Baterai":            "Baterai Rusak",
    "Cek Mesin Cpu":                     "IC Power Rusak",
    "Cek":                               "IC Power Rusak",
    "Recovery Cek Tombol":               "IC Power Rusak",
    "Restard Cek Bt":                    "IC Power Rusak",
    "Masuk Air":                         "IC Power Rusak",
    "Kena Air Servis":                   "IC Power Rusak",
    "Software":                          "IC Power Rusak",
    "Sofware":                           "IC Power Rusak",
    "Pindah Mesin":                      "IC Power Rusak",

    "Gakbisa Cas":                      "IC Cas Rusak",
    "Gak Bisa Cas":                     "IC Cas Rusak",
    "Gabisa Cas":                        "IC Cas Rusak",
    "Gkbisa Cas":                        "IC Cas Rusak",
    "Cek Gkbisa Cas":                   "IC Cas Rusak",
    "Cek Gakbisa Cas":                  "IC Cas Rusak",
    "Cas Gakmasuk":                     "IC Cas Rusak",

    "Servis Konektor":                  "Port Pengisian Rusak",
    "Servis Konektor Cas":               "Port Pengisian Rusak",
    "Flexible Cas":                     "Port Pengisian Rusak",
    "Servis Fleksi Cas":                "Port Pengisian Rusak",
    "Ganti Flexible Cas":               "Port Pengisian Rusak",
    "Ganti Fleksible Charger":          "Port Pengisian Rusak",
    "Blok Flexible Cas":                "Port Pengisian Rusak",
    "Port Charger Longgar":             "Port Pengisian Rusak",
    "Servis Koncas":                    "Port Pengisian Rusak",
    "Ganti Fleksibel Cas":              "Port Pengisian Rusak",
    "Bersihkan Konektor":               "Port Pengisian Rusak",
    "Bersihkan Port Cas":               "Port Pengisian Rusak",

    "Ganti Buzzer Speaker":             "Speaker Rusak",
    "Ganti Buzzer Speaker Bawah":       "Speaker Rusak",
    "Buzzer Speaker Bawah":             "Speaker Rusak",
    "Speaker Atas Mati":                "Speaker Rusak",
    "Speaker Bawah Pecah":              "Speaker Rusak",
    "Speaker Nelpon Gakbisa  Cek":      "Speaker Rusak",
    "Cek Speaker":                      "Speaker Rusak",
    "Ganti Speaker Atas":               "Speaker Rusak",

    "Servis Kamera":                    "Kamera Rusak",
    "Ganti Kamera Belakang":            "Kamera Rusak",
    "Ganti Kamera Depan":               "Kamera Rusak",
    "Kamera Depan Mati":                "Kamera Rusak",
    "Kamera Delay":                     "Kamera Rusak",
    "Kaca Kamera":                      "Kamera Rusak",
    "Bersihkn Kamera":                  "Kamera Rusak",
    "Ganti Flash":                      "Kamera Rusak",
    "Ganti Flash Belakang":             "Kamera Rusak",
    "Flash Lampu Off":                  "Kamera Rusak",

    "Servis Mic Telpon":                "Mikrofon Rusak",
    "Ganti Mic Bawah":                  "Mikrofon Rusak",
    "Servis Mic":                       "Mikrofon Rusak",

    "Signal Jauh (Ganti Antena)":       "Antena Signal Rusak",
    "Antena Signal":                    "Antena Signal Rusak",
    "Bar Signal Rendah":                "Antena Signal Rusak",
    "Sim Ga Kedetect":                  "IC WTR Rusak",
    "Cek Sim Gak Keditect":             "IC WTR Rusak",
    "Ic Sinyal":                        "IC WTR Rusak",
    "Servis Ic Signal":                 "IC WTR Rusak",
    "Ic Baseband":                      "IC WTR Rusak",

    "Servis Sensor Telfon":             "IC Audio Rusak",
    "Servis Face Id":                   "IC Audio Rusak",
    "Sensor Face Id":                   "IC Audio Rusak",
    "Perbaiki Face Id":                 "IC Audio Rusak",
    "Ganti Taptik":                     "IC Audio Rusak",
    "Tombol Haptik Mati":               "IC Audio Rusak",
    "Bersihkan Haptik":                 "IC Audio Rusak",
    "Ganti Speaker Atas":               "IC Audio Rusak",

    "Servis Tombol":                    "Tombol Rusak",
    "Servisa Tombol":                   "Tombol Rusak",
    "Service Tombol":                   "Tombol Rusak",
    "Tombol On Off":                    "Tombol Rusak",
    "Servis Tombol On Off":             "Tombol Rusak",
    "Servis Tombol Onoff":              "Tombol Rusak",
    "Servis Tombol Home":               "Tombol Rusak",
    "Servis Tombol Volume":             "Tombol Rusak",
    "Servis Tombol 1Set":               "Tombol Rusak",
    "Tombol Mati 1 Set":                "Tombol Rusak",
    "Ganti Tombol":                     "Tombol Rusak",
    "Ganti Tombol Power":               "Tombol Rusak",
    "Ganti Tombol Home":                "Tombol Rusak",
    "Ganti Tombol Volume":              "Tombol Rusak",
    "Pasang Tombol":                    "Tombol Rusak",
    "On Off Vol":                       "Tombol Rusak",
    "Ganti Fleksibel Tombol":           "Tombol Rusak",
    "Ganti Flexible Tombol":            "Tombol Rusak",
    "Ganti Flexible On Off":            "Tombol Rusak",
    "Pesan Fleksi Tombol":              "Tombol Rusak",
    "Fleksibel Tombolputus":            "Tombol Rusak",

    "Cpu":                              "IC Power Rusak",
    "Cpu Ram":                          "IC Power Rusak",
    "Flexible":                         "LCD Rusak",
    "Flexible Putus":                   "LCD Rusak",
    "Mesin":                            "IC Power Rusak",
    "Flash":                            "IC Power Rusak",
    "Tombol":                           "Tombol Rusak",
    "Batrai":                           "Baterai Rusak",
    "Lcd":                              "LCD Rusak",
    "Lcd Biasa":                        "LCD Rusak",
    "Cas":                              "IC Cas Rusak",
    "Koncas":                           "Port Pengisian Rusak",
    "Konektor":                         "Port Pengisian Rusak",
    "Bacdor":                           "Body Rusak",
    "Housing":                          "Body Rusak",
    "Face Id":                          "IC Audio Rusak",
    "Ngefreeze":                        "LCD Rusak",
    "Kena Air":                         "IC Power Rusak",
    "Kenak Air":                        "IC Power Rusak",
    "Masuk Air":                        "IC Power Rusak",
    "Short Jalur":                      "IC Power Rusak",
    "Mati Cek":                         "IC Power Rusak",
    "Cek Mati":                         "IC Power Rusak",
    "Mati":                             "IC Power Rusak",
    "Instal Ulang":                     "IC Power Rusak",
    "Install Ulang":                    "IC Power Rusak",
    "Software":                         "IC Power Rusak",
    "Sofware":                          "IC Power Rusak",
    "Bug Ios":                          "IC Power Rusak",
    "Reset":                            "IC Power Rusak",
    "Lemot":                            "IC Power Rusak",
    "Emmc":                             "IC Power Rusak",
    "Gakbisa Cas":                      "IC Cas Rusak",
    "Gabisa Cas":                       "IC Cas Rusak",
    "Gkbisa Cas":                       "IC Cas Rusak",
    "Kotor":                            "IC Cas Rusak",
    "Longgar":                          "Port Pengisian Rusak",
    "Charger Rusak":                    "IC Cas Rusak",
    "Fleksi Cas":                       "Port Pengisian Rusak",
    "Lubang Cas":                       "Port Pengisian Rusak",
    "Sinyal":                           "Antena Signal Rusak",
    "Simlock":                          "Antena Signal Rusak",
    "Imei Ke Blokir":                   "Antena Signal Rusak",
    "Cek Sinyal":                       "IC WTR Rusak",
    "On Off":                           "Tombol Rusak",
    "Onoff":                            "Tombol Rusak",
    "Flexible On Off":                  "Tombol Rusak",

    "Ngestuck Ts":                      "LCD Rusak",
    "Servis Tombol On":                 "Tombol Rusak",
    "Off":                              "Tombol Rusak",
    "Ganti Tombol On":                  "Tombol Rusak",
    "Ganti Flexible On":                "Tombol Rusak",
    "Mati Cek Kenak Air":               "IC Power Rusak",
    "Layar Gak Tampil":                 "LCD Rusak",
    "Ganti Mesin":                      "IC Power Rusak",
    "Ganti Baterai & Lcd":              "LCD Rusak",
    "Ganti Backdor":                    "Body Rusak",
    "Matot":                            "IC Power Rusak",
    "Cek Kenak Air":                    "IC Power Rusak",
    "Restar-Restart":                   "IC Power Rusak",
    "Ganti Fleksi Charger":             "Port Pengisian Rusak",
    "Servis Fleksible Charger":         "Port Pengisian Rusak",
    "Kena Air Mati":                    "IC Power Rusak",
    "Bersihkn Korosi":                  "IC Power Rusak",
    "Tegangan 0":                       "IC Power Rusak",
    "Cek Mati Nyala":                   "IC Power Rusak",
    "Instal":                           "IC Power Rusak",
    "Greenline":                        "LCD Rusak",
    "Cek Lcd":                          "LCD Rusak",
    "Cek Tombol":                       "Tombol Rusak",
    "Servis Lubang Cas":                "Port Pengisian Rusak",
    "Logo Eror Dicas":                  "Baterai Rusak",
    "Cek Masuk Air":                    "IC Power Rusak",
    "Mati Kena Air":                    "IC Power Rusak",
    "Lambat Cas":                       "Baterai Rusak",
}


@dataclass
class PSOConfig:
    n_particles:    int   = 30
    max_iter:       int   = 100
    w_max:          float = 0.9
    w_min:          float = 0.4
    c1:             float = 2.0
    c2:             float = 2.0
    v_max:          float = 0.5
    x_min:          float = 0.0
    x_max:          float = 1.0
    random_state:   int   = 42
    converge_tol:   float = 1e-6
    converge_n:     int   = 5


TRAIN_SIZE      = 0.8
RANDOM_STATE    = 42

PSO_CONFIG = PSOConfig()
