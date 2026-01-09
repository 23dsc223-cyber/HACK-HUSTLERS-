from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# ------------------ ACADEMIC DATA ------------------

academic_calendar = {
    "reopen": "16 June 2025",
    "odd_exam": "27 Oct – 12 Nov 2025",
    "even_exam": "13 – 29 April 2026",
    "vacation": "30 April 2026"
}

internal_tests = [
    "18 – 26 August 2025",
    "1 – 7 October 2025",
    "27 Jan – 4 Feb 2026",
    "11 – 19 March 2026"
]

fees = {
    "tuition": "17 July 2025",
    "exam_fee": "22 September 2025",
    "even_exam_fee": "2 February 2026"
}

events = [
    "Orientation Programme: 3, 4 & 7 July 2025",
    "Graduation Day: 24 January 2026"
]

departments = [
    "Department of Data Science",
    "Computer Science",
    "Mathematics",
    "Commerce",
    "English",
    "History",
    "Tamil",
    "Biotechnology",
    "Artificial Intelligence (AI)",
    "BBA",
    "BCA"
]

campus_location = "The American College Satellite Campus is located at Chatrapatti, Madurai."

holidays = [
    "2025-08-15",
    "2025-10-02",
    "2026-01-14",
    "2026-01-15",
    "2026-01-26"
]

day_orders = {
    "2026-01-08": "Day Order II",
    "2026-01-09": "Day Order III",
    "2026-01-12": "Day Order IV",
    "2026-01-13": "Day Order V"
}

# ------------------ FUNCTIONS ------------------

def next_working_day(today):
    nxt = today + timedelta(days=1)
    while nxt.strftime("%Y-%m-%d") in holidays:
        nxt += timedelta(days=1)
    return nxt

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["message"].lower()
    today = datetime.today()

    # Greeting
    if msg in ["hi", "hello", "hai", "hey"]:
        return jsonify({"reply": "Hello, how can I help you!"})

    # Help
    if "help" in msg:
        return jsonify({
            "reply":
            "📌 You can ask me:\n"
            "- academic calendar\n"
            "- today date\n"
            "- today day order\n"
            "- next day order\n"
            "- exam date\n"
            "- internal test\n"
            "- fee payment date\n"
            "- departments\n"
            "- campus location\n"
            "- holidays\n"
            "- events"
        })

    # Today Date
    if "today date" in msg:
        return jsonify({"reply": today.strftime("📅 %d %B %Y (%A)")})

    # Today Day Order
    if "today day order" in msg:
        return jsonify({
            "reply": day_orders.get(today.strftime("%Y-%m-%d"), "Day order not available")
        })

    # Next Day Order
    if "next day order" in msg:
        nxt = next_working_day(today)
        return jsonify({
            "reply": f"{nxt.strftime('%d %B %Y')} → {day_orders.get(nxt.strftime('%Y-%m-%d'), 'Not available')}"
        })

    # Academic Calendar
    if "academic calendar" in msg:
        return jsonify({
            "reply":
            f"📅 Academic Calendar:\n"
            f"• College Reopens: {academic_calendar['reopen']}\n"
            f"• Odd Semester Exams: {academic_calendar['odd_exam']}\n"
            f"• Even Semester Exams: {academic_calendar['even_exam']}\n"
            f"• Vacation Starts: {academic_calendar['vacation']}"
        })

    # Internal Tests
    if "internal" in msg:
        return jsonify({"reply": "📝 Internal Tests:\n" + "\n".join(internal_tests)})

    # Exam Dates
    if "exam" in msg:
        return jsonify({
            "reply":
            f"🧪 Exam Dates:\n"
            f"• Odd Semester: {academic_calendar['odd_exam']}\n"
            f"• Even Semester: {academic_calendar['even_exam']}"
        })

    # Fee Payment
    if "fee" in msg or "payment" in msg:
        return jsonify({
            "reply":
            f"💳 Fee Payment Dates:\n"
            f"• Tuition Fee: {fees['tuition']}\n"
            f"• Exam Fee: {fees['exam_fee']}\n"
            f"• Even Semester Exam Fee: {fees['even_exam_fee']}"
        })

    # Departments
    if "department" in msg:
        return jsonify({"reply": "🏢 Departments:\n" + "\n".join(departments)})

    # Campus Location
    if "location" in msg or "where" in msg:
        return jsonify({"reply": "📍 " + campus_location})

    # Holidays
    if "holiday" in msg:
        return jsonify({"reply": "🎉 Holidays:\n" + "\n".join(holidays)})

    # Events
    if "event" in msg:
        return jsonify({"reply": "🎊 Events:\n" + "\n".join(events)})

    return jsonify({
        "reply": "Sorry, I didn't understand. Type 'help' to see available options."
    })

if __name__ == "__main__":
    app.run(debug=True)