
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'geheimes_ding'

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
USER_ID = "10001"
USER_PASS = "user123"

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for("admin_panel"))
        else:
            return "Admin Login fehlgeschlagen", 401
    return render_template("admin_login.html")

@app.route("/admin")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return render_template("admin_panel.html")

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        if request.form.get("user_id") == USER_ID and request.form.get("password") == USER_PASS:
            session['user_logged_in'] = True
            return redirect(url_for("user_panel"))
        else:
            return "User Login fehlgeschlagen", 401
    return render_template("user_login.html")

@app.route("/user")
def user_panel():
    if not session.get("user_logged_in"):
        return redirect(url_for("user_login"))
    return render_template("user_panel.html")

@app.route("/user-logout")
def user_logout():
    session.pop("user_logged_in", None)
    return redirect(url_for("user_login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
