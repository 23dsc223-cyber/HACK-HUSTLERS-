from flask import Flask, render_template, request, jsonify
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ---------------- SAFE TEXT HANDLER ----------------

def safe_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(map(str, value))
    if isinstance(value, dict):
        return " ".join(map(str, value.values()))
    return str(value)

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

# ---------------- LOAD DATA ----------------

with open("data/colleges.json", "r", encoding="utf-8") as f:
    college = json.load(f)   # SINGLE OBJECT ✅

with open("data/qa.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

with open("data/smalltalk.json", "r", encoding="utf-8") as f:
    smalltalk = json.load(f)

# ---------------- PREPARE NLP CORPUS ----------------

corpus_map = {
    "overview": safe_text(college.get("overview")),
    "history": safe_text(college.get("history")),
    "courses": safe_text(college.get("courses")),
    "fees": safe_text(college.get("fees_estimates")),
    "admissions": safe_text(college.get("admissions")),
    "facilities": safe_text(college.get("facilities")),
    "contact": safe_text(college.get("contact")),
    "location": safe_text(college.get("location"))
}

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus_map.values())

CONFIDENCE_THRESHOLD = 0.40

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- CHAT API ----------------

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = normalize(request.json.get("message", ""))

    # 1️⃣ SMALL TALK
    if user_msg in smalltalk:
        return jsonify({"reply": smalltalk[user_msg]})

    # 2️⃣ EXACT Q&A FROM JSON
    if user_msg in qa_data:
        return jsonify({"reply": qa_data[user_msg]})

    # 3️⃣ RULE-BASED INTENTS
    if re.search(r"\b(course|courses|degree|program)\b", user_msg):
        return jsonify({"reply": corpus_map["courses"]})

    if re.search(r"\b(fee|fees|cost|tuition)\b", user_msg):
        return jsonify({"reply": corpus_map["fees"]})

    if re.search(r"\b(admission|apply|eligibility)\b", user_msg):
        return jsonify({"reply": corpus_map["admissions"]})

    if re.search(r"\b(facilities|hostel|library|canteen|parking)\b", user_msg):
        return jsonify({"reply": corpus_map["facilities"]})

    if re.search(r"\b(contact|phone|email)\b", user_msg):
        return jsonify({"reply": corpus_map["contact"]})

    if re.search(r"\b(location|where|address)\b", user_msg):
        return jsonify({"reply": corpus_map["location"]})

    if re.search(r"\b(about|history|college)\b", user_msg):
        return jsonify({"reply": corpus_map["overview"]})

    # 4️⃣ SMART NLP WITH BOOST
    query_vec = vectorizer.transform([user_msg])
    scores = cosine_similarity(query_vec, X)[0]

    boost = {
        "course": "courses",
        "fee": "fees",
        "admission": "admissions",
        "facility": "facilities",
        "hostel": "facilities",
        "college": "overview"
    }

    keys = list(corpus_map.keys())

    for word, key in boost.items():
        if word in user_msg:
            scores[keys.index(key)] += 0.3

    if max(scores) >= CONFIDENCE_THRESHOLD:
        best_index = scores.argmax()
        return jsonify({"reply": list(corpus_map.values())[best_index]})

    # 5️⃣ SAFE FALLBACK
    return jsonify({
        "reply": (
            "🤔 I didn’t understand that.\n\n"
            "You can ask me about:\n"
            "• Courses & Fees\n"
            "• Admissions\n"
            "• Facilities (hostel, parking, library)\n"
            "• Contact details\n"
            "• College overview"
        )
    })

# ---------------- ADMIN PANEL ----------------

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/save", methods=["POST"])
def save_qa():
    data = request.json
    question = normalize(data.get("question", ""))
    answer = data.get("answer", "").strip()

    if not question or not answer:
        return jsonify({"message": "❌ Question and answer required"})

    qa_data[question] = answer

    with open("data/qa.json", "w", encoding="utf-8") as f:
        json.dump(qa_data, f, indent=2, ensure_ascii=False)

    return jsonify({"message": "✅ Saved successfully"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

