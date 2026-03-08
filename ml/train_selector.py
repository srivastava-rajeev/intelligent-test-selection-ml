import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer

DATA_PATH = Path('data/processed/synthetic_commit_history.csv')
MODEL_DIR = Path('models')
MODEL_PATH = MODEL_DIR / 'selector.joblib'
MLB_PATH = MODEL_DIR / 'label_binarizer.joblib'
METRICS_PATH = MODEL_DIR / 'metrics.json'


def build_dataset(df: pd.DataFrame):
    x = df[['changed_files']].copy()
    y_labels = df['impacted_tests'].fillna('').apply(lambda s: [v for v in s.split(';') if v])
    return x, y_labels


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f'Missing dataset: {DATA_PATH}')

    df = pd.read_csv(DATA_PATH)
    x, y_labels = build_dataset(df)

    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_labels)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=7,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                'paths',
                CountVectorizer(token_pattern=r'[^;]+'),
                'changed_files',
            )
        ]
    )

    base_estimator = LogisticRegression(max_iter=1000, solver='liblinear')
    clf = OneVsRestClassifier(base_estimator)

    pipeline = Pipeline(
        steps=[
            ('features', preprocessor),
            ('clf', clf),
        ]
    )

    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)

    report = classification_report(
        y_test,
        y_pred,
        target_names=mlb.classes_,
        zero_division=0,
        output_dict=True,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(mlb, MLB_PATH)

    summary = {
        'micro_f1': report['micro avg']['f1-score'],
        'macro_f1': report['macro avg']['f1-score'],
        'weighted_f1': report['weighted avg']['f1-score'],
        'labels': list(mlb.classes_),
    }

    METRICS_PATH.write_text(json.dumps(summary, indent=2), encoding='utf-8')

    print('Training complete.')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
