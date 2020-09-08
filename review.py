from db import db
import user

def get_list():
    sql = "SELECT R.id, R.name, R.score FROM reviews R ORDER BY r.id DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_one(id):
    sql = "SELECT * FROM reviews Where id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def send(name, teatype, score, shop, reviewtext):
    user_id = user.user_id()
    if user_id == 0:
        return False
    if not name or not teatype or not score:
       return False
    if not shop:
        shop = "Unspecified"
    if not reviewtext:
        reviewtext = "Reviewer didn't provide a written review."
    sql = "INSERT INTO reviews (name, shop, teatype, score, reviewtext, user_id) VALUES (:name, :shop, :teatype, :score, :reviewtext, :user_id)"
    db.session.execute(sql, {"name":name, "shop":shop, "teatype":teatype, "score":score, "reviewtext":reviewtext, "user_id":user_id})
    db.session.commit()
    return True