from db import db
from flask import session
import user

# Browse reviews
def get_list():
    sql = "SELECT R.id, R.name, R.score FROM reviews R ORDER BY r.score DESC LIMIT 15"
    result = db.session.execute(sql)
    return result.fetchall()

# Browse teas
def get_tea_list():
    sql = "SELECT name, REPLACE(teatype,' ',''), ROUND( AVG(score),2) AS AVG FROM reviews GROUP BY name, teatype ORDER BY AVG DESC"
    result = db.session.execute(sql)
    return result.fetchall()

# Get reviews for specific tea
def get_tea_reviews(name):
    sql = """SELECT reviews.*, users.username, COUNT(likes.*) FROM reviews JOIN users ON users.id = Reviews.user_id 
    LEFT JOIN likes ON likes.review_id=reviews.id WHERE name=:name GROUP BY reviews.id, users.username"""
    result = db.session.execute(sql, {"name":name})
    return result.fetchall()

# Get amount
def get_amount():
    sql = "SELECT Count(*) FROM reviews"
    result = db.session.execute(sql)
    return result.fetchall()

# Search functionality teas
def get_search_teas(chosentype,minscore,namesearch):
    namesearch = "%" + namesearch + "%"
    sql = """SELECT name, REPLACE(teatype,' ',''), ROUND( AVG(score),2) AS AVG FROM reviews WHERE teatype 
    IN :chosentype AND name ILIKE :namesearch GROUP BY name, teatype HAVING AVG(score)>:minscore ORDER BY AVG DESC"""
    result = db.session.execute(sql, {"chosentype":chosentype, "minscore":minscore, "namesearch":namesearch})
    return result.fetchall()

# Search functionality reviews
def get_search(chosentype,minscore,namesearch):
    namesearch = "%" + namesearch + "%"
    sql = "SELECT R.id, R.name, R.score FROM reviews R WHERE R.teatype IN :chosentype AND R.score >= :minscore AND R.name ILIKE :namesearch ORDER BY r.score DESC"
    result = db.session.execute(sql, {"chosentype":chosentype, "minscore":minscore, "namesearch":namesearch})
    return result.fetchall()

# Get single review
def get_one(id):
    user_id=session["user_id"]
    sql = """SELECT reviews.*, COUNT(likes.*) FROM reviews LEFT JOIN likes ON likes.review_id=:id Where Reviews.id=:id GROUP BY reviews.id"""
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

# Save review to db, delete if there's duplicate
def send(name, teatype, score, shop, reviewtext, picture_url):
    user_id = user.user_id()

    if user_id == 0:
        return False
    if not name or not teatype or not score:
       return False
    if len(reviewtext) > 600:
        return False
    if not picture_url:
        picture_url="../static/kuppi.jpg"
    if not reviewtext:
        reviewtext = "Reviewer didn't provide a written review."
    
    sql = "DELETE FROM Reviews WHERE reviews.name=:name AND reviews.user_id=:user_id"
    db.session.execute(sql, {"name":name, "user_id":user_id})
    db.session.commit()
   
    sql = """INSERT INTO reviews (name, shop, teatype, score, reviewtext, picture_url, user_id) 
    VALUES (:name, :shop, :teatype, :score, :reviewtext, :picture_url, :user_id)"""
    db.session.execute(sql, {"name":name, "shop":shop, "teatype":teatype, "score":score, "reviewtext":reviewtext, "picture_url":picture_url, "user_id":user_id})
    db.session.commit()
    return True
# Delete review
def delete(id, user_id):
        if not id:
            return False
        if not user_id:
            return False
        sql = "DELETE FROM Reviews WHERE id=:id AND user_id=:user_id"
        db.session.execute(sql, {"id":id, "user_id":user_id})
        db.session.commit()
        return True