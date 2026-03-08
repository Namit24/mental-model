from pathlib import Path
from datasets import load_dataset
import json
import csv

DATASET_NAME = "Amod/mental_health_counseling_conversations"
OUT_DIR = Path("data/mental_health_counseling_conversations")

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading dataset: {DATASET_NAME}")
    ds = load_dataset(DATASET_NAME)

    print(ds)
    hf_dir = OUT_DIR / "hf_dataset"
    ds.save_to_disk(str(hf_dir))
    print(f"Saved Hugging Face dataset to: {hf_dir}")

    train_ds = ds["train"]

    jsonl_path = OUT_DIR / "mental_health.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for row in train_ds:
            obj = {
                "context": row["Context"].strip() if row["Context"] else "",
                "response": row["Response"].strip() if row["Response"] else "",
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"Saved JSONL to: {jsonl_path}")

    csv_path = OUT_DIR / "mental_health.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["context", "response"])
        writer.writeheader()
        for row in train_ds:
            writer.writerow({
                "context": row["Context"].strip() if row["Context"] else "",
                "response": row["Response"].strip() if row["Response"] else "",
            })
    print(f"Saved CSV to: {csv_path}")
    print(f"Total rows: {len(train_ds)}")
    print("Done.")
if __name__ == "__main__":
    main()