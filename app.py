
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mitglieder (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mitgliedsnummer TEXT,
            vorname TEXT,
            nachname TEXT,
            strasse TEXT,
            plz TEXT,
            ort TEXT
        )
    """)
    conn.commit()
    conn.close()

def generate_next_member_id():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mitglieder")
    count = cursor.fetchone()[0]
    conn.close()
    return f"CB-BHV-{count + 1:02d}"

@app.route("/admin-add-member")
def add_member_form():
    mitgliedsnummer = generate_next_member_id()
    return render_template("admin_add_member.html", mitgliedsnummer=mitgliedsnummer)

@app.route("/add-member", methods=["POST"])
def add_member():
    mitgliedsnummer = request.form["mitgliedsnummer"]
    vorname = request.form["vorname"]
    nachname = request.form["nachname"]
    strasse = request.form["strasse"]
    plz = request.form["plz"]
    ort = request.form["ort"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mitglieder (mitgliedsnummer, vorname, nachname, strasse, plz, ort) VALUES (?, ?, ?, ?, ?, ?)",
        (mitgliedsnummer, vorname, nachname, strasse, plz, ort)
    )
    conn.commit()
    conn.close()

    return f"Mitglied {mitgliedsnummer} wurde erfolgreich hinzugefügt."

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
