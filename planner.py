import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def understand_task(user_request):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "valid": False,
            "action": "unsupported",
            "vendor": "",
            "steps": [],
            "message": "GROQ_API_KEY is missing. Check your .env file."
        }

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI task planner for an invoice-processing assistant.

Supported capability:
- Find the latest invoice from a vendor.
- Extract invoice details.
- Record the invoice in a local ledger.
- Verify the ledger entry.

Return ONLY valid JSON in this format:

{
  "valid": true,
  "action": "process_invoice",
  "vendor": "ABC Company",
  "steps": [
    "Find the latest invoice",
    "Extract invoice details",
    "Record invoice in ledger",
    "Verify the ledger entry"
  ],
  "message": "Invoice processing task understood."
}

Rules:
- Understand different natural language phrasings.
- Extract the vendor name.
- If the vendor is unclear, set valid to false.
- If the request is unrelated to invoice processing, set valid to false.
- Never claim that a task has already been executed.
- Do not invent capabilities.
"""
                },
                {
                    "role": "user",
                    "content": user_request
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Handle possible Markdown code fences
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        plan = json.loads(content)

        # Validate the planner's response
        if (
            not isinstance(plan, dict)
            or plan.get("action") != "process_invoice"
            or not plan.get("vendor")
            or not isinstance(plan.get("steps"), list)
        ):
            return {
                "valid": False,
                "action": "unsupported",
                "vendor": "",
                "steps": [],
                "message": "Could not process your request"
            }

        plan["valid"] = True
        return plan

    except Exception as error:
        return {
            "valid": False,
            "action": "unsupported",
            "vendor": "",
            "steps": [],
            "message": f"Planner error: {error}"
        }