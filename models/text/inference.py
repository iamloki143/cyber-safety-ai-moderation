from transformers import pipeline

# Load toxicity model
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

# Tanglish abusive slang
TANGLISH_ABUSE = [
    "punda","oombu","thevdiya","thevidiya",
    "naaye","panni","pundamavan","thayoli",
    "otha","baadu","thooma","gunda","porukki",
    "porambokku","koothi","lawda","sootha",
    "soothu","kunji","othalokka","poolu",
    "pool","mola","molai","kottai","kola"
]
# English abusive words
ENGLISH_ABUSE = [
    "fuck","bitch","idiot","stupid","dumb",
    "asshole","bastard","kill","die"
]

# Tanglish indicator words
TANGLISH_WORDS = [
    "nalla","paiyan","ponnu","romba",
    "enna","seri","machan","anna",
    "super","mass","semma"
]


def detect_language(text):
    lower = text.lower()

    for word in TANGLISH_ABUSE:
        if word in lower:
            return "tanglish"

    for word in TANGLISH_WORDS:
        if word in lower:
            return "tanglish"

    return "english"


def predict_text(text: str):

    lower = text.lower()

    # Run AI model first
    result = classifier(text)[0]
    label = result["label"]
    score = result["score"]

    language = detect_language(text)
    category = "Neutral"

    # Rule override for Tanglish abuse
    for word in TANGLISH_ABUSE:
        if word in lower:
            category = "Bullying"

    # Rule override for English abuse
    for word in ENGLISH_ABUSE:
        if word in lower:
            category = "Bullying"

    # AI-based decision
    if label == "LABEL_1" and score > 0.60:
        category = "Bullying"

    return {
        "language": language,
        "category": category,
        "confidence": score
    }