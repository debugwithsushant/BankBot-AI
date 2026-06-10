# Decides if user query is banking-related or not

# All banking-related keywords
BANKING_KEYWORDS = [
    # Core banking
    "bank", "banking", "account", "balance", "deposit", "withdraw",
    "transaction", "transfer", "payment", "branch", "passbook",

    # Cards & ATM
    "atm", "debit", "credit", "card", "pin", "swipe",

    # Loans & interest
    "loan", "emi", "interest", "mortgage", "borrow", "repay",
    "instalment", "installment", "collateral",

    # Digital banking
    "upi", "neft", "rtgs", "imps", "net banking", "internet banking",
    "mobile banking", "gpay", "phonepe", "paytm", "bhim",

    # Savings & investments
    "savings", "fd", "fixed deposit", "recurring", "rd", "investment",
    "mutual fund", "insurance",

    # Security & KYC
    "kyc", "otp", "fraud", "scam", "phishing", "password", "secure",
    "ifsc", "micr", "cheque", "demand draft", "dd",

    # Indian banking terms
    "rbi", "nbfc", "sebi", "npci", "rupay", "visa", "mastercard",
    "jan dhan", "pmjdy", "aadhaar", "pan card"
]


def is_banking_query(user_query):
    query = user_query.lower().strip()

    # Check each banking keyword
    for keyword in BANKING_KEYWORDS:
        if keyword in query:
            return True

    return False