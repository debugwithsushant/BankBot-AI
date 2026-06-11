import streamlit as st
from datetime import datetime
from chatbot import get_response

# Page Configuration

st.set_page_config(
    page_title="BankBot AI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS — Dark Banking Theme

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0e17;
    }

    /* Hide Streamlit default header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Title styling */
    h1 {
        text-align: center;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Caption / subtitle */
    .stCaption, [data-testid="stCaptionContainer"] {
        text-align: center;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f1420;
        border-right: 1px solid #1f2937;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] button {
        width: 100%;
        text-align: left;
        border-radius: 8px;
    }

    /* Chat message bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 4px;
    }

    /* Quick category buttons row */
    div[data-testid="column"] button {
        border-radius: 100px;
        font-size: 0.8rem;
        border: 1px solid #1f2937;
        background-color: #1a2030;
        color: #9fe1cb;
    }

    div[data-testid="column"] button:hover {
        border-color: #1d9e75;
        color: #5DCAA5;
    }

    /* Chat input box */
    [data-testid="stChatInput"] {
        border-radius: 12px;
    }

    /* Response type badge */
    .badge-faq {
        background-color: #26215c;
        color: #cecbf6;
        font-size: 0.7rem;
        padding: 2px 10px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 6px;
    }
    .badge-ai {
        background-color: #085041;
        color: #9fe1cb;
        font-size: 0.7rem;
        padding: 2px 10px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 6px;
    }
    .badge-error {
        background-color: #791f1f;
        color: #f7c1c1;
        font-size: 0.7rem;
        padding: 2px 10px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)


# Session State Initialization

if "conversations" not in st.session_state:
    st.session_state.conversations = {
        "Chat 1": {"title": "New Chat", "messages": []}
    }
    st.session_state.current_chat = "Chat 1"
    st.session_state.chat_count = 1


# Helper: Build Export Text

def build_export_text(messages):
    """
    Convert chat messages into a readable text format for export.
    """
    lines = []
    lines.append("BankBot AI - Chat Export")
    lines.append(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 50)
    lines.append("")

    for msg in messages:
        role = "You" if msg["role"] == "user" else "BankBot"
        lines.append(f"{role}: {msg['content']}")
        lines.append("")

    return "\n".join(lines)


# Sidebar

with st.sidebar:
    st.markdown("### 🏦 BankBot AI")
    st.caption("Your banking FAQ assistant")
    st.divider()

    # New Chat button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_count += 1
        chat_id = f"Chat {st.session_state.chat_count}"
        st.session_state.conversations[chat_id] = {
            "title": "New Chat",
            "messages": []
        }
        st.session_state.current_chat = chat_id
        st.rerun()

    st.markdown("**Chats**")

    # List all chats
    for chat_id, chat_data in st.session_state.conversations.items():
        is_active = (chat_id == st.session_state.current_chat)
        label = f"💬 {chat_data['title']}"
        if is_active:
            label = f"➤ {chat_data['title']}"

        if st.button(label, key=chat_id, use_container_width=True):
            st.session_state.current_chat = chat_id
            st.rerun()

    st.divider()

    # Export current chat
    current_chat = st.session_state.conversations[st.session_state.current_chat]
    if current_chat["messages"]:
        export_text = build_export_text(current_chat["messages"])
        st.download_button(
            label="⬇️ Export Chat",
            data=export_text,
            file_name=f"bankbot_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Clear all history
    if st.button("🧹 Clear All History", use_container_width=True):
        st.session_state.conversations = {
            "Chat 1": {"title": "New Chat", "messages": []}
        }
        st.session_state.current_chat = "Chat 1"
        st.session_state.chat_count = 1
        st.rerun()

    st.divider()
    st.caption("Built with Python, Streamlit & Groq AI")
    st.caption("by Sushant Pawar")


# Main Header

st.title("🏦 BankBot AI Chatbot")
st.caption("Ask me anything about banking — accounts, loans, cards, UPI & more")

st.divider()

# Quick Category Buttons

current_chat = st.session_state.conversations[st.session_state.current_chat]
current_messages = current_chat["messages"]

# In new chat only shows quick category buttons.
if not current_messages:
    st.markdown("**Quick topics:**")
    col1, col2, col3, col4 = st.columns(4)

    quick_questions = {
        col1: ("💳 Cards", "What is the difference between debit and credit card?"),
        col2: ("💰 Loans", "What is EMI and how is it calculated?"),
        col3: ("📱 UPI", "What is UPI and how does it work?"),
        col4: ("🔒 Security", "How can I keep my bank account safe?"),
    }

    quick_clicked = None
    for col, (label, question) in quick_questions.items():
        with col:
            if st.button(label, use_container_width=True):
                quick_clicked = question

    st.divider()
else:
    quick_clicked = None


# Display Conversation History

for message in current_messages:
    avatar = "🧑‍💼" if message["role"] == "user" else "🏦"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

        # Show response type badge
        if message["role"] == "assistant" and "type" in message:
            badge_class = {
                "faq": ("badge-faq", "📋 FAQ Answer"),
                "ai": ("badge-ai", "🤖 AI Generated"),
                "off_topic": ("badge-error", "⚠️ Off Topic"),
                "error": ("badge-error", "⚠️ Error")
            }
            css_class, label = badge_class.get(
                message["type"], ("badge-faq", "")
            )
            if label:
                st.markdown(
                    f'<span class="{css_class}">{label}</span>',
                    unsafe_allow_html=True
                )


# Chat Input

user_query = st.chat_input("Type your banking question...")

# If quick category button clicked, set user_query to that question instead of input box.
if quick_clicked:
    user_query = quick_clicked


# Process Query

if user_query:

    # Chat title set
    if current_chat["title"] == "New Chat":
        title = user_query.strip().capitalize()
        if len(title) > 30:
            title = title[:27] + "..."
        current_chat["title"] = title

    # User message add
    current_chat["messages"].append(
        {"role": "user", "content": user_query}
    )

    # Display user message immediately
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(user_query)

    # Bot response generate
    with st.chat_message("assistant", avatar="🏦"):
        with st.spinner("BankBot is thinking..."):
            bot_response, response_type = get_response(user_query)

        st.markdown(bot_response)

        # Show badge
        badge_class = {
            "faq": ("badge-faq", "📋 FAQ Answer"),
            "ai": ("badge-ai", "🤖 AI Generated"),
            "off_topic": ("badge-error", "⚠️ Off Topic"),
            "error": ("badge-error", "⚠️ Error")
        }
        css_class, label = badge_class.get(
            response_type, ("badge-faq", "")
        )
        if label:
            st.markdown(
                f'<span class="{css_class}">{label}</span>',
                unsafe_allow_html=True
            )

    # Save bot message in history
    current_chat["messages"].append(
        {"role": "assistant", "content": bot_response, "type": response_type}
    )

    st.rerun()