import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from utils import logger, ensure_dir
from config import PSO_CONFIG, GBEST_CSV_PATH, RESULTS_DIR
from modules.dempster_shafer import get_top_diagnosis


def encode_kb(kb: dict) -> tuple[np.ndarray, list]:
    values = []
    index_map = []
    for symptom, beliefs in kb.items():
        for hyp, val in beliefs.items():
            values.append(val)
            index_map.append((symptom, hyp))
    return np.array(values, dtype=float), index_map


def decode_particle(particle: np.ndarray, index_map: list, kb_template: dict) -> dict:
    kb_new = {symptom: {} for symptom in kb_template}
    for idx, (symptom, hyp) in enumerate(index_map):
        kb_new[symptom][hyp] = float(np.clip(particle[idx], 0.0, 1.0))
    return kb_new


def fitness_function(particle: np.ndarray, index_map: list,
                     kb_template: dict, train_data: pd.DataFrame) -> float:
    kb_temp = decode_particle(particle, index_map, kb_template)

    y_true, y_pred = [], []
    for _, row in train_data.iterrows():
        symptoms = row["symptoms"]
        if isinstance(symptoms, str):
            import ast
            symptoms = ast.literal_eval(symptoms)
        pred, _ = get_top_diagnosis(symptoms, kb_temp)
        y_true.append(row["label"])
        y_pred.append(pred)

    return accuracy_score(y_true, y_pred)


class PSOOptimizer:
    def __init__(self, config=None):
        self.config = config or PSO_CONFIG

    def optimize(self, train_data: pd.DataFrame, kb: dict) -> tuple[dict, list]:
        cfg = self.config
        np.random.seed(cfg.random_state)

        x0, index_map = encode_kb(kb)
        n_dim = len(x0)
        logger.info(f"Dimensi PSO: {n_dim} (pasangan gejala-kerusakan)")

        X = np.random.uniform(cfg.x_min, cfg.x_max, (cfg.n_particles, n_dim))
        V = np.random.uniform(-cfg.v_max, cfg.v_max, (cfg.n_particles, n_dim))

        X[0] = np.clip(x0, cfg.x_min, cfg.x_max)

        pbest     = X.copy()
        pbest_fit = np.full(cfg.n_particles, -np.inf)
        gbest     = None
        gbest_fit = -np.inf
        gbest_history = []

        logger.info(f"Memulai PSO: {cfg.n_particles} partikel, {cfg.max_iter} iterasi.")

        stable_count = 0
        prev_gbest_fit = -np.inf

        for it in range(cfg.max_iter):
            w = cfg.w_max - (cfg.w_max - cfg.w_min) / cfg.max_iter * it

            for i in range(cfg.n_particles):
                fit = fitness_function(X[i], index_map, kb, train_data)
                if fit > pbest_fit[i]:
                    pbest[i]     = X[i].copy()
                    pbest_fit[i] = fit
                if fit > gbest_fit:
                    gbest     = X[i].copy()
                    gbest_fit = fit

            gbest_history.append({"iter": it + 1, "gbest_fitness": gbest_fit})

            if (it + 1) % 10 == 0 or it == 0:
                logger.info(
                    f"  Iter {it + 1:>3}/{cfg.max_iter} | "
                    f"w={w:.4f} | Gbest Fitness={gbest_fit:.4f}"
                )

            if abs(gbest_fit - prev_gbest_fit) < cfg.converge_tol:
                stable_count += 1
            else:
                stable_count = 0
            prev_gbest_fit = gbest_fit

            if stable_count >= cfg.converge_n:
                logger.info(
                    f"PSO konvergen pada iterasi {it + 1} "
                    f"(stabil {cfg.converge_n} iterasi berturut-turut)."
                )
                break

            r1 = np.random.rand(cfg.n_particles, n_dim)
            r2 = np.random.rand(cfg.n_particles, n_dim)
            V  = (w * V
                  + cfg.c1 * r1 * (pbest - X)
                  + cfg.c2 * r2 * (gbest - X))
            V  = np.clip(V, -cfg.v_max, cfg.v_max)

            X = np.clip(X + V, cfg.x_min, cfg.x_max)

        logger.info(f"PSO selesai. Gbest Fitness = {gbest_fit:.4f} ({gbest_fit*100:.2f}%)")

        kb_optimal = decode_particle(gbest, index_map, kb)
        self._save_history(gbest_history)
        return kb_optimal, gbest_history

    def _save_history(self, gbest_history: list) -> None:
        import csv
        ensure_dir(RESULTS_DIR)
        with open(GBEST_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["iter", "gbest_fitness"])
            writer.writeheader()
            writer.writerows(gbest_history)
        logger.info(f"Riwayat PSO disimpan: {GBEST_CSV_PATH}")
