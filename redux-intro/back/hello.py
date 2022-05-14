import json
import time
from flask import Flask, render_template, request, flash, session, jsonify, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'our_users'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_USER'] = 'root'

sql = MySQL(app)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    cursor = sql.connection.cursor()
 
    return "<h1>HOME PAGE</h1>"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userInfo = request.get_json()
        if userInfo.get('pass') != userInfo.get('confirm_pass'):
            res = { "result" : "false" }
            return jsonify({"result": res})
        cursor = sql.connection.cursor()
        passw = userInfo.get('confirm_pass')

        cursor.execute("INSERT INTO user(username, password, name, surname, birth_year, mail) " 
                    "VALUES ( %s, %s, %s, %s, %s, %s ) ", (userInfo.get('username'), passw, userInfo.get("name"), userInfo.get('surname'), userInfo.get("birth_year"), userInfo.get("mail")))
        
        #

        sql.connection.commit()

        
        cursor.execute( "SELECT user_ID from user WHERE username = %s", ([userInfo['username']]) )
        user = cursor.fetchone()
        ID = user[0]

        if userInfo.get('type') == "user":
            insert_user = "INSERT INTO slip_creator(creator_ID) VALUES ({0})".format(ID)
            cursor.execute(insert_user)
            sql.connection.commit()

            creator = cursor.fetchone()
            creator_ID = ID
            val = (creator_ID, 0, 0, False)
            cursor.execute("INSERT INTO bet_slip(creator_ID, bet_count, total_amount, isPlayed) VALUES (%s, %s, %s, %s)", (val))   
            
            sql.connection.commit()
            
            val = (ID, 0, 0, userInfo['address'], 0)
            cursor.execute("INSERT INTO normal_user(n_user_ID, balance, winning_cnt, address, coupons) VALUES ( %s, %s, %s, %s, %s)", (val))
            sql.connection.commit()
            
        if userInfo.get('type') == "editor":
            insert_editor = "INSERT INTO editor_request(editor_ID, status) VALUES({0}, {1})".format(ID, "PENDING")
            cursor.execute(insert_editor)
            sql.connection.commit()

        result = {
            "success": "true",
            "type": userInfo.get('type'),
            "user_ID": ID,
            "username": userInfo.get('username')
        }
        return jsonify({"result": result})

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        userInfo = request.get_json()
        cursor = sql.connection.cursor()
        value = cursor.execute("SELECT * FROM user WHERE username = %s", ([userInfo['username']]))
        if value > 0:
            user = cursor.fetchone()
            if user[2] == userInfo['password']:
                normal_user = cursor.execute("SELECT * FROM normal_user WHERE n_user_id = %s", ([user[0]]))
                normal_users = cursor.fetchone()
                if normal_user > 0:
                    ban = cursor.execute("SELECT * FROM banned_users WHERE n_user_id = %s", ([normal_users[0]]))
                    if ban > 0:
                        result = {
                            "success" : "false",
                            "ban" : "true"
                        }
                    else:
                        type = "user"
                        result = {
                            "success" : "true",
                            "type" : type,
                            "user_id" : normal_users[0],
                            "username" : userInfo['username'],
                            "balance" : normal_users[1]
                        }    
                else:
                    editor = cursor.execute("SELECT editor_ID FROM editor WHERE editor_ID = %s", ([user[0]]))
                    if editor > 0:
                        editorBan = cursor.execute("SELECT * FROM banned_editors WHERE editor_ID = %s", ([normal_users[0]]))
                        if editorBan > 0:
                            result = {
                                "success" : "false",
                                "ban" : "true"
                            }
                        else:
                            type = "editor"
                            result = {
                                "success" : "true",
                                "type" : type,
                                "editor_ID" : user[0],
                                "username" : userInfo['username']
                         }
                    else:
                        admin = cur.execute("SELECT admin_ID FROM admin WHERE admin_ID = %s", ([user[0]]))
                        if admin > 0:
                            type = "admin"
                            result = {
                                "success" : "true",
                                "type" : type,
                                "user_id" : user[0],
                                "username" : userInfo['username']
                            }
                        else:
                            result = {
                                "success" : "false",
                                "pending" : "true"
                            }
        else:
            result = {
                "success" : "false",
                "ban" : "false"
            }         
        return jsonify({"result" : result})

app.run(debug=True)