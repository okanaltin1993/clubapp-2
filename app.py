
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
USER_ID = "10001"
USER_PASS = "user123"

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            return redirect(url_for("admin_panel"))
        else:
            return "Admin Login fehlgeschlagen", 401
    return render_template("admin_login.html")

@app.route("/admin")
def admin_panel():
    return render_template("admin_panel.html")

@app.route("/", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        if request.form.get("user_id") == USER_ID and request.form.get("password") == USER_PASS:
            return redirect(url_for("user_panel"))
        else:
            return "User Login fehlgeschlagen", 401
    return render_template("user_login.html")

@app.route("/user")
def user_panel():
    return render_template("user_panel.html")

if __name__ == "__main__":
app.run(host="0.0.0.0", port=10000)
