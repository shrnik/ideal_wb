# parse batch output and save to csv
from operator import index
import pandas as pd
import os
import json
import argparse
import re


def extract_json_string(content):
    """
    Extract a JSON string from content that may be wrapped in Markdown code blocks or be raw JSON.
    Handles:
    - ```json\n{...}\n```
    - ```\n{...}\n```
    - Raw {...}
    """
    # Try extracting from Markdown-style code block first
    match = re.search(r"```(?:json)?\s*({.*?})\s*```", content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Try extracting from first {...} block even if not Markdown-wrapped
    match = re.search(r"({.*})", content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return None  # Nothing that looks like JSON found


def parse_batch_output(batch_output_file, output_csv_file):
    """
    Parse the batch output JSONL file and save the results to a CSV file.

    Args:
        batch_output_file (str): The path to the batch output JSONL file.
        output_csv_file (str): The path to save the parsed CSV file.
    """
    if not os.path.exists(batch_output_file):
        raise FileNotFoundError(
            f"The file {batch_output_file} does not exist.")

    results = []
    with open(batch_output_file, 'r') as f:
        for line in f:
            result = json.loads(line)
            output = extract_json_string(
                result["response"]["body"]["choices"][0]["message"]["content"])
            # parse json
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {output}")
            custom_id = result["custom_id"]
            index = custom_id.split("-")[1]
            # add to results
            results.append({
                "index": index,
                "output": output
            })

    results = sorted(results, key=lambda x: int(x["index"]))
    outputs = [result["output"] for result in results]
    df = pd.DataFrame(outputs)
    df.to_csv(output_csv_file, index=False)
    print(f"Parsed results saved to {output_csv_file}")


if __name__ == "__main__":

    parse_batch_output("data/batch_68379a60a40c81908feb536ea9694f28_output.jsonl",
                       output_csv_file="data/interventions2k.csv")
