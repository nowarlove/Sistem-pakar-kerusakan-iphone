import re

# ---------------------------------------------------------------
# Feature Extractor
# Mengekstrak 11 kolom gejala terstruktur dari teks keluhan bebas.
# Logika disalin dari map_row() di preprocessing.ipynb (read-only).
# ---------------------------------------------------------------


def _match(text: str, keywords: list) -> bool:
    """Cek apakah salah satu keyword ditemukan dalam teks."""
    patterns = []
    for k in keywords:
        escaped = re.escape(k).replace(r'\ ', r'\s+')
        patterns.append(rf'\b{escaped}\b')
    pattern = '|'.join(patterns)
    return bool(re.search(pattern, text, re.IGNORECASE))


def extract_features(normalized_text: str) -> dict:
    """
    Menerima teks yang sudah dinormalisasi,
    mengembalikan dict 11 gejala terstruktur.
    """
    t = normalized_text.lower()

    # 1. Signal
    if _match(t, ['sinyal hilang', 'signal hilang', 'hilang jaringan',
                  'modem', 'baseband', 'no signal', 'keblokir']):
        signal = 'Hilang Total'
    elif _match(t, ['sinyal lemah', 'signal lemah', 'sinyal naik turun',
                    'signal hilang timbul']):
        signal = 'Bar Rendah'
    else:
        signal = 'Normal'

    # 2. Baterai
    if _match(t, ['baterai', 'kembung', 'drop', 'boros',
                  'mentok 0%', 'turun']):
        baterai = 'Daya Tahan Rendah/Gembung'
    else:
        baterai = 'Normal'

    # 3. LCD
    has_lcd_kw = _match(t, ['greenscreen', 'greenline', 'hijau'])
    has_gelap_kw = (
        _match(t, ['blank', 'blackscreen', 'gelap', 'retak', 'garis', 'pecah'])
        and not _match(t, ['backdoor', 'kaca belakang', 'punggung',
                           'housing', 'casing', 'bodi'])
    )
    has_pecah_general = (
        _match(t, ['pecah'])
        and not _match(t, ['suara', 'speaker', 'audio', 'buzzer',
                           'backdoor', 'kaca belakang', 'punggung',
                           'housing', 'casing', 'bodi'])
    )
    if has_lcd_kw:
        lcd = 'Greenscreen'
    elif has_gelap_kw or has_pecah_general:
        lcd = 'Gelap'
    else:
        lcd = 'Normal'

    # 4. Wifi
    if _match(t, ['wifi']):
        wifi = 'Hilang Timbul'
    else:
        wifi = 'Normal'

    # 5. Touchscreen
    if _match(t, ['disentuh', 'sentuh', 'touchscreen', 'ghostouch', 'ngefreeze']):
        touch = 'Tidak bisa disentuh'
    else:
        touch = 'Normal'

    # 6. Tegangan
    if _match(t, ['korsleting', 'mati total', 'mati', 'korosi',
                  'basah', 'kena air', 'masuk air']):
        if _match(t, ['tombol', 'kamera', 'speaker', 'wifi']):
            tegangan = '0,8 - 2,2'
        else:
            tegangan = '0,0'
    elif _match(t, ['tegangan rendah', 'vcc main', 'baterai drop']):
        tegangan = '0,6'
    else:
        tegangan = '0,8 - 2,2'

    # 7. Kamera
    if _match(t, ['kamera', 'foto', 'buram', 'jamur', 'getar']):
        kamera = 'Blank'
    else:
        kamera = 'Normal'

    # 8. Konektor Cas
    if _match(t, ['tidak bisa dicas', 'dicas mati', 'dicas tidak naik',
                  'dicas keluar masuk', 'konektor cas', 'dicas', 'cas', 'konektor']):
        if _match(t, ['keluar masuk', 'longgar', 'kotor']):
            konektor = 'Keluar masuk'
        else:
            konektor = 'Tidak Ngecas'
    else:
        konektor = 'Normal'

    # 9. Speaker
    has_speaker_kw = _match(t, ['suara', 'speaker', 'buzzer', 'audio',
                                 'mikrofon', 'microphone', 'tidak terdengar',
                                 'rekam suara'])
    has_pecah_speaker = (
        _match(t, ['pecah'])
        and _match(t, ['suara', 'speaker', 'buzzer', 'audio'])
    )
    if has_speaker_kw or has_pecah_speaker:
        speaker = 'Tidak ada suara'
    else:
        speaker = 'Normal'

    # 10. Backdoor
    if _match(t, ['backdoor', 'kaca belakang', 'punggung',
                  'housing', 'casing', 'bodi']):
        backdoor = 'Pecah/Retak'
    else:
        backdoor = 'Normal'

    # 11. Tombol
    if _match(t, ['tombol', 'power', 'volume', 'haptic', 'haptik',
                  'switch', 'silent', 'home', 'on off', 'on/off']):
        tombol = 'Tidak Berfungsi'
    else:
        tombol = 'Normal'

    return {
        'Signal': signal,
        'Baterai': baterai,
        'LCD': lcd,
        'Wifi': wifi,
        'Touchscreen': touch,
        'Tegangan': tegangan,
        'Kamera': kamera,
        'Konektor Cas': konektor,
        'Speaker': speaker,
        'Backdoor': backdoor,
        'Tombol': tombol,
    }
