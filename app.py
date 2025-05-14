
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
    return "<h1>Admin Login Seite</h1><form method='post'><input name='admin_id' placeholder='Admin-ID'><br><input name='password' type='password'><br><button type='submit'>Login</button></form>"

@app.route("/admin-panel")
def admin_panel():
    if not session.get("admin"):
        return redirect("/admin-login")
    return render_template("admin_panel.html")

@app.route("/admin-add-member")
def add_member_form():
    if not session.get("admin"):
        return redirect("/admin-login")
    return render_template("admin_add_member.html", mitgliedsnummer="CB-BHV-01")

@app.route("/add-member", methods=["POST"])
def add_member():
    return "Mitglied erfolgreich gespeichert."
