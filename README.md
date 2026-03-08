# Machine Learning Based Intelligent Test Selection for Faster CI/CD Pipelines

A reproducible prototype that uses machine learning to predict which Playwright tests should run for a given code change.

![License](https://img.shields.io/github/license/srivastava-rajeev/intelligent-test-selection-ml)
![Last Commit](https://img.shields.io/github/last-commit/srivastava-rajeev/intelligent-test-selection-ml)
![Repo Size](https://img.shields.io/github/repo-size/srivastava-rajeev/intelligent-test-selection-ml)

---

## Problem

Large regression suites make CI/CD pipelines slower and more expensive. Teams often run all tests for every commit, even when only a small subset is impacted.

## Solution

Train a machine learning model on historical commit-to-test-impact data. For every new commit, predict only impacted tests and run those first.

Example:

- Commit touches `src/services/inventory.js`
- Model selects:
  - `tests/playwright/tests/inventory.spec.js`
  - `tests/playwright/tests/order.spec.js`

Expected outcome: 70-80% faster feedback loops in many repositories (depends on historical data quality and fallback policies).

---

## Architecture

Code Change -> Feature Extraction -> ML Selector -> Test Subset -> Playwright Run -> Feedback Logs -> Retraining

See [docs/architecture.md](docs/architecture.md).

---

## Project Structure

```text
intelligent-test-selection-ml/
├── ci/
│   └── select_tests.py
├── data/
│   └── processed/
│       └── synthetic_commit_history.csv
├── docs/
│   └── architecture.md
├── ml/
│   ├── generate_synthetic_history.py
│   ├── train_selector.py
│   └── predict_tests.py
├── posts/
│   ├── devto-intelligent-test-selection.md
│   └── linkedin-intelligent-test-selection.md
├── src/
│   └── services/
│       ├── inventory.js
│       ├── order.js
│       └── payment.js
├── tests/
│   └── playwright/
│       ├── playwright.config.js
│       └── tests/
│           ├── inventory.spec.js
│           ├── order.spec.js
│           └── payment.spec.js
├── .github/workflows/
│   └── intelligent-test-selection.yml
├── package.json
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/srivastava-rajeev/intelligent-test-selection-ml.git
cd intelligent-test-selection-ml
```

### 2. Python setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Train selector model

```bash
python3 ml/generate_synthetic_history.py
python3 ml/train_selector.py
```

### 4. Predict tests for a commit

```bash
python3 ci/select_tests.py \
  --changed-files src/services/inventory.js src/services/order.js
```

### 5. Run selected Playwright tests

```bash
npm install
npx playwright install
SELECTED_TESTS="tests/playwright/tests/inventory.spec.js,tests/playwright/tests/order.spec.js" npm run test:selected
```

---

## CI Integration Strategy

1. Detect changed files from git diff.
2. Run `ci/select_tests.py` to choose impacted tests.
3. Execute selected tests first.
4. Optionally run full suite as nightly safety net.
5. Continuously retrain using latest CI outcomes.

---

## Publish Plan

- Dev.to draft: [posts/devto-intelligent-test-selection.md](posts/devto-intelligent-test-selection.md)
- LinkedIn draft: [posts/linkedin-intelligent-test-selection.md](posts/linkedin-intelligent-test-selection.md)

---

## License

MIT
