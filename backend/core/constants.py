CACHE_THRESHOLD = 0.90
CACHE_EXPIRY_DAYS = 30
MODEL_VERSION = "qwen2.5:1.5b"
CACHE_VERSION = "1.5"
EMBEDDING_MODEL_VERSION = "BAAI/bge-small-en-v1.5"

RULE_BASED_INTENTS = {
    "GREETING": [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ],
    "GOODBYE": [
        "bye",
        "thanks",
        "thank you",
        "see you",
    ],
}

FOLLOWUP_PATTERNS = [
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    "they",
    "them",
    "same",
    "also",
    "another",
    "again",
    "earlier",
    "previous",
    "above",
    "how many",
    "how much",
    "what about",
    "what if",
    "can i",
    "does this",
    "is this",
]

ALLOWED_CATEGORIES = {
    "Leave Policy",
    "Attendance",
    "Payroll",
    "Travel",
    "Insurance",
    "Employee Benefits",
    "Performance",
    "Recruitment",
    "Learning",
    "Onboarding",
    "Exit",
    "OutOfScope",
}

ALLOWED_INTENTS = {
    "Information",
    "Eligibility",
    "Procedure",
    "Comparison",
    "Policy",
    "Document",
    "Unknown",
}
