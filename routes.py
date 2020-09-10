from app import app
from flask import redirect, render_template, request, session, flash
import user, review
import random

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/frontpage")
def frontpage():
    return render_template("front-page.html")

@app.route("/reviews/<int:id>")
def singlereview(id):
    target = review.get_one(id)
    if not target:
        return redirect("/")
    targetuser = user.get_one(target[0][7])
    return render_template("single-review.html", targetreview=target, targetuser=targetuser)

@app.route("/newreview", methods=["get","post"])
def newreview():
    if request.method == "GET": # random used to generate random number of invisible buttons for very simple spam protection.
        return render_template("new-review.html", rnumber=random.randint(1,15))
    if request.method == "POST":
        name = request.form["teaname"]
        teatype = request.form["teatype"]
        score = request.form["score"]
        shop = request.form["shop"]
        reviewtext = request.form["reviewtext"]
        picture_url = request.form["picture"]
        if review.send(name, teatype, score, shop, reviewtext, picture_url):
            return redirect("/frontpage")
        else:
            flash("Unable to post review, check mandatory info.")
        return redirect("/newreview")

@app.route("/browse",methods=["get","post"])
def browse():
    if request.method == "GET":
        list=review.get_list()
        return render_template("browse.html", reviews=list)
    if request.method == "POST":
        minscore = request.form["score"]
        if not minscore:
            minscore=1
        chosentype = request.form.getlist("teatype")
        if not chosentype:
            chosentype = ["Black Tea", "Green Tea", "Oolong Tea", "Other Tea", "Pu-erh Tea", "White Tea"]
        chosentype = tuple(chosentype)
        list = review.get_search(chosentype,minscore)
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
        flash('Wrong username or password')
        return render_template("index.html")

@app.route("/logout")
def logout():
    del session["user_name"]
    del session["user_id"]
    return redirect("/")

@app.errorhandler(404)
def backup(e):
    return redirect("/")
