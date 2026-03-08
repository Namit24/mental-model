import json
from pathlib import Path

INPUT_FILE = Path("/home/namit/mental-model/data/mental_health.jsonl")
OUTPUT_FILE = Path("/home/namit/mental-model/data/mental_health_cleaned.jsonl")

HIGH_RISK_TERMS = [
    "suicide",
    "kill myself",
    "want to die",
    "end my life",
    "hurt myself",
    "self-harm",
    "shouldn't be here",
    "no reason to live",
]

def contains_high_risk(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in HIGH_RISK_TERMS)

def clean_text(text: str) -> str:
    return " ".join(text.strip().split())

def safe_high_risk_response(original_response: str) -> str:
    return (
        "I'm really sorry you're going through this. You deserve support, and you do not have to handle it alone. "
        "If you feel like you might act on these thoughts or you are in immediate danger, please contact local emergency services "
        "or a crisis line right now, and reach out to someone you trust to stay with you. "
        "If you are not in immediate danger, speaking with a licensed mental health professional could help you work through this with support."
    )

def should_drop(context: str, response: str) -> bool:
    if not context or not response:
        return True
    if len(context.split()) < 5 or len(response.split()) < 5:
        return True
    return False

def main():
    kept = 0
    rewritten = 0
    dropped = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
        for line in fin:
            row = json.loads(line)

            context = clean_text(str(row.get("context", "")))
            response = clean_text(str(row.get("response", "")))

            if should_drop(context, response):
                dropped += 1
                continue

            if contains_high_risk(context):
                response = safe_high_risk_response(response)
                rewritten += 1

            cleaned = {
                "context": context,
                "response": response,
            }
            fout.write(json.dumps(cleaned, ensure_ascii=False) + "\n")
            kept += 1

    print(f"Saved cleaned dataset to: {OUTPUT_FILE}")
    print(f"Kept: {kept}")
    print(f"Rewritten high-risk rows: {rewritten}")
    print(f"Dropped: {dropped}")

if __name__ == "__main__":
    main()