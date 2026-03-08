# Machine Learning Based Intelligent Test Selection for Faster CI/CD Pipelines

CI pipelines become slow as regression suites grow. In many teams, every commit triggers full test execution even when only a few components changed.

In this project, I built a practical prototype that predicts impacted Playwright tests using machine learning.

## Research Note

This is an independent research-style implementation. I did not use proprietary company data. The current version is trained on synthetic, reproducible commit-impact history to validate the approach.

## The Problem

When all tests run on every commit:
- feedback is delayed
- compute cost increases
- developer productivity drops

For large systems, this creates a release bottleneck.

## The Idea

Use historical data from CI:
- changed files in commit
- tests that were impacted (failed, flaky, or behaviorally affected)

Train a model that maps file-change patterns to impacted test files.

Then in CI:
1. detect changed files
2. predict relevant tests
3. run only selected tests first
4. keep full-suite fallback/nightly run for safety

## Example

Commit touches:
- `src/services/inventory.js`

Model predicts:
- `tests/playwright/tests/inventory.spec.js`
- `tests/playwright/tests/order.spec.js`

This gives much faster feedback compared to running all tests.

## Tech Stack

- Playwright for test execution
- Python + scikit-learn for model training/inference
- GitHub Actions for CI integration

## Implementation Summary

The repository includes:
- synthetic commit-impact dataset generator
- multi-label classifier (`OneVsRest + LogisticRegression`)
- prediction utility with threshold and safe fallback
- CI script that exports `SELECTED_TESTS`
- Playwright runner that executes just selected spec files

## Why This Matters

Intelligent test selection is a practical way to improve CI throughput. With good historical data and conservative fallback strategy, teams can achieve significant speedups while preserving confidence.

In many repositories this can reduce per-commit test time by 70-80%.

## Screenshots To Add (Recommended)

To keep this post grounded and non-generic, add these screenshots from real runs:

1. Terminal output of model training (`python3 ml/train_selector.py`) showing F1 scores.
2. Terminal output of selector (`python3 ci/select_tests.py --changed-files ...`) showing selected tests.
3. Playwright full run summary (`6 passed`) vs selected run summary (`4 passed`).
4. GitHub Actions run page for `.github/workflows/intelligent-test-selection.yml`.
5. Optional architecture visual from `docs/architecture.md` converted to a clean diagram image.

Use your own run logs/screenshots only. Avoid synthetic stock images.

## Repository

[GitHub - intelligent-test-selection-ml](https://github.com/srivastava-rajeev/intelligent-test-selection-ml)

If you want, I can share next steps for production hardening (coverage guards, risk bands, retraining cadence, and drift monitoring).
