from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests
from datetime import datetime

app = FastAPI()

# Hugging Face Router + DeepSeek config
API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
HEADERS = {
    "Authorization": "Bearer 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"
}
MODEL_NAME = "deepseek/deepseek-v3-0324"

# Transaction schema
class Transaction(BaseModel):
    consumer_id: str
    amount: float
    location: str
    hour: int
    device_id: str
    known_locations: list[str]
    known_devices: list[str]
    average_transaction_amount: float
    recent_flags: list[str] = []

@app.post("/analyze")
def analyze(txn: Transaction):
    try:
        # --- Step 1: Format prompt for LLM ---
        prompt = f"""
You are an expert fraud analyst with knowledge of scam patterns and online transaction anomalies.

Analyze the following transaction for fraud:

{json.dumps(txn.dict(), indent=2)}

Evaluate the following:
- Is the amount much higher than the user's average?
- Is the location previously unseen?
- Is the device ID not among known devices?
- Is the hour of transaction unusual (like late night)?
- Are there recent flags?
- Should this raise a fraud suspicion?

Return a structured analysis:
1. Risk Score (0-100)
2. Verdict [Likely Fraud / Unusual but Safe / Safe]
3. Explanation
4. Suggested Action
"""

        # --- Step 2: Query DeepSeek via Hugging Face Router ---
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        # --- Step 3: Save transaction to fraud_history.jsonl ---
        txn_record = txn.dict()
        txn_record["analyzed_at"] = datetime.utcnow().isoformat()
        with open("fraud_history.jsonl", "a") as f:
            f.write(json.dumps(txn_record) + "\n")

        return {
            "analysis": answer
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
