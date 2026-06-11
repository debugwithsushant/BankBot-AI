# 3-Layer Response System:
#   Layer 1: FAQ exact/fuzzy match
#   Layer 2: Domain filter check
#   Layer 3: Groq AI response

import difflib
import streamlit as st
from groq import Groq

from faqs import faqs
from faq_aliases import FAQ_ALIASES
from domain_filter import is_banking_query

# Groq Client Setup 
# Local: .streamlit/secrets.toml
# Cloud: Streamlit Cloud secrets settings

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# AI System Prompt 

SYSTEM_PROMPT = """You are BankBot, a professional and helpful banking assistant for Indian customers.

Your rules:
1. Answer ONLY banking-related questions
2. Keep answers clear, concise, and helpful (3-5 sentences max)
3. Use simple English that anyone can understand
4. Include specific numbers/percentages when relevant (e.g., interest rates)
5. If the question is NOT banking-related, politely decline
6. Always be professional and trustworthy

You specialize in:
- Bank accounts (savings, current, zero balance)
- ATM usage and card management
- Loans (home, personal, car, education)
- Net banking, UPI, NEFT, RTGS, IMPS
- Fixed deposits and recurring deposits
- KYC, OTP, and banking security
- Indian banking regulations (RBI guidelines)
"""


# Common phrases used by multiple functions
# "what is", "how to" etc. — these inflate similarity scores
# during fuzzy matching, so we strip them before comparing.

COMMON_STARTS = [
    "what is ", "what are ", "what was ",
    "how to ", "how do ", "how does ", "how can ",
    "tell me about ", "explain ", "define ",
    "i want to know about ", "what do you mean by "
]


def strip_start(text):
    """
        Remove common starting phrases from the text to get the core topic.
        Example: "what is bitcoin" → "bitcoin"
             "how does loan work" → "loan work"
    """
    for phrase in COMMON_STARTS:
        if text.startswith(phrase):
            return text[len(phrase):]
    return text


# Layer 1: FAQ Matcher

def normalize(text):
    """
    Normalize query — lowercase, strip spaces, punctuation remove.
    Example: "What is ATM??" → "what is atm"
    """
    text = text.lower().strip()
    for char in ["?", "!", ".", ",", "'"]:
        text = text.replace(char, "")
    text = " ".join(text.split())
    return text


def check_alias(query):
    """
    Check if query matches any FAQ aliases — either exact or partial (for multi-word aliases).

    Single word aliases (e.g. "loan", "upi") → EXACT match only.
    Multi-word aliases (e.g. "home loan", "savings account") → partial match allowed.

        Returns: corresponding FAQ key string if match found, None otherwise.
        Example: "savings account" query matches "a savings account" alias → returns "a savings account"
    """
    query = normalize(query)

    # Exact alias match
    if query in FAQ_ALIASES:
        return FAQ_ALIASES[query]

    # Partial match for multi-word aliases
    for alias, faq_key in FAQ_ALIASES.items():
        if len(alias.split()) >= 2 and alias in query:
            return faq_key

    return None


def check_faq_direct(query):
    """
    Check if query directly matches any FAQ key — either exact or partial (query in faq_key or faq_key in query).
    Returns: answer string if match found, None otherwise.
    """
    query = normalize(query)

    # Exact match
    if query in faqs:
        return faqs[query]

    # Partial match (query in faq_key or faq_key in query)
    for faq_key, answer in faqs.items():
        if query in faq_key or faq_key in query:
            return answer

    return None


def check_faq_fuzzy(query):
    """
    Fuzzy matching — Handle spelling mistakes

    Key fix: Remove common starting words like, "what is", "how to"

        Returns: answer string if close match found, None otherwise.
    """
    query = normalize(query)

    # Remove common starting phrases to get the core topic for better fuzzy matching
    query_core = strip_start(query)
    faq_keys = list(faqs.keys())
    faq_keys_core = [strip_start(k) for k in faq_keys]

    # Find close matches based on the core topics
    matches = difflib.get_close_matches(query_core, faq_keys_core, n=1, cutoff=0.65)

    if matches:
        # Get the original FAQ key corresponding to the matched core topic
        matched_core = matches[0]
        original_index = faq_keys_core.index(matched_core)
        original_key = faq_keys[original_index]
        return faqs[original_key]

    return None


def check_faq_keywords(query):
    """
    Keyword overlap — Handle rephrased queries by checking common words with FAQ keys.
    """
    query = normalize(query)
    query_words = set(query.split())

    # Ignore common stop words that don't add meaning to the query
    stop_words = {"what", "is", "are", "how", "to", "a", "an",
                   "the", "i", "my", "can", "do", "does", "tell",
                   "me", "about", "explain", "difference", "between",
                   "work", "works", "get", "give", "of", "for", "on"}

    query_words = query_words - stop_words

    # If no meaningful words left after removing stop words, return None
    if not query_words:
        return None

    best_answer = None
    best_score = 2  # Require at least 3 common words to consider it a good match

    for faq_key, answer in faqs.items():
        faq_words = set(faq_key.split()) - stop_words
        common = query_words.intersection(faq_words)

        if len(common) > best_score:
            best_score = len(common)
            best_answer = answer

    return best_answer


def get_faq_response(user_query):
    """
    Layer 1: FAQ Matcher — Try multiple strategies to find an instant answer from the FAQ database.
    """

    # Layer 1a: Alias check
    alias_key = check_alias(user_query)
    if alias_key:
        normalized_key = normalize(alias_key)
        if normalized_key in faqs:
            return faqs[normalized_key]

    # Layer 1b: Direct FAQ match
    answer = check_faq_direct(user_query)
    if answer:
        return answer

    # Layer 1c: Fuzzy match (spelling mistakes handle)
    answer = check_faq_fuzzy(user_query)
    if answer:
        return answer

    # Layer 1d: Keyword overlap
    answer = check_faq_keywords(user_query)
    if answer:
        return answer

    # No FAQ match found
    return None


# Layer 2 & 3: Domain Check + Groq AI

def get_ai_response(user_query):
    """
    Generate response from Groq AI based on the user query and system prompt.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        max_tokens=300,
        temperature=0.5,
    )
    return response.choices[0].message.content


# Main Response Router

def get_response(user_query):
    """
    Main function to get response for a user query by going through the 3 layers:
        1. FAQ Matcher
        2. Domain Filter
        3. Groq AI Response
    """

    if not user_query or not user_query.strip():
        return "Please enter a question.", "error"

    # Step 1: FAQ Check
    faq_answer = get_faq_response(user_query)

    if faq_answer:
        return faq_answer, "faq"

    # Step 2: Domain Filter
    if not is_banking_query(user_query):
        return (
            "⚠️ I can only answer banking-related questions. "
            "Please ask me about accounts, ATM, loans, cards, "
            "net banking, UPI, or other banking topics.",
            "off_topic"
        )

    # Step 3: Groq AI Response
    try:
        ai_answer = get_ai_response(user_query)
        return ai_answer, "ai"

    except Exception:
        return (
            "⚠️ AI service is temporarily unavailable. "
            "Please try again in a moment. "
            "For urgent help, call your bank's customer care.",
            "error"
        )