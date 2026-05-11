import json
import os
from typing import List

from utils import logger, ensure_dir
from config import KB_INITIAL_PATH, DATA_DIR


KNOWLEDGE_BASE: dict = {
    "Signal Hilang Total": {
        "IC WTR Rusak":          0.60,
        "Antena Signal Rusak":   0.30,
    },
    "Baterai Kembung": {
        "Baterai Rusak":         0.95,
    },
    "Baterai Daya Tahan Rendah": {
        "Baterai Rusak":         0.65,
        "IC Cas Rusak":          0.15,
        "IC Power Rusak":        0.10,
    },
    "LCD Greenscreen": {
        "LCD Rusak":             0.90,
    },
    "LCD Blank": {
        "LCD Rusak":             0.55,
        "IC Power Rusak":        0.30,
    },
    "Layar Retak": {
        "LCD Rusak":             0.90,
    },
    "Layar Bergaris": {
        "LCD Rusak":             0.88,
    },
    "Layar Redup": {
        "LCD Rusak":             0.85,
        "IC Power Rusak":        0.10,
    },
    "Touch Tidak Responsif": {
        "LCD Rusak":             0.70,
    },
    "Suara Pecah": {
        "Speaker Rusak":         0.75,
        "Baterai Rusak":         0.15,
        "IC Audio Rusak":        0.05,
    },
    "Tidak Ada Suara": {
        "IC Audio Rusak":        0.80,
        "Speaker Rusak":         0.10,
    },
    "Perangkat Tidak Menyala": {
        "IC Power Rusak":        0.65,
        "LCD Rusak":             0.20,
    },
    "Perangkat Hang": {
        "IC Power Rusak":        0.60,
        "Baterai Rusak":         0.20,
    },
    "Restart Sendiri": {
        "IC Power Rusak":        0.55,
        "Baterai Rusak":         0.30,
    },
    "Tidak Bisa Mengisi Daya": {
        "IC Cas Rusak":          0.55,
        "Port Pengisian Rusak":  0.35,
    },
    "Port Longgar": {
        "Port Pengisian Rusak":  0.75,
    },
    "Kabel Tidak Terdeteksi": {
        "Port Pengisian Rusak":  0.80,
    },
    "Kamera Tidak Terbuka": {
        "Kamera Rusak":          0.85,
    },
    "Hasil Foto Buram": {
        "Kamera Rusak":          0.70,
    },
    "Mikrofon Tidak Berfungsi": {
        "Mikrofon Rusak":        0.85,
    },
    "Sinyal Lemah": {
        "Antena Signal Rusak":   0.70,
        "IC WTR Rusak":          0.20,
    },
    "Tombol Tidak Berfungsi": {
        "Tombol Rusak":          0.92,
    },
    "Casing Retak": {
        "Body Rusak":            0.95,
    },
}


def save_kb(kb: dict, path: str) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    logger.info(f"Knowledge base disimpan: {path}")


def load_kb(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Knowledge base tidak ditemukan: {path}")
    with open(path, encoding="utf-8") as f:
        kb = json.load(f)
    logger.info(f"Knowledge base dimuat: {path} ({len(kb)} gejala).")
    return kb


def get_all_symptoms(kb: dict) -> List[str]:
    return list(kb.keys())


def get_all_hypotheses(kb: dict) -> List[str]:
    hyps = set()
    for beliefs in kb.values():
        hyps.update(beliefs.keys())
    return sorted(hyps)


def count_kb_pairs(kb: dict) -> int:
    return sum(len(beliefs) for beliefs in kb.values())


def validate_kb(kb: dict) -> bool:
    valid = True
    for symptom, beliefs in kb.items():
        total = sum(beliefs.values())
        if total > 1.0 + 1e-9:
            logger.warning(f"Gejala '{symptom}' total belief = {total:.4f} > 1.0")
            valid = False
    return valid


def initialize_kb() -> dict:
    if not os.path.exists(KB_INITIAL_PATH):
        ensure_dir(DATA_DIR)
        save_kb(KNOWLEDGE_BASE, KB_INITIAL_PATH)
        logger.info("Knowledge base awal dibuat dari nilai pakar.")
    else:
        logger.info(f"Knowledge base awal sudah ada: {KB_INITIAL_PATH}")
    return KNOWLEDGE_BASE
