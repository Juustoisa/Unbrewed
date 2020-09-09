from db import db
import user


def get_list():
    sql = "SELECT R.id, R.name, R.score FROM reviews R ORDER BY r.id DESC LIMIT 10"
    result = db.session.execute(sql)
    return result.fetchall()

def get_one(id):
    sql = "SELECT * FROM reviews Where id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

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
    sql = "INSERT INTO reviews (name, shop, teatype, score, reviewtext, picture_url, user_id) VALUES (:name, :shop, :teatype, :score, :reviewtext, :picture_url, :user_id)"
    db.session.execute(sql, {"name":name, "shop":shop, "teatype":teatype, "score":score, "reviewtext":reviewtext, "picture_url":picture_url, "user_id":user_id})
    db.session.commit()
    return True