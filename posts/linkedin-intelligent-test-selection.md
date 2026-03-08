Built a new ML + Playwright prototype for faster CI/CD:

Machine Learning Based Intelligent Test Selection for Faster CI/CD Pipelines

Problem:
Large regression suites slow delivery because every commit runs everything.

Approach:
Train an ML model on historical commit change patterns and impacted tests, then run only predicted tests first.

Example:
If commit touches `inventory service`, model can select:
- inventory tests
- order tests

Result target:
70-80% faster feedback loops (with fallback safety strategy).

Stack used:
- Playwright
- Python (scikit-learn)
- GitHub Actions

Repo:
https://github.com/srivastava-rajeev/intelligent-test-selection-ml

This extends my earlier work on flaky test prediction and moves toward smarter, risk-aware CI execution.

#MachineLearning #Testing #Playwright #CICD #DevOps #QualityEngineering #MLOps
