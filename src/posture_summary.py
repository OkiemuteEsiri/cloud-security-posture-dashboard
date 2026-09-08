"""Summarize synthetic cloud security findings."""

import csv
from collections import Counter
from pathlib import Path


def summarize(path: str) -> dict[str, Counter]:
    severity = Counter()
    status = Counter()
    control = Counter()

    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            severity[row["severity"]] += 1
            status[row["status"]] += 1
            control[row["control_area"]] += 1

    return {"severity": severity, "status": status, "control_area": control}


if __name__ == "__main__":
    result = summarize("data/sample_findings.csv")
    for section, counts in result.items():
        print(section)
        for name, count in counts.most_common():
            print(f"  {name}: {count}")
