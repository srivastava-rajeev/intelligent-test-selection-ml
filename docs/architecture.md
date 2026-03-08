# Intelligent Test Selection Architecture

## Goal

Predict the smallest reliable subset of tests to execute for each commit.

## Pipeline

1. Collect historical commits:
   - changed files
   - tests that actually failed or were impacted
2. Featurize changed paths using a text vectorizer.
3. Train a multi-label model (`OneVsRestClassifier(LogisticRegression)`).
4. Predict impacted tests for new commit changes.
5. Apply confidence threshold and fallback policy.
6. Run selected Playwright tests in CI.
7. Log actual outcomes and retrain periodically.

## Safety Controls

- Confidence threshold (`--threshold`) to reduce false negatives.
- Fallback to running all tests if no label clears threshold.
- Nightly full-suite execution for regression catch-up.

## Why This Works

File paths carry strong signal about test impact in modular systems. For example:

- `src/services/inventory.js` -> inventory tests, possibly order tests
- `src/services/order.js` -> order tests
- shared utility changes -> broader impact

With sufficient historical data, model confidence improves and CI cycle time drops significantly.
