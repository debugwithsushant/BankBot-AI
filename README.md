# 🏦 BankBot AI

An AI-powered banking chatbot built using **Python**, **Streamlit**, and **Groq LLMs**. BankBot AI acts as a virtual banking assistant capable of answering banking-related questions through a hybrid approach that combines a predefined FAQ knowledge base with AI-generated responses.

## 🚀 Features

* Banking-focused AI chatbot
* Predefined FAQ knowledge base
* FAQ alias mapping for better query matching
* Domain restriction to banking-related queries only
* Groq-powered LLM responses
* Streamlit web interface
* Fast and interactive user experience

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Groq API
* Natural Language Processing (NLP)

---

## 📂 Project Structure

```text
BankBot-AI/
│
├── app.py
├── chatbot.py
├── faqs.py
├── faq_aliases.py
├── domain_filter.py
├── requirements.txt
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/debugwithsushant/BankBot-AI.git
cd BankBot-AI
```

### 2. Create a virtual environment

```bash
py -3.13 -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Groq API Key

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open your browser and visit:

```text
http://localhost:8501
```

---

## 💬 Example Queries

* What is a savings account?
* What is a fixed deposit?
* How does a credit card work?
* What is the interest rate on loans?
* How can I open a bank account?

---

## 🛡️ Domain Restriction

BankBot AI is designed to answer **banking-related questions only**.

Examples:

✅ "What is a savings account?"

✅ "Explain fixed deposits."

❌ "Who won the FIFA World Cup?"

❌ "Write a Python program."

This helps keep chatbot responses relevant and reliable.

---

## 📸 Screenshots

Add screenshots of:

* Main chatbot interface
* FAQ response example
* AI-generated response example
* Domain restriction example

inside a `/screenshots` folder and reference them here.

---

## 🎯 Project Objectives

* Provide instant answers to banking FAQs
* Reduce dependency on manual customer support
* Demonstrate practical use of AI and NLP
* Build a domain-specific conversational assistant

---

## 🔮 Future Enhancements

* Multi-language support
* Voice-enabled interactions
* Database-backed knowledge base
* Conversation history storage
* User authentication
* Retrieval-Augmented Generation (RAG)

---

## 👨‍💻 Author

**Sushant Pawar**

Infosys Springboard Virtual Internship Project

---

## 📄 License

This project is licensed under the MIT License.
