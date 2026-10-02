# Generative AI for Financial Services

A simple base project showing how LLMs can be used in banking and finance.

## Features
1. **Report Summarizer** – highlights, risks, outlook from earnings text
2. **News Sentiment** – positive/neutral/negative with reasons
3. **Document Q&A** – answers grounded only in the supplied document
4. **Fraud Explainer** – risk level + red flags for a transaction; synthetic data generator
5. **Finance Assistant** – customer-friendly financial-literacy chatbot

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env      # add your ANTHROPIC_API_KEY
streamlit run app.py
```

## Structure
```
app.py            Streamlit UI
finai/llm.py      Anthropic API wrapper (text + JSON)
finai/tasks.py    Prompts for each use case
```

## Next steps
- RAG over real filings (vector DB + embeddings)
- Authentication, audit logs, PII masking
- Evaluation sets and human review for high-risk outputs
- Compliance review before any customer-facing use
