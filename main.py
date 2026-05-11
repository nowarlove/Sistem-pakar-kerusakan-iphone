import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import logger, print_header, ensure_dir
from config import (
    RAW_EXCEL_PATH,
    TRAIN_CSV_PATH,
    TEST_CSV_PATH,
    KB_INITIAL_PATH,
    KB_OPTIMAL_PATH,
    RESULTS_DIR,
)
from modules.data_loader  import load_excel, print_data_summary
from modules.preprocessor  import run_preprocessing, load_processed_csv
from modules.knowledge_base import initialize_kb, save_kb, load_kb
from modules.pso_optimizer  import PSOOptimizer
from modules.evaluator      import (
    evaluate,
    plot_confusion_matrix,
    save_evaluation_report,
    print_evaluation_summary,
)
from modules.interface import run_interface


def mode_train() -> None:
    print_header("FASE TRAINING — DS-PSO iPhone")

    logger.info("── FASE 1: Data Engineering & Preprocessing ──")
    df_raw = load_excel(RAW_EXCEL_PATH)
    print_data_summary(df_raw)
    train_df, test_df = run_preprocessing(df_raw)

    logger.info("── FASE 2: Inisialisasi Knowledge Base ──")
    kb_initial = initialize_kb()

    logger.info("── FASE 3: PSO Optimizer ──")
    ensure_dir(RESULTS_DIR)
    pso = PSOOptimizer()
    kb_optimal, history = pso.optimize(train_df, kb_initial)

    save_kb(kb_optimal, KB_OPTIMAL_PATH)
    logger.info(f"Training selesai. KB optimal disimpan: {KB_OPTIMAL_PATH}")


def mode_evaluate() -> None:
    print_header("FASE EVALUASI — DS-PSO iPhone")

    for path, name in [
        (TEST_CSV_PATH, "test_data.csv"),
        (KB_OPTIMAL_PATH, "knowledge_base_optimal.json"),
    ]:
        if not os.path.exists(path):
            logger.error(
                f"File tidak ditemukan: {path}. "
                f"Jalankan mode 'train' terlebih dahulu."
            )
            sys.exit(1)

    test_df    = load_processed_csv(TEST_CSV_PATH)
    kb_optimal = load_kb(KB_OPTIMAL_PATH)

    logger.info("── FASE 5: Evaluasi Model ──")
    eval_result = evaluate(test_df, kb_optimal)

    print_evaluation_summary(eval_result)
    plot_confusion_matrix(eval_result["cm"])
    save_evaluation_report(eval_result)

    logger.info("Evaluasi selesai.")


def mode_infer() -> None:
    if os.path.exists(KB_OPTIMAL_PATH):
        kb = load_kb(KB_OPTIMAL_PATH)
        logger.info("Menggunakan Knowledge Base optimal.")
    elif os.path.exists(KB_INITIAL_PATH):
        kb = load_kb(KB_INITIAL_PATH)
        logger.warning(
            "KB optimal belum tersedia. Menggunakan KB awal (nilai pakar). "
            "Jalankan mode 'train' untuk hasil yang lebih akurat."
        )
    else:
        kb = initialize_kb()
        logger.warning("Menggunakan Knowledge Base bawaan (belum dioptimasi).")

    run_interface(kb)


def mode_all() -> None:
    mode_train()
    mode_evaluate()
    mode_infer()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sistem Pakar Diagnosa Kerusakan iPhone\n"
            "Metode Hybrid Dempster-Shafer + PSO\n"
            "NST Phoneshop, Tanjungpinang"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["train", "evaluate", "infer", "all"],
        default="all",
        help=(
            "Mode pipeline:\n"
            "  train    — preprocessing + PSO (hasilkan KB optimal)\n"
            "  evaluate — evaluasi model pada data uji\n"
            "  infer    — antarmuka konsol interaktif\n"
            "  all      — jalankan seluruh pipeline (default)"
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    MODE_MAP = {
        "train":    mode_train,
        "evaluate": mode_evaluate,
        "infer":    mode_infer,
        "all":      mode_all,
    }

    MODE_MAP[args.mode]()
