import os
import ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from utils import logger, ensure_dir
from config import (
    CONFUSION_IMG_PATH,
    EVAL_REPORT_PATH,
    RESULTS_DIR,
    DAMAGE_CLASSES,
)
from modules.dempster_shafer import get_top_diagnosis


def evaluate(test_data: pd.DataFrame, kb_optimal: dict) -> dict:
    y_true, y_pred = [], []

    for _, row in test_data.iterrows():
        symptoms = row["symptoms"]
        if isinstance(symptoms, str):
            symptoms = ast.literal_eval(symptoms)

        pred, _ = get_top_diagnosis(symptoms, kb_optimal)
        y_true.append(row["label"])
        y_pred.append(pred)

    acc    = accuracy_score(y_true, y_pred)
    report = classification_report(
        y_true, y_pred,
        labels=DAMAGE_CLASSES,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_true, y_pred, labels=DAMAGE_CLASSES)

    logger.info(f"Akurasi sistem DS-PSO: {acc * 100:.2f}%")
    return {
        "accuracy": acc,
        "report":   report,
        "cm":       cm,
        "y_true":   y_true,
        "y_pred":   y_pred,
    }


def plot_confusion_matrix(cm, labels: list = DAMAGE_CLASSES,
                          save_path: str = CONFUSION_IMG_PATH) -> None:
    ensure_dir(RESULTS_DIR)

    short_labels = [
        lbl.replace(" Rusak", "").replace("Signal ", "").replace("Pengisian ", "")
        for lbl in labels
    ]

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=short_labels,
        yticklabels=short_labels,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title(
        "Confusion Matrix — Sistem Pakar DS-PSO iPhone\nNST Phoneshop Tanjungpinang",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.set_xlabel("Prediksi", fontsize=11)
    ax.set_ylabel("Aktual", fontsize=11)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Confusion matrix disimpan: {save_path}")


def save_evaluation_report(eval_result: dict,
                            path: str = EVAL_REPORT_PATH) -> None:
    ensure_dir(RESULTS_DIR)
    report = eval_result["report"]

    rows = []
    for label in DAMAGE_CLASSES:
        if label in report:
            rows.append({
                "Kelas":     label,
                "Precision": round(report[label]["precision"], 4),
                "Recall":    round(report[label]["recall"], 4),
                "F1-Score":  round(report[label]["f1-score"], 4),
                "Support":   int(report[label]["support"]),
            })

    if "macro avg" in report:
        rows.append({
            "Kelas":     "Macro Average",
            "Precision": round(report["macro avg"]["precision"], 4),
            "Recall":    round(report["macro avg"]["recall"], 4),
            "F1-Score":  round(report["macro avg"]["f1-score"], 4),
            "Support":   int(report["macro avg"]["support"]),
        })
    rows.append({
        "Kelas":     "Accuracy",
        "Precision": "",
        "Recall":    "",
        "F1-Score":  round(eval_result["accuracy"], 4),
        "Support":   "",
    })

    df_report = pd.DataFrame(rows)
    df_report.to_csv(path, index=False, encoding="utf-8")
    logger.info(f"Laporan evaluasi disimpan: {path}")


def print_evaluation_summary(eval_result: dict) -> None:
    acc    = eval_result["accuracy"]
    report = eval_result["report"]

    print("\n" + "=" * 62)
    print("  LAPORAN EVALUASI — DS-PSO iPhone")
    print("=" * 62)
    print(f"  {'Kelas':<25} {'Prec':>6}  {'Recall':>6}  {'F1':>6}  {'N':>5}")
    print("-" * 62)

    for label in DAMAGE_CLASSES:
        if label in report:
            r = report[label]
            print(
                f"  {label:<25} "
                f"{r['precision']:>6.3f}  "
                f"{r['recall']:>6.3f}  "
                f"{r['f1-score']:>6.3f}  "
                f"{int(r['support']):>5}"
            )

    print("-" * 62)
    if "macro avg" in report:
        ma = report["macro avg"]
        print(
            f"  {'Macro Average':<25} "
            f"{ma['precision']:>6.3f}  "
            f"{ma['recall']:>6.3f}  "
            f"{ma['f1-score']:>6.3f}"
        )
    print(f"\n  >> Akurasi Total : {acc * 100:.2f}%")
    print("=" * 62 + "\n")
