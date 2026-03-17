import sys
import os
import argparse

LETTERS = "abcdefghijklmnopqrstuvwxyz"

def count_from_dic(path):
    counts = {c: 0 for c in LETTERS}
    with open(path, encoding="utf-8", errors="ignore") as f:
        next(f)
        for line in f:
            word = line.split("/")[0].strip()
            if word and len(word) > 1 and word[0] in counts and '-' not in word:
                counts[word[0]] += 1
    return counts

def write_csv(f, locales, all_counts, normalize=False):
    f.write("letter," + ",".join(locales) + "\n")
    if normalize:
        totals = [sum(c.values()) for c in all_counts]
        for ch in LETTERS:
            row = [ch.upper()] + [f"{c[ch] / t * 100:.2f}" for c, t in zip(all_counts, totals)]
            f.write(",".join(row) + "\n")
    else:
        for ch in LETTERS:
            row = [ch.upper()] + [str(c[ch]) for c in all_counts]
            f.write(",".join(row) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("locales", help="Comma-separated locale codes, e.g. en_GB,fr,pt_BR")
    parser.add_argument("--output-dir", default="/output")
    args = parser.parse_args()

    locales = args.locales.split(",")
    all_counts = []
    for locale in locales:
        path = f"/usr/share/hunspell/{locale}.dic"
        if not os.path.exists(path) and '_' not in locale:
            path = f"/usr/share/hunspell/{locale}_{locale.upper()}.dic"
        if not os.path.exists(path):
            print(f"Error: dictionary not found: {path}", file=sys.stderr)
            sys.exit(1)
        all_counts.append(count_from_dic(path))

    slug = "-".join(locales)
    raw_path = os.path.join(args.output_dir, f"output_{slug}.csv")
    pct_path = os.path.join(args.output_dir, f"output_{slug}_percent.csv")

    with open(raw_path, "w") as f:
        write_csv(f, locales, all_counts)
    with open(pct_path, "w") as f:
        write_csv(f, locales, all_counts, normalize=True)

main()
