import logging
import os
from datetime import datetime
from typing import Any


def setup_logger(name: str = "ds_pso", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger()


def print_header(title: str, width: int = 50) -> None:
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_table(headers: list, rows: list, col_widths: list = None) -> None:
    if col_widths is None:
        col_widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) + 2
                      for i, h in enumerate(headers)]

    sep = "+" + "+".join("-" * w for w in col_widths) + "+"
    fmt = "|" + "|".join(f" {{:<{w-1}}}" for w in col_widths) + "|"

    print(sep)
    print(fmt.format(*headers))
    print(sep.replace("-", "="))
    for row in rows:
        print(fmt.format(*[str(v) for v in row]))
    print(sep)


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def validate_indices(input_str: str, max_index: int) -> list:
    parts = [p.strip() for p in input_str.split(",") if p.strip()]
    indices = []
    for p in parts:
        if not p.isdigit():
            raise ValueError(f"'{p}' bukan angka valid.")
        idx = int(p)
        if idx < 1 or idx > max_index:
            raise ValueError(f"Indeks {idx} di luar range (1–{max_index}).")
        indices.append(idx - 1)
    return indices


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")
