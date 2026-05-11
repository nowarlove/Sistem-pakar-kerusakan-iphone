import os
import pandas as pd
from utils import logger
from config import (
    RAW_EXCEL_PATH,
    REQUIRED_COLUMNS,
    COL_KERUSAKAN,
)


def load_excel(path: str = RAW_EXCEL_PATH) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    logger.info(f"Memuat data dari: {path}")
    all_sheets = pd.read_excel(path, engine="openpyxl", sheet_name=None)

    frames = []
    for sheet_name, df_sheet in all_sheets.items():
        logger.info(f"  Sheet '{sheet_name}': {len(df_sheet)} baris")
        frames.append(df_sheet)

    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(axis=1, how="all")
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df.columns = df.columns.str.strip()
    logger.info(f"Total gabungan: {len(df)} baris dari {len(all_sheets)} sheet, {len(df.columns)} kolom.")
    logger.info(f"Kolom tersedia: {list(df.columns)}")

    _validate_columns(df)
    return df


def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    logger.info(f"Memuat CSV dari: {path}")
    df = pd.read_csv(path)
    logger.info(f"CSV dimuat — {len(df)} baris.")
    return df


def _validate_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise KeyError(
            f"Kolom wajib tidak ditemukan: {missing}. "
            f"Kolom tersedia: {list(df.columns)}"
        )
    logger.info("Validasi kolom: OK.")


def get_data_info(df: pd.DataFrame) -> dict:
    info = {
        "total_rows":       len(df),
        "total_columns":    len(df.columns),
        "columns":          list(df.columns),
        "missing_values":   df.isnull().sum().to_dict(),
        "duplicates":       int(df.duplicated().sum()),
    }
    if COL_KERUSAKAN in df.columns:
        info["unique_damage_types"] = df[COL_KERUSAKAN].nunique()
        info["damage_distribution"] = df[COL_KERUSAKAN].value_counts().to_dict()

    return info


def print_data_summary(df: pd.DataFrame) -> None:
    info = get_data_info(df)
    print("\n" + "=" * 50)
    print("  RINGKASAN DATASET")
    print("=" * 50)
    print(f"  Total baris        : {info['total_rows']}")
    print(f"  Total kolom        : {info['total_columns']}")
    print(f"  Duplikat           : {info['duplicates']}")
    print(f"  Kolom              : {info['columns']}")
    print(f"  Missing values     : {info['missing_values']}")
    if "unique_damage_types" in info:
        print(f"  Jenis kerusakan    : {info['unique_damage_types']}")
    print("=" * 50 + "\n")
