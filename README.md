# replace-pattern

A flexible command-line tool to recursively replace regex patterns in ASCII text files. Supports dry-run, file filtering, logging, and colorized output.

## 📦 Features
- Regex-based replacements with backreferences
- Recursive search in any directory
- File include/exclude patterns (`--files`, `--files-exclude`)
- Dry-run support with clear output
- Log all replacements and summary stats

## 🔧 Usage

```bash
python replace_pattern.py \
  --root ./data \
  --pattern 'FINEME\.([A-Z0-9]+)' \
  --replace 'REPLACED.\1' \
  --files *.xml \
  --files-exclude *.bak \
  --dry-run \
  --summary-only
```

## 📝 Example
Replaces all `FINEME.XXX` with `REPLACED.XXX` in `.xml` files.

## 💡 Tips
- Use `--dry-run` first to preview changes
- Combine with `--summary-only` for quiet mode
- Use glob patterns to filter files

## 🗂️ Directory Layout

```
replace-pattern/
├── replace_pattern.py   # Main script
├── README.md            # This file
├── .gitignore           # Ignore logs and temporary files
└── LICENSE              # Optional license
```
