import streamlit as st
from faqs import faqs
from faq_aliases import FAQ_ALIASES
from domain_filter import is_banking_query

st.title("Milestone 2 Test")

# FAQ count
st.success(f"✅ FAQs loaded: {len(faqs)}")
st.success(f"✅ Aliases loaded: {len(FAQ_ALIASES)}")

# Domain filter test
test_queries = ["What is ATM?", "Tell me about cricket", "How to open account?", "Who is Modi?"]
for q in test_queries:
    result = "✅ Banking" if is_banking_query(q) else "❌ Not Banking"
    st.write(f"{result} — *{q}*")