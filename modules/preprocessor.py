import ast
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from utils import logger, ensure_dir
from config import (
    STANDARDIZE_DICT,
    DAMAGE_CLASSES,
    SYMPTOM_LIST,
    DAMAGE_TO_SYMPTOMS,
    COL_KERUSAKAN,
    TRAIN_CSV_PATH,
    TEST_CSV_PATH,
    PROCESSED_DIR,
    TRAIN_SIZE,
    RANDOM_STATE,
)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    import re
    before = len(df)
    df = df.drop_duplicates()
    after_dup = len(df)
    logger.info(f"Duplikat dihapus: {before - after_dup} baris.")

    df = df.dropna(subset=[COL_KERUSAKAN])
    after_nan = len(df)
    logger.info(f"Baris NaN pada kolom kerusakan dihapus: {after_dup - after_nan} baris.")
    
    # Pisahkan nilai yang mengandung + atau /
    df[COL_KERUSAKAN] = df[COL_KERUSAKAN].astype(str)
    df[COL_KERUSAKAN] = df[COL_KERUSAKAN].apply(lambda x: re.sub(r'[+/]', '|', x))
    df[COL_KERUSAKAN] = df[COL_KERUSAKAN].str.split('|')
    df = df.explode(COL_KERUSAKAN)
    df[COL_KERUSAKAN] = df[COL_KERUSAKAN].str.strip()
    df = df[df[COL_KERUSAKAN] != '']

    after_split = len(df)
    logger.info(f"Data setelah pemisahan (split by + dan /): {after_split} baris.")
    
    return df.reset_index(drop=True)


def standardize_labels(df: pd.DataFrame) -> pd.DataFrame:
    std_dict_norm = {
        k.strip().title(): v for k, v in STANDARDIZE_DICT.items()
    }

    def _map_label(text: str) -> str:
        normalized = str(text).strip().title()
        return std_dict_norm.get(normalized, normalized)

    df = df.copy()
    df["label"] = df[COL_KERUSAKAN].apply(_map_label)

    unknown_mask = ~df["label"].isin(DAMAGE_CLASSES)
    n_unknown = unknown_mask.sum()
    if n_unknown > 0:
        unknown_vals = df.loc[unknown_mask, "label"].unique()
        logger.warning(
            f"{n_unknown} baris dengan label tidak dikenal akan dihapus: {unknown_vals}"
        )
        df = df[~unknown_mask].reset_index(drop=True)

    logger.info(f"Standardisasi label: {len(df)} baris valid dari 11 kelas baku.")
    return df


def extract_symptoms(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["symptoms"] = df["label"].map(
        lambda lbl: DAMAGE_TO_SYMPTOMS.get(lbl, [])
    )
    no_symptom = (df["symptoms"].apply(len) == 0).sum()
    if no_symptom > 0:
        logger.warning(f"{no_symptom} baris tidak memiliki gejala terpetakan.")
    logger.info("Ekstraksi gejala selesai.")
    return df


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    le = LabelEncoder()
    le.fit(DAMAGE_CLASSES)
    df["label_enc"] = le.transform(df["label"])
    logger.info(f"Label encoding: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    for symptom in SYMPTOM_LIST:
        col_name = f"g_{symptom.replace(' ', '_')}"
        df[col_name] = df["symptoms"].apply(lambda syms: int(symptom in syms))

    logger.info(f"Binary encoding: {len(SYMPTOM_LIST)} kolom gejala ditambahkan.")
    return df


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    min_class_count = df["label"].value_counts().min()
    use_stratify = min_class_count >= 2

    if not use_stratify:
        small_classes = df["label"].value_counts()[df["label"].value_counts() < 2].index.tolist()
        logger.warning(
            f"Kelas {small_classes} hanya punya 1 sampel. "
            f"Menggunakan split non-stratified."
        )

    train_df, test_df = train_test_split(
        df,
        train_size=TRAIN_SIZE,
        stratify=df["label"] if use_stratify else None,
        random_state=RANDOM_STATE,
    )
    logger.info(f"Split data: {len(train_df)} train, {len(test_df)} test.")
    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def save_processed(train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    ensure_dir(PROCESSED_DIR)

    train_save = train_df.copy()
    test_save  = test_df.copy()
    train_save["symptoms"] = train_save["symptoms"].apply(str)
    test_save["symptoms"]  = test_save["symptoms"].apply(str)

    train_save.to_csv(TRAIN_CSV_PATH, index=False)
    test_save.to_csv(TEST_CSV_PATH, index=False)
    logger.info(f"Train CSV disimpan: {TRAIN_CSV_PATH}")
    logger.info(f"Test CSV disimpan : {TEST_CSV_PATH}")


def load_processed_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "symptoms" in df.columns:
        df["symptoms"] = df["symptoms"].apply(ast.literal_eval)
    return df


def run_preprocessing(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    logger.info("=== MEMULAI PREPROCESSING ===")
    df = clean_data(df_raw)
    df = standardize_labels(df)
    df = extract_symptoms(df)
    df = encode_features(df)
    train_df, test_df = split_data(df)
    save_processed(train_df, test_df)
    logger.info("=== PREPROCESSING SELESAI ===\n")
    return train_df, test_df
