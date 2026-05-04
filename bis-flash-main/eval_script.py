"""
eval_script.py — Evaluate RAG Pipeline accuracy and latency.
"""

import json
import argparse
import sys
import re

def normalize_std(std_string: str) -> str:
    """Normalize standard ID for fair matching."""
    s = re.sub(r'[^a-z0-9]', '', str(std_string).lower())
    # Order matters: replace longer Roman numerals first
    s = s.replace('partiv', 'part4')
    s = s.replace('partiii', 'part3')
    s = s.replace('partii', 'part2')
    s = s.replace('parti', 'part1')
    return s

def evaluate_results(results_file: str):
    try:
        with open(results_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading results file: {e}")
        sys.exit(1)

    total_queries = len(data)
    if total_queries == 0:
        print("No queries found.")
        return

    hits_at_3 = 0
    mrr_sum_at_5 = 0.0
    total_latency = 0.0
    processed_count = 0

    for item in data:
        expected_raw = item.get("expected_standards")
        if expected_raw is None:
            continue # Skip items without expected ground truth for evaluation
            
        processed_count += 1
        expected = {normalize_std(std) for std in expected_raw}
        retrieved = [normalize_std(std) for std in item.get("retrieved_standards", [])]
        latency = item.get("latency_seconds", 0.0)

        total_latency += latency

        # Hit Rate @3
        if any(std in expected for std in retrieved[:3]):
            hits_at_3 += 1

        # MRR @5
        mrr = 0.0
        for rank, std in enumerate(retrieved[:5], start=1):
            if std in expected:
                mrr = 1.0 / rank
                break
        mrr_sum_at_5 += mrr

    if processed_count == 0:
        print("Warning: No queries with 'expected_standards' found for evaluation.")
        return

    hit_rate_3 = (hits_at_3 / processed_count) * 100
    mrr_5 = mrr_sum_at_5 / processed_count
    avg_latency = total_latency / total_queries

    print("\n" + "=" * 50)
    print("   BIS HACKATHON EVALUATION RESULTS")
    print("=" * 50)
    print(f"Queries Evaluated : {processed_count}")
    print(f"Hit Rate @3       : {hit_rate_3:.2f}%")
    print(f"MRR @5            : {mrr_5:.4f}")
    print(f"Avg Latency       : {avg_latency:.2f}s")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate RAG Pipeline Results")
    parser.add_argument("--results", type=str, required=True, help="Path to output JSON file")
    args = parser.parse_args()
    evaluate_results(args.results)
