
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'geheimes_ding'

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for("admin_panel"))
        else:
            return "Login fehlgeschlagen", 401
    return render_template("admin_login.html")

@app.route("/admin")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return render_template("admin_panel.html")

@app.route("/admin/add-member", methods=["GET", "POST"])
def admin_add_member():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        name = request.form.get("name")
        nummer = request.form.get("mitgliedsnummer")
        geburtsdatum = request.form.get("geburtsdatum")
        adresse = request.form.get("adresse")
        print(f"NEUES MITGLIED: {name}, Nr: {nummer}, Geb: {geburtsdatum}, Adr: {adresse}")
        return "Mitglied wurde (simuliert) hinzugefügt!"
    return render_template("admin_add_member.html")

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/")
def home():
    return redirect(url_for("admin_login"))
