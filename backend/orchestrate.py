import os
import openai
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = openai.OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

SPECIALIST_ROUTES = {
        "full_report": ["categorization", "search", "anomaly", "analytics"],
        "analytics": ["analytics"],
        "projection": ["projection"],
        "anomaly": ["anomaly", "analytics"],
        "search": ["search"],
        "categorization": ["categorization"]
    }

VALID_INTENTS = {
        "full_report", "analytics", "projection", 
        "anomaly", "search", "categorization"
    }

def route(intent: str) -> list[str]:
        return SPECIALIST_ROUTES.get(intent, ["full_report"])

def classify_and_route(user_message: str) -> list[str]:
    
    prompt = """You are an intent classifier for a personal finance agent.

    Given a user message, classify it into exactly one of these intents:
    - full_report
    - analytics
    - projection
    - anomaly
    - search
    - categorization

    Rules:
- full_report: user wants everything at once. Keywords: "overview", "full breakdown", 
  "show me everything", "summary of all my finances".

- analytics: user wants a specific number or comparison. They reference a time period 
  and a category. Keywords: "how much", "how often", "total", "average", "compare".
  Examples: "how much did I spend on food in March", "compare last 2 months"

- projection: user asks about the future. They mention a savings goal, a target date, 
  or use future tense. Keywords: "will I", "can I", "by [month/year]", "how long until".
  Examples: "will I save £5000 by December", "how long until I can afford a car"

- anomaly: user is confused or concerned about their spending and wants the agent 
  to investigate. They do NOT know what they're looking for. Keywords: "where did my 
  money go", "why is my balance low", "am I overspending", "what am I wasting money on".

- search: user wants to find specific transactions by naming a merchant, app, or 
  service. They know what they're looking for. Keywords: merchant names like "Uber", 
  "Netflix", "Starbucks", or "transactions over £X".
  Examples: "show me all Uber charges", "find transactions over £100 in April"

- categorization: user wants transactions labeled or questions an existing label.
  Keywords: "categorize", "label", "why is this labeled", "organize my transactions".

    Respond with ONLY the intent word, nothing else."""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=10,
        messages=[
            {
                "role": "system",
                "content":prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    text = response.choices[0].message.content
    intent = text.strip().lower()
    if intent not in VALID_INTENTS:
        intent = "full_report" 
    return route(intent=intent)

if __name__ == "__main__":
    tests = [
        "show me everything",
        "how much did I spend on food in March",
        "will I save £5000 by December",
        "where did all my money go",
        "show me all Uber transactions",
        "categorize my transactions"
    ]
    for msg in tests:
        print(f"{msg} → {classify_and_route(msg)}")