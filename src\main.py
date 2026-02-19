import argparse
import os
import sys

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'

def load_env(filepath):
    env = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Trim inline comments
                line = line.split('#', 1)[0].strip()
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                if not key:
                    continue
                value = value.strip()
                # Remove surrounding quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                env[key] = value
        return env
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

def get_env_diff(left, right):
    left_keys = set(left)
    right_keys = set(right)
    removed = sorted(left_keys - right_keys)
    added = sorted(right_keys - left_keys)
    changed = sorted(k for k in (left_keys & right_keys) if left[k] != right[k])
    return removed, added, changed

def print_diff(left_name, right_name, left_env, right_env):
    removed, added, changed = get_env_diff(left_env, right_env)
    print(f"Diff: {left_name} -> {right_name}")
    has_diff = False
    if removed:
        print(BLUE + "REMOVED:" + ENDC)
        for k in removed:
            print(f"  {RED}-{k}={left_env[k]}{ENDC}")
        has_diff = True
    if changed:
        print(BLUE + "CHANGED:" + ENDC)
        for k in changed:
            print(f"  {YELLOW}{k}={left_env[k]}{ENDC} -> {GREEN}{right_env[k]}{ENDC}")
        has_diff = True
    if added:
        print(BLUE + "ADDED:" + ENDC)
        for k in added:
            print(f"  {GREEN}+{k}={right_env[k]}{ENDC}")
        has_diff = True
    if not has_diff:
        print("No differences.")
    return has_diff

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to compare two .env files or current environment, showing added, removed, and changed variables with colorized output."
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('--current', '-c', action='store_true', help="Compare current environment (left) to the given file (right)")
    parser.add_argument('files', nargs='*', help="One or two .env files")
    args = parser.parse_args()
    if args.current:
        if len(args.files) != 1:
            parser.error("--current requires exactly one file")
        left_env = {k: v.strip() for k, v in os.environ.items()}
        left_name = "CURRENT"
        right_name = args.files[0]
        right_env = load_env(right_name)
    else:
        if len(args.files) != 2:
            parser.error("Without --current, provide exactly two files")
        left_name = args.files[0]
        right_name = args.files[1]
        left_env = load_env(left_name)
        right_env = load_env(right_name)
    if print_diff(left_name, right_name, left_env, right_env):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
