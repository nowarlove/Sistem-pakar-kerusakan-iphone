"""
NST Phone Repair — Sistem Pakar Diagnosis Kerusakan iPhone
Flask Web Application Backend
"""
import json
import os
from flask import Flask, render_template, request, jsonify

from core.normalizer import normalize_text
from core.feature_extractor import extract_features
from core.ds_engine import DSEngine

# ---------------------------------------------------------------
# Path Setup
# ---------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
KB_PATH = os.path.join(DATA_DIR, 'optimal_knowledge_base.json')

# ---------------------------------------------------------------
# Load Knowledge Base saat startup
# ---------------------------------------------------------------
with open(KB_PATH, 'r', encoding='utf-8') as f:
    KNOWLEDGE_BASE = json.load(f)

engine = DSEngine(KNOWLEDGE_BASE)

# ---------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    """
    Menerima JSON: {"nama": "...", "tipe_hp": "...", "keluhan": "..."}
    Mengembalikan JSON hasil diagnosis lengkap + dev_log.
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Data tidak valid.'}), 400

    nama = data.get('nama', '').strip()
    tipe_hp = data.get('tipe_hp', '').strip()
    keluhan_raw = data.get('keluhan', '').strip()

    if not nama:
        return jsonify({'success': False, 'error': 'Nama pelanggan harus diisi.'}), 400
    if not tipe_hp:
        return jsonify({'success': False, 'error': 'Tipe ponsel harus diisi.'}), 400
    if not keluhan_raw:
        return jsonify({'success': False, 'error': 'Keluhan tidak boleh kosong.'}), 400

    normalized = normalize_text(keluhan_raw)
    features = extract_features(normalized)
    result = engine.run_inference(features)

    return jsonify({
        'success': True,
        'customer': {
            'nama': nama,
            'tipe_hp': tipe_hp,
        },
        'input': {
            'raw': keluhan_raw,
            'normalized': normalized,
        },
        'features': features,
        **result,
    })


@app.route('/model-info')
def model_info():
    """Mengembalikan seluruh basis pengetahuan optimal (untuk menu Pengembangan)."""
    return jsonify({
        'rules': KNOWLEDGE_BASE['rules'],
        'class_priors': KNOWLEDGE_BASE['class_priors'],
        'total_rules': len(KNOWLEDGE_BASE['rules']),
        'total_classes': len(KNOWLEDGE_BASE['class_priors']),
    })


if __name__ == '__main__':
    print("=" * 55)
    print("  NST Phone Repair — Sistem Pakar Kerusakan iPhone")
    print("  Buka browser: http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)
