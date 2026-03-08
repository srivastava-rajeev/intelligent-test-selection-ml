import argparse
import json
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path('models/selector.joblib')
MLB_PATH = Path('models/label_binarizer.joblib')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Predict impacted tests from changed files.')
    parser.add_argument('--changed-files', nargs='+', required=True, help='List of changed file paths')
    parser.add_argument('--threshold', type=float, default=0.35, help='Probability threshold')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not MODEL_PATH.exists() or not MLB_PATH.exists():
        raise FileNotFoundError('Model artifacts missing. Run ml/train_selector.py first.')

    model = joblib.load(MODEL_PATH)
    mlb = joblib.load(MLB_PATH)

    changed = ';'.join(args.changed_files)
    x = pd.DataFrame([{'changed_files': changed}])

    probabilities = model.predict_proba(x)[0]

    selected = []
    scored = []
    for label, prob in zip(mlb.classes_, probabilities):
        p = float(prob)
        scored.append({'test': label, 'probability': round(p, 4)})
        if p >= args.threshold:
            selected.append(label)

    if not selected:
        # Conservative fallback: run all known tests.
        selected = list(mlb.classes_)

    output = {
        'changed_files': args.changed_files,
        'threshold': args.threshold,
        'selected_tests': selected,
        'scores': sorted(scored, key=lambda x: x['probability'], reverse=True),
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
