from db import db
import user


def get_list():
    sql = "SELECT R.id, R.name, R.score FROM reviews R ORDER BY r.score DESC LIMIT 15"
    result = db.session.execute(sql)
    return result.fetchall()

def get_search(chosentype,minscore,namesearch):
    namesearch = "%" + namesearch + "%"
    sql = "SELECT R.id, R.name, R.score FROM reviews R WHERE R.teatype IN :chosentype AND R.score >= :minscore AND R.name ILIKE :namesearch ORDER BY r.id DESC"
    result = db.session.execute(sql, {"chosentype":chosentype, "minscore":minscore, "namesearch":namesearch})
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
    sql = "SELECT * FROM reviews WHERE name=:name AND user_id=:user_id"
    doesItExist = db.session.execute(sql, {"user_id":user_id, "name":name})
    if doesItExist:
        sql = "UPDATE Reviews SET name = :name, shop = :shop, teatype = :teatype, score = :score, reviewtext = :reviewtext, picture_url = :picture_url, user_id = :user_id WHERE reviews.name = :name AND reviews.user_id = :user_id"
        db.session.execute(sql, {"name":name, "shop":shop, "teatype":teatype, "score":score, "reviewtext":reviewtext, "picture_url":picture_url, "user_id":user_id})
        db.session.commit()
        return True
    sql = "INSERT INTO reviews (name, shop, teatype, score, reviewtext, picture_url, user_id) VALUES (:name, :shop, :teatype, :score, :reviewtext, :picture_url, :user_id)"
    db.session.execute(sql, {"name":name, "shop":shop, "teatype":teatype, "score":score, "reviewtext":reviewtext, "picture_url":picture_url, "user_id":user_id})
    db.session.commit()
    return True

def delete(id, user_id):
        if not id:
            return False
        if not user_id:
            return False
        sql = "DELETE FROM Reviews WHERE id=:id AND user_id=:user_id"
        db.session.execute(sql, {"id":id, "user_id":user_id})
        db.session.commit()
        return True