from db import db
from flask import session
import user


def send(review_id, user_id):
    sql = "INSERT INTO likes (review_id, user_id) VALUES (:review_id, :user_id) ON CONFLICT DO NOTHING;"
    db.session.execute(sql, {"review_id":review_id, "user_id":user_id})
    db.session.commit()
    return True

def remove(review_id, user_id):
    if not review_id:
        return False
    if not user_id:
        return False
    sql = "DELETE FROM Likes WHERE review_id=:review_id AND user_id=:user_id"
    db.session.execute(sql, {"review_id":review_id, "user_id":user_id})
    db.session.commit()
    return True

def check_if_liked(review_id, user_id):
    sql = "SELECT * FROM likes WHERE review_id=:review_id AND user_id=:user_id"
    result = db.session.execute(sql, {"review_id":review_id, "user_id":user_id})
    exist = result.fetchone()

    if not exist: 
        return False
    return True
def get_likes_for_review(review_id):
    if not review_id:
        return False
    sql = "SELECT COUNT FROM likes Where review_id=:review_id"
    result = db.session.execute(sql, {"review_id":review_id})
    return result.fetchall()