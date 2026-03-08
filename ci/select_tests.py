import argparse
import json
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Select tests for CI from changed files')
    parser.add_argument('--changed-files', nargs='+', required=True)
    parser.add_argument('--threshold', type=float, default=0.35)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cmd = [
        'python3',
        'ml/predict_tests.py',
        '--threshold',
        str(args.threshold),
        '--changed-files',
        *args.changed_files,
    ]

    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    payload = json.loads(proc.stdout)
    selected = payload['selected_tests']

    print('Selected tests:')
    for test_file in selected:
        print(test_file)

    # CSV output form for CI env vars.
    print('\nSELECTED_TESTS=' + ','.join(selected))


if __name__ == '__main__':
    main()
