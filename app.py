
from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3
import os
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = "super_secret_key"

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

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

@app.route("/add-member", methods=["POST"])
def add_member():
    if not session.get("admin"):
        return redirect("/admin-login")

    vorname = request.form["vorname"]
    nachname = request.form["nachname"]
    geburtsdatum = request.form["geburtsdatum"]
    straße = request.form["straße"]
    plz = request.form["plz"]
    ort = request.form["ort"]
    staatsbuergerschaft = request.form["staatsbuergerschaft"]
    mitgliedstyp = request.form["mitgliedstyp"]

    profilbild = request.files["profilbild"]
    dokument = request.files["dokument"]

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM mitglieder")
    result = cursor.fetchone()
    next_id = (result[0] or 0) + 1
    mitgliedsnummer = f"CB-BHV-{next_id:02d}"

    # Profilbild speichern
    if profilbild and profilbild.filename:
        pb_name = secure_filename(mitgliedsnummer + "_profilbild" + os.path.splitext(profilbild.filename)[1])
        profilbild_path = os.path.join(UPLOAD_FOLDER, pb_name)
        profilbild.save(profilbild_path)
        with open(profilbild_path, "rb") as f:
            bild_bytes = f.read()
    else:
        bild_bytes = None

    # Dokument speichern
    if dokument and dokument.filename:
        ext = os.path.splitext(dokument.filename)[1].lower()
        if ext in [".pdf", ".jpg", ".jpeg"]:
            filename = f"{mitgliedsnummer}{ext}"
            dokument.save(os.path.join(UPLOAD_FOLDER, filename))

    cursor.execute("""
        INSERT INTO mitglieder (
            mitgliedsnummer, vorname, nachname, geburtsdatum, straße, plz, ort,
            staatsbuergerschaft, mitgliedsstatus, bild
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        mitgliedsnummer, vorname, nachname, geburtsdatum, straße, plz, ort,
        staatsbuergerschaft, mitgliedstyp, bild_bytes
    ))
    conn.commit()
    conn.close()

    return redirect(f"/admin-panel?success={mitgliedsnummer}")

@app.route("/next-id")
def get_next_id():
    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM mitglieder")
    result = cursor.fetchone()
    conn.close()
    next_id = (result[0] or 0) + 1
    return f"CB-BHV-{next_id:02d}"

@app.route("/member-search")
def member_search():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("SELECT mitgliedsnummer, vorname, nachname, straße, mitgliedsstatus, plz, ort FROM mitglieder")
    mitglieder = cursor.fetchall()
    conn.close()

    return render_template("member_search.html", mitglieder=mitglieder)

@app.route("/delete-member", methods=["POST"])
def delete_member():
    if not session.get("admin"):
        return redirect("/admin-login")

    mitgliedsnummer = request.form["mitgliedsnummer"]

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mitglieder WHERE mitgliedsnummer = ?", (mitgliedsnummer,))
    conn.commit()
    conn.close()

    return redirect("/member-search")

@app.route("/mitglied/<mitgliedsnummer>")
def mitglied_detail(mitgliedsnummer):
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("club.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vorname, nachname, straße, plz, ort,
               staatsbuergerschaft, mitgliedsstatus, bild
        FROM mitglieder WHERE mitgliedsnummer = ?
    """, (mitgliedsnummer,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return "Mitglied nicht gefunden", 404

    vorname, nachname, straße, plz, ort, staatsbuergerschaft, mitgliedstyp, bild = result
    symbol_map = {
        "Bronze": "🥉",
        "Silber": "🥈",
        "Gold": "🥇",
        "Platin": "💎"
    }
    symbol = symbol_map.get(mitgliedstyp, "")

    foto_url = None
    if bild:
        foto_url = "data:image/png;base64," + base64.b64encode(bild).decode("utf-8")

    formular_url = None
    for ext in [".pdf", ".jpg", ".jpeg"]:
        test_path = os.path.join(UPLOAD_FOLDER, f"{mitgliedsnummer}{ext}")
        if os.path.exists(test_path):
            formular_url = f"/uploads/{mitgliedsnummer}{ext}"
            break

    return render_template("mitglied_detail.html",
        mitgliedsnummer=mitgliedsnummer,
        vorname=vorname,
        nachname=nachname,
        straße=straße,
        plz=plz,
        ort=ort,
        staatsbuergerschaft=staatsbuergerschaft,
        mitgliedstyp=mitgliedstyp,
        symbol=symbol,
        foto_url=foto_url or "/static/default-user.png",
        formular_url=formular_url
    )

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
