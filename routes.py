from app import app
from flask import redirect, render_template, request, session, flash
import user, review

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/frontpage")
def frontpage():
    return render_template("front-page.html")

@app.route("/newreview", methods=["get","post"])
def newreview():
    if request.method == "GET":
        return render_template("new-review.html")
    if request.method == "POST":
        name = request.form["teaname"]
        teatype = request.form["teatype"]
        score = request.form["score"]
        shop = request.form["shop"]
        reviewtext = request.form["reviewtext"]
        if review.send(name, teatype, score, shop, reviewtext):
            return redirect("/frontpage")
        else:
            flash("Unable to post review, mandatory parts missing.")
            return redirect("/newreview")

@app.route("/browse")
def browse():
    list=review.get_list()
    return render_template("browse.html", reviews=list)

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) < 6 or len(username) > 20:
            flash("Username doesn't fit criteria")
            return redirect("/register")
        if len(password) < 6:
            flash("Password doesn't fit criteria")
            return redirect("/register")
        if user.register(username,password):
            return redirect("/")
        else:
            flash('Username "' + username + '" already taken')
            return redirect("/register")


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if user.login(username,password):
            return redirect("/frontpage")
    else:
            return render_template("index.html")

@app.route("/logout")
def logout():
    del session["user_name"]
    del session["user_id"]
    return redirect("/")
