
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = "super_secret_key"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin-login")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin-panel")
    return render_template("admin_login_styled.html")

@app.route("/admin-panel")
def admin_panel():
    if not session.get("admin"):
        return redirect("/admin-login")
    return render_template("admin_panel.html")

@app.route("/admin-add-member")
def add_member_form():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mitglieder")
    count = cursor.fetchone()[0] + 1
    conn.close()

    mitgliedsnummer = f"CB-BHV-{count:02d}"
    return render_template("admin_add_member.html", mitgliedsnummer=mitgliedsnummer)

@app.route("/add-member", methods=["POST"])
def add_member():
    if not session.get("admin"):
        return redirect("/admin-login")

    vorname = request.form["vorname"]
    nachname = request.form["nachname"]
    strasse = request.form["strasse"]
    plz = request.form["plz"]
    ort = request.form["ort"]
    staatsbuergerschaft = request.form["staatsbuergerschaft"]
    mitgliedsstatus = request.form["mitgliedsstatus"]
    bild = request.files["bild"].read() if "bild" in request.files and request.files["bild"] else None

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mitglieder")
    count = cursor.fetchone()[0] + 1
    mitgliedsnummer = f"CB-BHV-{count:02d}"

    cursor.execute("""
        INSERT INTO mitglieder (
            mitgliedsnummer, vorname, nachname, strasse, plz, ort, staatsbuergerschaft, mitgliedsstatus, bild
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        mitgliedsnummer, vorname, nachname, strasse, plz, ort, staatsbuergerschaft, mitgliedsstatus, bild
    ))
    conn.commit()
    conn.close()

    return redirect("/admin-panel")

@app.route("/member-search")
def member_search():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("SELECT mitgliedsnummer, vorname, nachname, plz, ort FROM mitglieder")
    mitglieder = cursor.fetchall()
    conn.close()

    return render_template("member_search.html", mitglieder=mitglieder)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
