from flask import Flask, render_template, request, jsonify
import time
from db.db_utils import get_recent, add_data, get_data
from llm import LLM
from db.client import DB

app = Flask(__name__)


def create_test_user(collection):
    """
        Sets up the test user <admin> and add 15 notes
    """
    notes = [
        "Meeting with Board of Directors at 10 AM - Discuss quarterly financials and new strategic initiatives.",
        "Client Lunch Meeting - Book a table at the downtown restaurant. Confirm with the client.",
        "Staff Training Session - Organize training on new software implementation for the sales team.",
        "Review Contracts - Go through the terms of the new partnership agreement with the legal team.",
        "Follow Up with Marketing - Check on the progress of the new product launch campaign.",
        "Order Office Supplies - Restock pens, paper, and printer ink. Contact the office manager.",
        "Conference Call with Overseas Partners - Set up a call for 3 PM to discuss shipment delays.",
        "Budget Review - Meet with the finance team to review next year's budget plans.",
        "Prepare Presentation - Create a slide deck for the upcoming industry conference.",
        "Client Satisfaction Survey Results - Analyze the feedback and identify areas for improvement.",
        "Team Meeting - Schedule a team-building activity for next week. Find a venue and arrange logistics.",
        "Employee Evaluations - Start preparing feedback for annual employee performance reviews.",
        "Networking Event - Attend the industry networking event. Bring business cards.",
        "Office Renovation Planning - Consult with the design team about new office layout and color schemes.",
        "Research New Business Opportunities - Explore potential markets and identify growth prospects for the next fiscal year.",
    ]
    # Example of queries: Get info about all meetings/What meeting do I need to attend at ten o'clock
    for note in notes:
        add_data(collection, note, "admin")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/set_username", methods=["POST"])
def set_username():
    username = request.form.get("username")
    return jsonify({"username": f"Hello {username}!"})


@app.route("/insert_note", methods=["POST"])
def insert_note():
    note = request.form.get("note")
    username = request.form.get("username")
    add_data(collection, note, username)
    return jsonify({"status": "Note added", "note": note})


@app.route("/get_recent_notes", methods=["POST"])
def get_recent_notes():
    n = int(request.form.get("n"))
    username = request.form.get("username")
    last_notes = get_recent(collection, n, username)[::-1]
    last_notes_formatted = []
    for i, note in enumerate(last_notes):
        last_notes_formatted.extend([f" {i+1}. " + note.replace("\n", "<br>")])
    return jsonify({"last_notes": last_notes_formatted})


@app.route("/search", methods=["POST"])
def search():
    message = request.form.get("query")
    username = request.form.get("username")
    notes = get_data(collection, message, username)["documents"][0]
    response = llm.reply(message, notes)
    return jsonify({"response": response})


if __name__ == "__main__":

    db = DB()
    collection = db.get_collection("personal_assistant")
    create_test_user(collection)

    llm = LLM()
    app.run(debug=True, host="0.0.0.0", port=5000)
