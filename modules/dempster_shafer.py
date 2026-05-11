from utils import logger


def build_mass_function(symptom: str, kb: dict) -> dict:
    if symptom not in kb:
        return {"Theta": 1.0}

    beliefs = dict(kb[symptom])
    theta = max(0.0, 1.0 - sum(beliefs.values()))
    beliefs["Theta"] = theta
    return beliefs


def combine(m1: dict, m2: dict) -> dict:
    combined: dict = {}
    conflict_pairs = []
    K = 0.0

    for h1, v1 in m1.items():
        for h2, v2 in m2.items():
            if h1 == "Theta":
                intersect = h2
            elif h2 == "Theta":
                intersect = h1
            elif h1 == h2:
                intersect = h1
            else:
                intersect = None

            if intersect is None:
                K += v1 * v2
                conflict_pairs.append((h1, v1, h2, v2))
            else:
                combined[intersect] = combined.get(intersect, 0.0) + v1 * v2

    norm = 1.0 - K

    if abs(norm) < 1e-10:
        result = dict(combined)
        for h1, v1, h2, v2 in conflict_pairs:
            denom = v1 + v2
            if denom > 1e-10:
                result[h1] = result.get(h1, 0.0) + (v1 * v2 * v1) / denom
                result[h2] = result.get(h2, 0.0) + (v1 * v2 * v2) / denom

        result.pop("Theta", None)

        total_mass = sum(result.values())
        if total_mass > 1e-10:
            return {h: v / total_mass for h, v in result.items()}

        hyps = [h for h in set(list(m1.keys()) + list(m2.keys())) if h != "Theta"]
        return {h: 1.0 / len(hyps) for h in hyps} if hyps else {}

    return {h: v / norm for h, v in combined.items()}


def diagnose(symptoms: list, kb: dict) -> dict:
    mass_functions = []

    for symptom in symptoms:
        if symptom not in kb:
            logger.warning(f"Gejala tidak dikenal dalam KB: '{symptom}' — dilewati.")
            continue
        m = build_mass_function(symptom, kb)
        mass_functions.append(m)

    if not mass_functions:
        logger.warning("Tidak ada gejala valid untuk diproses.")
        return {}

    result = mass_functions[0]
    for m_next in mass_functions[1:]:
        try:
            result = combine(result, m_next)
        except ValueError as e:
            logger.error(f"Error kombinasi DS: {e}")
            return {}

    result.pop("Theta", None)

    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


def get_top_diagnosis(symptoms: list, kb: dict) -> tuple[str, float]:
    result = diagnose(symptoms, kb)
    if not result:
        return "Unknown", 0.0
    top_hyp = max(result, key=result.get)
    return top_hyp, result[top_hyp]
