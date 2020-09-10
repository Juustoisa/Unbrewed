from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["user_name"] = username
            return True
        else:
            return False

def get_one(id):
    sql = "SELECT username FROM users Where id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_list():
    sql = "SELECT U.username, U.id, COUNT(R.user_id) as total FROM users as U LEFT JOIN reviews as R ON U.id = R.user_id GROUP BY U.id ORDER BY total DESC" 
    result = db.session.execute(sql)
    return result.fetchall()

def get_profile(id):
    sql = "SELECT U.username, SUM(CASE WHEN R.teatype ='Green Tea' then 1 ELSE 0 END) as Green, SUM(CASE WHEN R.teatype ='Black Tea' then 1 ELSE 0 END) as Black, SUM(CASE WHEN R.teatype ='Oolong Tea' then 1 ELSE 0 END) as Oolong, SUM(CASE WHEN R.teatype ='Other Tea' then 1 ELSE 0 END) as Other, SUM(CASE WHEN R.teatype ='Pu-erh Tea' then 1 ELSE 0 END) as Pu_erh, SUM(CASE WHEN R.teatype ='White Tea' then 1 ELSE 0 END) as White FROM users as U INNER JOIN reviews as R ON U.id = R.user_id AND U.id=:id GROUP BY U.id" 
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def logout():
    del session["user_id"]
    del session["user_name"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)