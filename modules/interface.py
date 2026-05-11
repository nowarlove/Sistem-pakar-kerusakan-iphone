from utils import logger, print_header, format_percent
from config import SYMPTOM_LIST
from modules.dempster_shafer import diagnose


def show_symptom_menu() -> None:
    print("\nDaftar gejala yang tersedia:")
    print("-" * 40)
    for i, symptom in enumerate(SYMPTOM_LIST, start=1):
        print(f"  [{i:>2}]  {symptom}")
    print("-" * 40)


def get_user_symptoms() -> list:
    while True:
        try:
            raw = input(
                "\nMasukkan nomor gejala (pisahkan dengan koma, contoh: 3,5,9):\n> "
            ).strip()
            if not raw:
                print("⚠  Input tidak boleh kosong. Coba lagi.")
                continue

            parts = [p.strip() for p in raw.split(",") if p.strip()]
            selected = []
            valid = True

            for p in parts:
                if not p.isdigit():
                    print(f"⚠  '{p}' bukan angka. Coba lagi.")
                    valid = False
                    break
                idx = int(p)
                if idx < 1 or idx > len(SYMPTOM_LIST):
                    print(f"⚠  Nomor {idx} di luar range (1–{len(SYMPTOM_LIST)}). Coba lagi.")
                    valid = False
                    break
                symptom = SYMPTOM_LIST[idx - 1]
                if symptom not in selected:
                    selected.append(symptom)

            if valid and selected:
                return selected

        except KeyboardInterrupt:
            print("\n\nDiagnosis dibatalkan oleh user.")
            return []


def show_diagnosis_result(symptoms: list, result: dict) -> None:
    print("\n🔍 Memproses diagnosis...")
    print()
    print("Gejala yang dipilih:")
    for s in symptoms:
        print(f"  • {s}")
    print()

    if not result:
        print("❌ Tidak ada diagnosis yang dapat dihasilkan.")
        print("   (Gejala mungkin tidak terdaftar dalam knowledge base.)")
        return

    theta = max(0.0, 1.0 - sum(result.values()))

    w_hyp  = 25
    w_pct  = 10
    sep    = "+" + "-" * (w_hyp + 2) + "+" + "-" * (w_pct + 2) + "+"
    header = f"| {'Hipotesis':<{w_hyp}} | {'Keyakinan':>{w_pct}} |"
    row_fmt = "| {:<{w_hyp}} | {:>{w_pct}} |"

    print("HASIL DIAGNOSIS:")
    print(sep)
    print(header)
    print(sep.replace("-", "="))

    for hyp, belief in result.items():
        print(row_fmt.format(hyp, format_percent(belief), w_hyp=w_hyp, w_pct=w_pct))

    if theta > 0.001:
        print(row_fmt.format("Ketidakpastian", format_percent(theta), w_hyp=w_hyp, w_pct=w_pct))

    print(sep)

    top_hyp  = max(result, key=result.get)
    top_conf = result[top_hyp]
    print(f"\n→ Diagnosis: \033[1m{top_hyp}\033[0m ({format_percent(top_conf)})")


def run_interface(kb: dict) -> None:
    print_header("SISTEM PAKAR KERUSAKAN IPHONE\n  DS-PSO | NST Phoneshop Tanjungpinang", width=50)
    logger.info("Antarmuka konsol dimulai.")

    while True:
        show_symptom_menu()
        symptoms = get_user_symptoms()

        if not symptoms:
            break

        result = diagnose(symptoms, kb)
        show_diagnosis_result(symptoms, result)

        print()
        again = input("Diagnosis lain? (y/n): ").strip().lower()
        if again != "y":
            print("\nTerima kasih telah menggunakan Sistem Pakar Kerusakan iPhone.\n")
            break
