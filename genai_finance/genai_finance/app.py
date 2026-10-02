import pandas as pd
import streamlit as st

from finai import tasks

st.set_page_config(page_title="GenAI for Financial Services", page_icon="🏦", layout="wide")
st.title("🏦 Generative AI for Financial Services")
st.caption(tasks.DISCLAIMER)

SAMPLE_REPORT = """Q2 FY26: Revenue rose 12% YoY to INR 4,820 crore driven by retail lending.
Net interest margin held at 3.4%. Gross NPA improved to 1.9% from 2.3%.
Management flagged rising unsecured-loan delinquencies and a possible rate cut
as risks. Guidance: 10-12% loan growth for the full year."""

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📄 Report Summarizer", "📰 News Sentiment", "❓ Document Q&A",
     "🚨 Fraud Explainer", "💬 Finance Assistant"])


def run(fn, *args):
    try:
        with st.spinner("Thinking..."):
            return fn(*args)
    except Exception as e:
        st.error(f"Error: {e}")


with tab1:
    text = st.text_area("Paste a financial report / earnings text", SAMPLE_REPORT, height=200)
    if st.button("Summarize"):
        out = run(tasks.summarize_report, text)
        if out:
            st.markdown(out)

with tab2:
    raw = st.text_area("One headline per line", height=150, value=
        "Bank profits jump 15% on strong loan demand\n"
        "RBI keeps repo rate unchanged\n"
        "Fintech startup faces regulatory probe over KYC lapses")
    if st.button("Analyze sentiment"):
        data = run(tasks.analyze_sentiment, [l for l in raw.splitlines() if l.strip()])
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)

with tab3:
    doc = st.text_area("Document", SAMPLE_REPORT, height=150, key="doc")
    q = st.text_input("Ask a question", "What was the gross NPA?")
    if st.button("Get answer"):
        out = run(tasks.answer_from_document, doc, q)
        if out:
            st.info(out)

with tab4:
    c1, c2 = st.columns(2)
    amount = c1.number_input("Amount (INR)", value=95000.0)
    merchant = c1.text_input("Merchant", "Electronics Store")
    city = c2.text_input("City", "Lagos")
    hour = c2.slider("Hour of day", 0, 23, 3)
    home = st.text_input("Customer home city", "Hyderabad")
    avg = st.number_input("Customer average txn (INR)", value=1800.0)
    if st.button("Assess risk"):
        res = run(tasks.explain_transaction, dict(
            amount=amount, merchant=merchant, city=city, hour=hour,
            customer_home_city=home, customer_avg_txn=avg))
        if res:
            st.subheader(f"Risk: {res['risk_level'].upper()}")
            st.write("**Red flags:**")
            for f in res["red_flags"]:
                st.write(f"- {f}")
            st.write(f"**Recommended action:** {res['recommended_action']}")
    st.divider()
    n = st.number_input("Generate synthetic test transactions", 5, 30, 10)
    if st.button("Generate data"):
        data = run(tasks.generate_synthetic_transactions, int(n))
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)

with tab5:
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for m in st.session_state.chat:
        st.chat_message(m["role"]).write(m["content"])
    if msg := st.chat_input("Ask about budgeting, loans, SIPs, insurance..."):
        st.chat_message("user").write(msg)
        reply = run(tasks.advisor_chat, list(st.session_state.chat), msg)
        if reply:
            st.chat_message("assistant").write(reply)
            st.session_state.chat += [{"role": "user", "content": msg},
                                      {"role": "assistant", "content": reply}]
