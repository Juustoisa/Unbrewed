from app import app
from flask import redirect, render_template, request, session, flash
import user, review
import random

#Login screen / landing page
@app.route("/")
def index():
    return render_template("index.html")
#Hub page
@app.route("/frontpage")
def frontpage():
    return render_template("front-page.html")

#See single review
@app.route("/reviews/<int:id>")
def singlereview(id):
    target = review.get_one(id)
    if not target:
        return redirect("/browse")
    targetuser = user.get_one(target[0][7])
    isReviewer = False
    if session["user_id"] == target[0][7]:
        isReviewer = True
    return render_template("single-review.html", targetreview=target, targetuser=targetuser, isReviewer=isReviewer)

#Delete review
@app.route("/reviews/<int:id>/delete",methods=["GET","POST"])
def deletereview(id):
    if request.method == "POST":
        if review.delete(id,session["user_id"]):
            return redirect("/browse")
    if request.method == "GET":
        return redirect("/reviews/" + str(id))

#Post new review
@app.route("/newreview", methods=["get","post"])
def newreview():
    if request.method == "GET": # random used to generate random number of invisible buttons for very simple spam protection.
        return render_template("new-review.html", rnumber=random.randint(1,15))
    if request.method == "POST":
        incompleteReviews = False
        name = request.form["teaname"]
        if len(name) < 5:
            flash("Tea name too short")
            incompleteReviews = True
        elif len(name) > 100:
            flash("Tea name too long")
            incompleteReviews = True
        teatype = request.form["teatype"]
        score = request.form["score"]
        shop = request.form["shop"]
        reviewtext = request.form["reviewtext"]
        if len(reviewtext) > 600:
            flash("Reviews have a maximum length of 600 characters")
            incompleteReviews = True
        picture_url = request.form["picture"]
        if incompleteReviews:
            redirect("/newreview")
        elif review.send(name, teatype, score, shop, reviewtext, picture_url):
            return redirect("/frontpage")
        else:
            flash("Unable to post review, check mandatory info.")
        return redirect("/newreview")

#Browse reviews
@app.route("/browse",methods=["get","post"])
def browse():
    if request.method == "GET":
        list=review.get_list()
        amount=review.get_amount()
        return render_template("browse.html", reviews=list, amount=amount)
    if request.method == "POST":
        minscore = request.form["score"]
        if not minscore:
            minscore=1
        chosentype = request.form.getlist("teatype")
        if not chosentype:
            chosentype = ["Black Tea", "Green Tea", "Oolong Tea", "Other Tea", "Pu-erh Tea", "White Tea"]
        chosentype = tuple(chosentype)
        namesearch = request.form["namesearch"]
        if not namesearch:
            namesearch = ""
        list = review.get_search(chosentype,minscore,namesearch)
        amount=review.get_amount()
        return render_template("browse.html", reviews=list, amount=amount)

#Browse users
@app.route("/users",methods=["get","post"])
def users():
    if request.method == "GET":
        list=user.get_list()
        return render_template("users.html", users=list)

#Get profile
@app.route("/users/<int:id>")
def profile(id):
    target=user.get_profile(id)
    return render_template("profile.html", targetuser=target)

#Register user
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
            flash('User "' + username + '" created', 'flashSuccess')
            return redirect("/")
        else:
            flash('Username "' + username + '" already taken.', 'flashError')
            return redirect("/register")

#Login
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if user.login(username,password):
            return redirect("/frontpage")
    else:
        flash('Wrong username or password')
        return render_template("index.html")
#Logout
@app.route("/logout")
def logout():
    del session["user_name"]
    del session["user_id"]
    return redirect("/")
#Redirect 
@app.errorhandler(404)
def backup(e):
    return redirect("/browse")
