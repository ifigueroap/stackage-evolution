import json

REFERENCE_FILE = "lts-24-37-reader_training.jsonl"
CODEX_FILE = "reader_testing.jsonl"


def load_jsonl(path):
    records = {}
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                records[record["index"]] = record
    return records

def compare_dict(reference, codex, section):
    """
    Compare one nested section, e.g.:
        api_usage
        categories

    Returns a list of mismatches:
        (field, expected, actual)
    """
    mismatches = []

    ref_fields = reference.get(section, {})
    codex_fields = codex.get(section, {})

    for field, expected in ref_fields.items():
        actual = codex_fields.get(field)

        if actual != expected:
            mismatches.append((field, expected, actual))

    return mismatches


def main():
    reference_records = load_jsonl(REFERENCE_FILE)
    codex_records = load_jsonl(CODEX_FILE)

    total = 0
    correct = 0

    for index, reference in reference_records.items():

        # Codex has not categorized this file
        if index not in codex_records:
            continue

        total += 1
        codex = codex_records[index]

        api_errors = compare_dict(
            reference,
            codex,
            "api_usage"
        )

        category_errors = compare_dict(
            reference,
            codex,
            "categories"
        )

        if not api_errors and not category_errors:
            correct += 1
            print(
                f"[OK] {index}: {reference['module']}"
            )
            continue

        print(
            f"\n[MISMATCH] {index}: {reference['module']}"
        )

        if api_errors:
            print("  API usage:")
            for field, expected, actual in api_errors:
                print(
                    f"    {field}: "
                    f"expected={expected}, codex={actual}"
                )

        if category_errors:
            print("  Categories:")
            for field, expected, actual in category_errors:
                print(
                    f"    {field}: "
                    f"expected={expected}, codex={actual}"
                )

    print("\n-----------------------------")
    print("SUMMARY")
    print("-----------------------------")
    print(f"Files compared: {total}")
    print(f"Exact matches:  {correct}")
    print(f"With errors:    {total - correct}")

    if total:
        print(
            f"Exact accuracy: {correct / total:.2%}"
        )


if __name__ == "__main__":
    main()