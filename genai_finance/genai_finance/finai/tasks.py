"""Financial-services use cases built on top of the LLM wrapper."""
from .llm import ask, ask_json

DISCLAIMER = ("This is AI-generated information for educational purposes, "
              "not personalised financial advice.")


def summarize_report(text: str) -> str:
    system = ("You are a senior financial analyst. Summarize financial documents "
              "accurately. Never invent numbers that are not in the text.")
    prompt = ("Summarize the following document as:\n"
              "1) Key highlights (max 5 bullets)\n2) Risks\n3) Outlook\n\n"
              f"Document:\n{text}")
    return ask(system, prompt)


def analyze_sentiment(headlines: list[str]):
    system = "You are a market sentiment classifier."
    prompt = ('For each headline return a JSON list of objects with keys: '
              '"headline", "sentiment" (positive|neutral|negative), '
              '"confidence" (0-1), "reason" (one short sentence).\n\n'
              + "\n".join(f"- {h}" for h in headlines))
    return ask_json(system, prompt)


def answer_from_document(document: str, question: str) -> str:
    system = ("Answer ONLY using the provided document. If the answer is not in "
              "the document, say you cannot find it.")
    return ask(system, f"Document:\n{document}\n\nQuestion: {question}")


def explain_transaction(txn: dict) -> dict:
    system = ("You are a fraud-analysis assistant for a bank. Assess risk using "
              "only the given fields and explain clearly for a human reviewer.")
    prompt = ('Return JSON with keys "risk_level" (low|medium|high), '
              '"red_flags" (list of strings), "recommended_action" (string).\n\n'
              f"Transaction: {txn}")
    return ask_json(system, prompt)


def advisor_chat(history: list[dict], user_msg: str) -> str:
    system = ("You are a friendly financial-literacy assistant for retail bank "
              "customers. Explain concepts (budgeting, loans, SIPs, insurance) "
              "simply. Do not recommend specific securities. Always remind users "
              "to consult a licensed advisor for personal decisions.")
    return ask(system, user_msg, history=history)


def generate_synthetic_transactions(n: int = 10):
    system = "You generate realistic but entirely fictional banking data for testing."
    prompt = (f"Generate {n} fictional card transactions as a JSON list. Keys: "
              '"txn_id", "amount" (number, INR), "merchant", "category", '
              '"city", "hour" (0-23). Include 2 that look suspicious.')
    return ask_json(system, prompt, max_tokens=3000)
