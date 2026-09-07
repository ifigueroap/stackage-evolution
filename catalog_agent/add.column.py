import json

input_path = "results_writer_reviewed_3.jsonl"
output_path = "results_writer_reviewed_4.jsonl"

with open(input_path, "r") as infile, open(output_path, "w") as outfile:
    for line in infile:
        if not line.strip():
            continue

        record = json.loads(line)

        categories = record["categories"]

        # Rebuild the dict so the new field appears in the desired position
        new_categories = {}

        for key, value in categories.items():
            new_categories[key] = value

            if key == "polymorphic_use":
                new_categories["constraint_only"] = False

        record["categories"] = new_categories

        outfile.write(json.dumps(record) + "\n")