from app import app
from flask import redirect, render_template, request, session, flash
import user, review, comment, like
import random

# Login screen / landing page
@app.route("/")
def index():
    return render_template("index.html")
# Hub page
@app.route("/frontpage")
def frontpage():
    return render_template("front-page.html")

# See single review
@app.route("/reviews/<int:id>")
def singlereview(id):
    target = review.get_one(id)
    comment_list = comment.get_comments_on_review(id)
    has_liked = like.check_if_liked(id,session["user_id"])
    if not target:
        return redirect("/reviews")
    targetuser = user.get_one(target[0][7])
    isReviewer = False
    if session["user_id"] == target[0][7]:
        isReviewer = True
    return render_template("single-review.html", targetreview=target, targetuser=targetuser, isReviewer=isReviewer, comment_list=comment_list, has_liked=has_liked)

# Comment handler
@app.route("/reviews/<int:id>/comments", methods=["POST"])
def comments(id):
    if request.method == "POST":
        user_id = session["user_id"]
        if not user_id:
            flash('Login first.', 'flashError')  
            return redirect("/reviews/" + str(id))
        commenttext = request.form["commenttext"]
        if len(commenttext) < 8:
            flash('Comment too short. Comment length should be between 8-600 characters.', 'flashError')
            return redirect("/reviews/" + str(id))
        if len(commenttext) > 600:
            flash('Comment too long. Comment length should be between 8-600 characters.', 'flashError')
            return redirect("/reviews/" + str(id))
        if comment.send(id,user_id,commenttext):
            flash('Comment posted', 'flashSuccess')
            return redirect("/reviews/" + str(id))
    flash('Failed to add comment.', 'flashError')        
    return redirect("/reviews/" + str(id))

# Comment delete
@app.route("/reviews/<int:id>/comments/<int:delete_id>", methods=["GET","POST"])
def delete_comment(id,delete_id):
    if request.method == "GET":
        return redirect("/reviews/" + str(id))
    if request.method == "POST":
        user_id = session["user_id"]
        if comment.delete(delete_id,user_id):
            return redirect("/reviews/" + str(id))
    return redirect("/reviews/" + str(id))

# Like handler
@app.route("/reviews/<int:id>/like", methods=["GET","POST"])
def likes(id):
    if request.method == "POST":
        review_id = id
        user_id = session["user_id"]
        if not review_id or not user_id:
            flash('Something went wrong', 'flashError')
            return redirect("/reviews/" + str(id))
        if like.send(review_id,user_id):
            return redirect("/reviews/" + str(id))
    

# Unlike handler
@app.route("/reviews/<int:id>/unlike", methods=["GET","POST"])
def unlikes(id):
    if request.method == "POST":
        review_id = id
        user_id = session["user_id"]
        if not review_id or not user_id:
            flash('Something went wrong', 'flashError')
            return redirect("/reviews/" + str(id))
        if like.remove(review_id,user_id):
            return redirect("/reviews/" + str(id))
    

# See reviews of single tea
@app.route("/teas/<name>")
def reviews(name):
    if request.method == "GET":
        list = review.get_tea_reviews(name)
        if not list:
            return redirect("/teas")
        return render_template("reviews-for-tea.html", reviews=list, userID=session["user_id"])

# Delete review
@app.route("/reviews/<int:id>/delete",methods=["GET","POST"])
def deletereview(id):
    if request.method == "POST":
        if review.delete(id,session["user_id"]):
            flash('Review deleted successfully.', 'flashSuccess')
            return redirect("/frontpage")
    if request.method == "GET":
        return redirect("/reviews/" + str(id))

# Post new review
@app.route("/newreview", methods=["get","post"])
def newreview():
    if request.method == "GET": # random used to generate random number of invisible buttons for very simple spam protection.
        return render_template("new-review.html", rnumber=random.randint(1,15))
    if request.method == "POST":
        incompleteReviews = False
        name = request.form["teaname"]
        if len(name.strip()) < 5:
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
        elif review.send(name.strip().lower().capitalize(), teatype, score, shop, reviewtext, picture_url):
            flash('New review posted successfully.', 'flashSuccess')
            return redirect("/frontpage")
        else:
            flash("Unable to post review, check mandatory info.")
        return redirect("/newreview")

# Prefilled name review
@app.route("/newreview/<name>", methods=["get"])
def prefilled_name_review(name):
        return render_template("new-review.html", rnumber=random.randint(1,15), teaname=name)


# Browse teas
@app.route("/teas",methods=["get","post"])
def teas():
    if request.method == "GET":
        list=review.get_tea_list()
        amount = len(list)
        return render_template("teas.html", reviews=list, amount=amount)
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
        list = review.get_search_teas(chosentype,minscore,namesearch)
        amount=len(review.get_tea_list())
        return render_template("teas.html", reviews=list, amount=amount)


# Browse reviews
@app.route("/reviews",methods=["get","post"])
def browse():
    if request.method == "GET":
        list=review.get_list()
        amount = len(list)
        return render_template("reviews.html", reviews=list, amount=amount)
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
        amount = review.get_amount()[0][0]
        return render_template("reviews.html", reviews=list, amount=amount)

# Not needed currently
# Link reviews from teaname 
# @app.route("/reviews/<name>",methods=["get"])
# def reviews_for_tea(name):
#    if request.method == "GET":
#        minscore=1
#        chosentype = ["Black Tea", "Green Tea", "Oolong Tea", "Other Tea", "Pu-erh Tea", "White Tea"]
#        chosentype = tuple(chosentype)
#        namesearch = name
#        list = review.get_search(chosentype,minscore,namesearch)
#        amount = review.get_amount()[0][0]
#        return render_template("reviews.html", reviews=list, amount=amount)

# Browse users
@app.route("/users",methods=["get","post"])
def users():
    if request.method == "GET":
        list=user.get_list()
        return render_template("users.html", users=list)

# Get profile
@app.route("/users/<int:id>")
def profile(id):
    target=user.get_profile(id)
    return render_template("profile.html", targetuser=target, user_id=id)

# Register user
@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username.strip()) < 6 or len(username) > 20:
            flash("Username doesn't fit criteria")
            return redirect("/register")
        if len(password) < 6:
            flash("Password doesn't fit criteria")
            return redirect("/register")
        if user.register(username.strip(),password):
            flash('User "' + username.strip() + '" created', 'flashSuccess')
            return redirect("/")
        else:
            flash('Username "' + username + '" already taken. Username uniqueness is case-insensitive.', 'flashError')
            return redirect("/register")

# Login
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if user.login(username,password):
            return redirect("/frontpage")
    else:
        flash('Wrong username or password', 'flashError')
        return render_template("index.html")

# Logout
@app.route("/logout")
def logout():
    del session["user_name"]
    del session["user_id"]
    flash('Logged out', 'flashSuccess')
    return redirect("/")

# Delete account
@app.route("/users/<int:id>/delete",methods=["POST"])
def delete_user(id):
    username = session["user_name"]
    if user.delete_user(id):
        flash('Profile ' + username + ' deleted, all reviews, comments and likes removed.', 'flashSuccess')
        return redirect("/")
    return redirect("/")

# Redirect 
@app.errorhandler(404)
def backup(e):
    return redirect("/frontpage")
