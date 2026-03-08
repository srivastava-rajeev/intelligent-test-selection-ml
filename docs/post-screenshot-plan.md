# Post Screenshot Plan (Dev.to + LinkedIn)

Use real project evidence to make the post look authentic and engineering-led.

## Must-have images

1. Model training metrics
- Command: `python3 ml/train_selector.py`
- Capture: terminal block with `micro_f1`, `macro_f1`, `weighted_f1`

2. Intelligent selection output
- Command: `python3 ci/select_tests.py --changed-files src/services/inventory.js src/services/order.js`
- Capture: selected tests list + `SELECTED_TESTS=...`

3. Full suite run
- Command: `npm test`
- Capture: final summary line (`6 passed`)

4. Selected suite run
- Command:
  `SELECTED_TESTS="tests/playwright/tests/inventory.spec.js,tests/playwright/tests/order.spec.js" npm run test:selected`
- Capture: final summary line (`4 passed`)

5. CI evidence
- Capture GitHub Actions workflow run page and successful job status.

## Optional image

- Architecture diagram showing the flow:
  `Code Change -> Feature Extraction -> ML Selector -> Test Subset -> Playwright -> Feedback`

## Placement recommendation

- Dev.to: put screenshots immediately after each relevant section.
- LinkedIn: use 2-3 images max (selector output, full vs selected test run, Actions run).

## Authenticity checklist

- Use your own terminal and GitHub run screenshots.
- Keep timestamps and command prompts visible.
- Do not use generated stock images.
- Mention: independent research-style project, synthetic/non-proprietary dataset.
