"""Script diagnostik cepat untuk memverifikasi output model DS-PSO."""
import sys, json
sys.path.insert(0, '.')
from core.normalizer import normalize_text
from core.feature_extractor import extract_features
from core.ds_engine import DSEngine

kb = json.load(open('../data/optimal_knowledge_base.json', encoding='utf-8'))
engine = DSEngine(kb)

test_cases = [
    "layar retak tidak bisa disentuh",
    "tidak bisa dicas baterai drop cepat habis",
    "speaker pecah suara kecil",
    "sinyal hilang",
    "kamera buram dan getar",
    "layar gelap tidak nyala",
    "tombol power tidak berfungsi",
    "wifi hilang tidak bisa connect",
    "bodi retak kaca belakang pecah",
    "suara tidak keluar saat telepon",
    "baterai cepat habis drop terus",
    "kena air masuk air mati total",
    "layar blank hitam tidak ada gambar",
    "sinyal lemah naik turun",
    "konektor cas longgar keluar masuk",
]

for kl in test_cases:
    n = normalize_text(kl)
    f = extract_features(n)
    r = engine.run_inference(f)
    active = {k: v for k, v in f.items() if v not in ['Normal', '0,8 - 2,2']}
    diagnosis = r["top_diagnosis"]
    pct = r["top_percentage"]
    fallback = r["used_fallback"]
    print(f"Keluhan  : {kl}")
    print(f"Normalized: {n}")
    print(f"Fitur aktif: {active}")
    print(f"Diagnosis: {diagnosis} ({pct:.1f}%) | fallback={fallback}")
    print("-" * 70)
