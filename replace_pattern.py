import os
import re
import fnmatch
import argparse
from datetime import datetime

# === COLOR UTILITIES ===
class Color:
    GREEN = '\033[92m'
    GRAY = '\033[90m'
    RESET = '\033[0m'

def print_color(text, color):
    print(f"{color}{text}{Color.RESET}")

# === ARGUMENT PARSING ===
parser = argparse.ArgumentParser(description='Generic recursive regex replacer for ASCII text files.')
parser.add_argument('--root', required=True, help='Root directory to scan')
parser.add_argument('--pattern', required=True, help='Regex pattern to search (with optional capture groups)')
parser.add_argument('--replace', required=True, help='Replacement string (supports \1, \2, etc.)')
parser.add_argument('--dry-run', action='store_true', help='Simulate only, do not modify files')
parser.add_argument('--log', default='replacement_log.txt', help='Log file path')
parser.add_argument('--files', nargs='*', help='Include only files matching these patterns (e.g. *.xml *.txt)')
parser.add_argument('--files-exclude', nargs='*', help='Exclude files matching these patterns (e.g. *.bak *.tmp)')
parser.add_argument('--summary-only', action='store_true', help='Suppress file-level replacement output')
args = parser.parse_args()

# === CONFIG ===
root_dir = args.root
regex_pattern = args.pattern
replacement_template = args.replace
dry_run = args.dry_run
log_file_path = args.log
include_patterns = args.files or ['*']
exclude_patterns = args.files_exclude or []
summary_only = args.summary_only

# === COMPILE PATTERN ===
try:
    pattern = re.compile(regex_pattern)
except re.error as e:
    print(f"Invalid regex pattern: {e}")
    exit(1)

# === COUNTERS & LOG ===
file_change_count = 0
total_replacements = 0
log_lines = []

def log_entry(file_path, old_value, new_value):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] File: {file_path}\n    Replaced: {old_value} -> {new_value}\n"
    log_lines.append(entry)

# === FILE FILTER ===
def file_is_included(filename):
    included = any(fnmatch.fnmatch(filename, pat) for pat in include_patterns)
    excluded = any(fnmatch.fnmatch(filename, pat) for pat in exclude_patterns)
    return included and not excluded

# === PROCESS FILE ===
def replace_in_file(file_path):
    global file_change_count, total_replacements

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()

    matches = list(pattern.finditer(content))
    if not matches:
        if not summary_only:
            print_color(f"[Skipped] {file_path}", Color.GRAY)
        return

    file_change_count += 1
    total_replacements += len(matches)

    preview_changes = [(m.group(0), pattern.sub(replacement_template, m.group(0))) for m in matches]
    new_content = pattern.sub(replacement_template, content)

    if dry_run:
        if not summary_only:
            print_color(f"[Dry Run] Would modify: {file_path}", Color.GREEN)
            for old, new in preview_changes:
                print(f"  Replace: {old} → {new}")
        for old, new in preview_changes:
            log_entry(file_path, old, new)
    else:
        with open(file_path, 'w', encoding='latin-1') as f:
            f.write(new_content)
        if not summary_only:
            print_color(f"[Modified] {file_path}", Color.GREEN)
        for old, new in preview_changes:
            log_entry(file_path, old, new)

# === WALK FILES ===
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if file_is_included(filename):
            full_path = os.path.join(dirpath, filename)
            replace_in_file(full_path)

# === SUMMARY ===
summary = (
    "\n=== SUMMARY ===\n"
    f"Files modified:    {file_change_count}\n"
    f"Replacements made: {total_replacements}\n"
    f"Log saved to:      {log_file_path}\n"
)
print(summary)
log_lines.append(summary)

# === WRITE LOG FILE ===
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    log_file.writelines(log_lines)
