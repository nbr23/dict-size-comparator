# dict-size-comparator

Counts how many words in hunspell dictionaries start with each letter of the alphabet in multiple languages, and compiles the data into a csv.

## Usage

```sh
./run.sh en_GB,fr,pt_BR
```

The first argument is a comma-separated list of locale codes (e.g. `en_GB`, `fr`, `pt_BR`). These are mapped to hunspell dictionary packages automatically.

Two files are written to `output/`:
- `output_<locales>.csv` — raw counts
- `output_<locales>_percent.csv` — percentages (0–100)
