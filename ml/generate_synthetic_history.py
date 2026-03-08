import csv
import random
from pathlib import Path

OUTPUT = Path('data/processed/synthetic_commit_history.csv')

TESTS = [
    'tests/playwright/tests/inventory.spec.js',
    'tests/playwright/tests/order.spec.js',
    'tests/playwright/tests/payment.spec.js',
]

FILE_POOL = [
    'src/services/inventory.js',
    'src/services/order.js',
    'src/services/payment.js',
    'src/shared/utils.js',
    'src/shared/validators.js',
    'src/api/routes.js',
]

RULES = {
    'src/services/inventory.js': {
        'tests/playwright/tests/inventory.spec.js': 0.95,
        'tests/playwright/tests/order.spec.js': 0.40,
    },
    'src/services/order.js': {
        'tests/playwright/tests/order.spec.js': 0.93,
        'tests/playwright/tests/inventory.spec.js': 0.30,
    },
    'src/services/payment.js': {
        'tests/playwright/tests/payment.spec.js': 0.95,
        'tests/playwright/tests/order.spec.js': 0.25,
    },
    'src/shared/utils.js': {
        'tests/playwright/tests/inventory.spec.js': 0.35,
        'tests/playwright/tests/order.spec.js': 0.35,
        'tests/playwright/tests/payment.spec.js': 0.35,
    },
    'src/shared/validators.js': {
        'tests/playwright/tests/order.spec.js': 0.45,
        'tests/playwright/tests/payment.spec.js': 0.45,
    },
    'src/api/routes.js': {
        'tests/playwright/tests/inventory.spec.js': 0.25,
        'tests/playwright/tests/order.spec.js': 0.40,
        'tests/playwright/tests/payment.spec.js': 0.40,
    },
}


def main() -> None:
    random.seed(42)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for idx in range(450):
        touched_count = random.randint(1, 3)
        changed_files = random.sample(FILE_POOL, k=touched_count)

        impacted = set()
        for changed in changed_files:
            test_probs = RULES.get(changed, {})
            for test_file, prob in test_probs.items():
                if random.random() < prob:
                    impacted.add(test_file)

        if not impacted:
            # Ensure at least one impacted test to keep labels meaningful.
            impacted.add(random.choice(TESTS))

        rows.append(
            {
                'commit_id': f'commit_{idx:04d}',
                'changed_files': ';'.join(changed_files),
                'impacted_tests': ';'.join(sorted(impacted)),
            }
        )

    with OUTPUT.open('w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['commit_id', 'changed_files', 'impacted_tests'])
        writer.writeheader()
        writer.writerows(rows)

    print(f'Wrote {len(rows)} rows to {OUTPUT}')


if __name__ == '__main__':
    main()
