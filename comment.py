from db import db
from flask import session
import user

def get_comments_on_review(id):
    sql = "SELECT comments.*, users.username FROM Comments JOIN users ON users.id = Comments.user_id WHERE Comments.review_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def send(review_id, user_id, commenttext):
    sql = "INSERT INTO comments (review_id, user_id, commenttext) VALUES (:review_id, :user_id, :commenttext)"
    db.session.execute(sql, {"review_id":review_id, "user_id":user_id, "commenttext":commenttext})
    db.session.commit()
    return True

def delete(delete_id,user_id):
    sql = "DELETE FROM comments WHERE id=:delete_id AND user_id=:user_id"
    db.session.execute(sql, {"delete_id":delete_id, "user_id":user_id})
    db.session.commit()
    return True