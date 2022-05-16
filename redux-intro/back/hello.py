import json
import time
from unittest import result
from flask import Flask, render_template, request, flash, session, jsonify, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
from random import randint


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
 
    info = request.get_json(force=True)

    if info["request-type"] == "filter":

        #Check this after
        if info["filter"]["sort_type"] == "popularity":

            popularity_query = "WITH active_bets AS ( SELECT bet_ID, match_ID FROM bet WHERE active = TRUE), all_played_bets AS ( SELECT * FROM placed_on NATURAL JOIN bet_slip NATURAL JOIN active_bets WHERE isPlayed = TRUE) SELECT bet_ID, match_ID, Count(bet_slip_ID) AS played_cnt FROM all_played_bets GROUP BY bet_ID, match_ID"
            popularity = cursor.execute(popularity_query)
            if popularity > 0:

                popularity_cols = [col[0] for col in cursor.description]

                pop_results = []

                for r in cursor.fetchall():
                    pop_results.append( dict( zip( popularity_cols, r ) ) )
            else:
                return { "status" : "Popularity query failed" }
        if len( info["filter"]["contest"] ) == 0:
            cursor.execute("SELECT name FROM contest")
            tmp = cursor.fetchall()
            contest = tuple([contest[0] for contest in tmp])
        else:
            contest = tuple(info["filter"]["contest"])
        #contest = tuple(info["filter"]["contest"])
        search_text = '\'' + info["filter"]["search_text"] + '%\''

        values = (info["filter"]["sport_name"], info["filter"]["max_mbn"], info["filter"], contest, search_text, search_text, search_text)
        filter_query = "WITH s_filter AS ( SELECT match_ID from matches WHERE sport_name = %s), " \
                        "b_filter AS (SELECT match_ID FROM bet WHERE active = TRUE AND mbn <= %s), " \
                        "c_filter AS (SELECT match_ID FROM matches NATURAL JOIN contest WHERE contest.name IN %s), " \
                        "esport_filter AS (SELECT match_ID FROM plays NATURAL JOIN esports_team WHERE team_name LIKE %s), " \
                        "team_filter AS (SELECT match_ID FROM plays NATURAL JOIN team WHERE team_name LIKE %s), " \
                        "competitor_union AS (SELECT match_ID FROM esport_filter UNION TABLE team_filter), "\
                        "final_filter AS (SELECT DISTINCT match_ID FROM s_filter INNER JOIN b_filter USING(match_ID) INNER JOIN c_filter USING(match_ID) INNER JOIN c_filter USING(match_ID) " \
                        "INNER JOIN competitor_union USING(match_ID))"
        continuing_filter = filter_query + ", data AS (SELECT * FROM final_filter NATURAL JOIN matches), " \
                            "all_competitors AS (SELECT name, id FROM (SELECT competitor_ID AS id, name AS name FROM esports_team) AS tmp UNION (SELECT competitor_ID AS id, team_name AS name FROM team)), " \
                            "curr_competitors AS (SELECT competitor_ID as id, side, match_ID FROM plays NATURAL JOIN final_filter), " \
                            "all_side AS (SELECT name, side, match_ID FROM all_competitors NATURAL JOIN curr_competitors), " \
                            "b_data AS (SELECT * FROM bet NATURAL JOIN final_filter WHERE active = TRUE AND result = 'PENDING') SELECT * FROM data NATURAL JOIN b_data NATURAL JOIN all_side"

        apply_filter = cursor.execute(continuing_filter, values)
        if apply_filter:

            match_cols = [col[0] for col in cursor.description]
            match_res = []

            for r in cursor.fetchall():
                match_res.append( dict( zip( match_cols, r ) ) )
            
            matches = []
            for r in match_res:
                already_added = False
                m_found = False

                if r["side"] == "HOME":
                    home_side = r["competitor_name"]
                    away_side = ""
                else:
                    home_side = ""
                    away_side = r["competitor_name"]

                total_ratio = r["ratio"]
                for m in matches:
                    if m["match_ID"] == r["match_ID"]:
                        m_found = True
                        for b in m["bets"]:
                            if b["bet_ID"] == r["bet_ID"]:
                                already_added = True
                            if b["home_side"] == "":
                                b["home_side"] = r["name"]
                            else:
                                b["away_side"] = r["name"]
                        if not already_added:
                            added_bet = {
                                "bet_ID" : r["bet_ID"],
                                "home_side" : home_side,
                                "away_side" : away_side,
                                "ratio" : total_ratio,
                                "mbn" : r["mbn"],
                                "p_cnt" : 0,
                                "old_ratio" : "",
                                "bet_type" : r["bet_type"]
                            }

                            if info["filter"]["sort_type"] == "popularity":
                                for b in pop_results:
                                    if b["match_ID"] == m["match_ID"] and b["bet_ID"] == r["bet_ID"]:
                                        added_bet["p_cnt"] = b["played_cnt"]

                            m["bets"].append(added_bet)
                
                if not m_found:
                    bets = [{
                        "bet_ID" : r["bet_ID"],
                        "home_side" : home_side,
                        "away_side" : away_side,
                        "ratio" : total_ratio,
                        "mbn" : r["mbn"], 
                        "p_cnt" : 0,
                        "old_ratio" : "",
                        "bet_type" : r["bet_type"]
                    }]

                    if info["filter"]["sort_type"] == "popularity":
                        for b in pop_results:
                            if b["match_ID"] == r["match_ID"] and b["bet_ID"] == r["bet_ID"]:
                                bets[0]["p_cnt"] = b["played_cnt"]
                    matches.append({
                        "match_ID" : r["match_ID"],
                        "match_start_date" : r["start_date"],
                        "bets" : bets
                    })
            old_ratio_query = filter_query + "SELECT match_ID, bet_ID, bet_type, MAX(change_date) AS change_date, ratio FROM (SELECT * " \
                                "FROM bet NATURAL JOIN final_filter WHERE active = FALSE) AS inactives GROUP BY match_ID, bet_ID, bet_type, ratio"
            execute_old_ratio = cursor.execute(old_ratio_query)
            if execute_old_ratio:
                old_ratio_col = [col[0] for col in cursor.description]
                old_ratio_res = []

                for r in cursor.fetchall():
                    old_ratio_res.append( dict( zip( old_ratio_col, r) ) )
                for m in matches:
                    for old_ratio in old_ratio_res:
                        if old_ratio["match_ID"] == m["match_ID"]:
                            for b in m["bets"]:
                                if old_ratio["bet_type"] == b["bet_type"]:
                                    b["old_ratio"] = old_ratio["ratio"]
                return {
                    "matches" : matches,
                }
    elif info["request-type"] == "play_betslip":
        value = (info["username"])
        search_user_query = "SELECT user_ID FROM user WHERE username = %s"
        execute_search = cursor.execute(search_user_query, value)
        if execute_search:
            user_ID = cursor.fetchone()[0]
            value = (user_ID)
            check_mbn_query = "WITH user_bet_slip AS (SELECT bet_slip_ID FROM bet_slip WHERE creator_ID = %s AND isPlayed = FALSE, " \
                            "current_bets AS (SELECT * FROM user_bet_slip NATURAL JOIN bet), " \
                            "current_cnt_bet AS (SELECT COUNT(bet_slip_ID) AS bet_cnt FROM current_bets), " \
                            "max_mbn_cnt AS (SELECT MAX(mbn) AS max_mbn FROM current_bets) " \
                            "SELECT CASE WHEN current_cnt_bet.bet_cnt < max_mbn_cnt.max_mbn THEN 'MBN_NOT_OK' " \
                            "WHEN current_cnt_bet.bet_cnt >= max_mbn_cnt.max_mbn THEN 'MBN_OK' " \
                            "END AS response FROM current_bet_cnt, max_mbn_cnt"
            execute_check = cursor.execute(check_mbn_query, value)
            if execute_check:
                mbn_res = cursor.fetchone()[0]
                if mbn_res == "MBN_OK":
                    value = (info["total_amount"], info["total_amount"], user_ID)
                    check_balance_query = "SELECT CASE WHEN normal_user.balance < %s THEN 'Insufficient funds' " \
                                        "WHEN normal_user.balance > %s THEN 'Sufficient funds' " \
                                        "END AS response FROM normal_user WHERE n_user_ID = %s"
                    execute_check = cursor.execute(check_balance_query, value)
                    if execute_check:
                        balance_res = cursor.fetchone()[0]
                        if balance_res == "Sufficient funds":
                            select_bet_slip_query = "SELECT bet_slip_ID FROM bet_slip WHERE isPlayed = FALSE AND creator_ID = %s"
                            value = (user_ID)
                            execute_select = cursor.execute(select_bet_slip_query, value)
                            if execute_select:
                                played_slip_ID = cursor.fetchone()[0]
                                update_slip_query = "UPDATE bet_slip SET total_amount = %s, isPlayed = TRUE WHERE creator_ID = %s AND bet_slip_ID = %s"
                                value = (info["total_amount"], user_ID, played_slip_ID)
                                execute_update = cursor.execute(update_slip_query, value)
                                if execute_update:
                                    update_balance_query = "UPDATE normal_user SET balance = normal_user.balance - %s WHERE n_user_ID = %s"
                                    value = (info["total_amount"], user_ID)
                                    execute_b_update = cursor.execute(update_balance_query, value)
                                    if execute_b_update:
                                        insert_bet_slip_query = "INSERT INTO bet_slip (creator_ID, bet_count, total_amount, isPlayed) VALUES (%s, 0, 0, FALSE)"
                                        value = (user_ID)
                                        execute_insert = cursor.execute(insert_bet_slip_query, value)
                                        if execute_insert:
                                            share_slip_query = "INSERT INTO shared_slip (bet_slip_ID, sharer_ID) VALUES (%s, %s)"
                                            value = (played_slip_ID, user_ID)
                                            execute_share = cursor.execute(share_slip_query, value)
                                            if execute_share:
                                                sql.connection.commit()
                                                return {"status" : "success"}
                                            else:
                                                return {"status" : "share_failed"}
                                        else:
                                            return {"status" : "insert_slip_failed"}
                                    else:
                                        return {"status" : "update_balance_failed"}
                                else:
                                    return {"status" : "update_slip_failed"}
                            else:
                                return {"status" : "select_bet_slip_failed"}
                        else:
                            return {"status" : "insufficient_funds"}
                    else:
                        return {"status" : "balance_check_failed"}
                else:
                    return {"status" : "mbn_not_ok"}
            else:
                return {"status" : "MBN_check_failed"}
        else:
            return {"status" : "User_not_found"}
    elif info["request_type"] == "editor_share_betslip":
        print("Editor Share Bet")
    elif info["request_type"] == "suggest_bet":
        print(" Suggest Bet")
    elif input["request_type"] == "add_bet_to_betslip":
        print(" Add Bet")
    elif input["request_type"] == "remove_bet_from_betslip":
        print(" Remove Bet")
    elif input["request_type"] == "display_user_bet_slip":
        print(" Display")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userInfo = request.get_json()
        if userInfo.get('pass') != userInfo.get('confirm_pass'):
            res = { "result" : "false" }
            return jsonify({"result": res})
        cursor = sql.connection.cursor()
        passw = userInfo.get('confirm_pass')

        val = (userInfo.get('username'), passw, userInfo.get("name"), userInfo.get('surname'), userInfo.get("birth_year"), userInfo.get("mail"))
        cursor.execute("INSERT INTO user(username, password, name, surname, birth_year, mail) VALUES ( %s, %s, %s, %s, %s, %s ) ", val)
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
            cursor.execute("INSERT INTO bet_slip(creator_ID, bet_count, total_amount, isPlayed) VALUES (%s, %s, %s, %s)", val)   
            sql.connection.commit()
            
            val = (ID, 0, 0, userInfo['address'], 0)
            cursor.execute("INSERT INTO normal_user(n_user_ID, balance, winning_cnt, address, coupons) VALUES ( %s, %s, %s, %s, %s)", val)
            sql.connection.commit()
            
        if userInfo.get('type') == "editor":
            insert_user = "INSERT INTO slip_creator(creator_ID) VALUES ({0})".format(ID)
            cursor.execute(insert_user)
            sql.connection.commit()

            creator_ID = ID
            val = (creator_ID, 0, 0, False)
            cursor.execute("INSERT INTO bet_slip(creator_ID, bet_count, total_amount, isPlayed) VALUES (%s, %s, %s, %s)", val)   
            sql.connection.commit()

            val = (ID, 0, 0)
            cursor.execute("INSERT INTO editor(editor_ID, win_rate, winning_cnt) VALUES( %s , %s, %s)", val)

            val = (ID, "PENDING")
            cursor.execute("INSERT INTO editor_request(editor_ID, status) VALUES( %s , %s)", val)
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
            if user[2] == userInfo['pass']:
                normal_users_list = cursor.execute("SELECT * FROM normal_user WHERE n_user_ID = %s", ([user[0]]))
                normal_user = cursor.fetchone()
                if normal_users_list > 0:
                    banned_user = cursor.execute("SELECT * FROM banned_users WHERE n_user_ID = %s", ([normal_user[0]]))
                    if banned_user > 0:
                        result = {
                            "success" : "false",
                            "ban" : "true"
                        }
                        return jsonify({"result" : result})
                    else:
                        type = "user"
                        result = {
                            "success" : "true",
                            "type" : type,
                            "user_ID" : normal_user[0],
                            "username" : userInfo['username'],
                            "balance" : normal_user[1],
                            "winning_cnt" : normal_user[2],
                            "address" : normal_user[3],
                            "coupons" : normal_user[4]
                        }  
                        return jsonify({"result" : result})  
                else:
                    editor_request = cursor.execute("SELECT * FROM editor_request WHERE editor_ID = %s", ([user[0]]))
                    e_request = cursor.fetchone()
                    if editor_request > 0:
                        if e_request[1] == 'PENDING':
                            result = {
                                "success" : "false",
                                "ban" : "false"
                            }
                            return jsonify({"result" : result})
                        else:
                            editorBan = cursor.execute("SELECT * FROM banned_editors WHERE editor_ID = %s", ([user[0]]))
                            if editorBan > 0:
                                result = {
                                    "success" : "false",
                                    "ban" : "true"
                                }
                                return jsonify({"result" : result})
                            else:
                                editor = cursor.execute("SELECT * FROM editor WHERE editor_ID = %s", ([user[0]]))
                                editor = cursor.fetchone()
                                type = "editor"
                                result = {
                                    "success" : "true",
                                    "type" : type,
                                    "editor_ID" : editor[0],
                                    "username" : userInfo['username'],
                                    "win_rate" : editor[1],
                                    "winning_cnt" : editor[2]
                                } 
                                return jsonify({"result" : result})
                    else:
                        admin = cursor.execute("SELECT admin_ID FROM admin WHERE admin_ID = %s", ([user[0]]))
                        if admin > 0:
                            type = "admin"
                            result = {
                                "success" : "true",
                                "type" : type,
                                "user_id" : user[0],
                                "username" : userInfo['username']
                            }
                            return jsonify({"result" : result})
                        else:
                            result = {
                                "success" : "false",
                                "ban" : "false"
                            }
                            return jsonify({"result" : result})
            else:
                result = {
                    "success" : "false",
                    "ban" : "false"
                }
                return jsonify({"result" : result})
        else:
            result = {
                "success" : "false",
                "ban" : "false"
            }         
        return jsonify({"result" : result})

@app.route('/admin/manage-editors', methods=['GET', 'POST'])
def manage_editors():
    cursor = sql.connection.cursor()

    info = request.get_json(force=True)

    if info['request-type'] == "display_requests":
        display_query = "SELECT user_ID, username, name, surname FROM editor_request AS e INNER JOIN user AS u ON e.editor_ID = u.user_ID WHERE status = 'PENDING' "
        cursor.execute(display_query)

        editor_list = []
        editor_cols = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            editor_list.append(dict(zip(editor_cols, row)))

        return{"editor-requests": editor_list}

    elif info['request-type'] == "display_editor_info":
        editor_query = "SELECT username, name, surname, mail FROM editor_request AS e INNER JOIN user AS u ON e.editor_ID = u.user_ID WHERE status = 'PENDING' AND u.user_ID = {0}".format(info['user_ID'])
        editors = cursor.execute( editor_query )
        if editors > 0:
            editor_info = []
            editor_cols = [col[0] for col in cursor.description]
            
            for r in cursor.fetchall():
                editor_info.append( dict( zip( editor_cols, r ) ) )
            return {"editor": editor_info[0]}
            
        else:
            return {"status" : "Editor request is not found in db"}
    
    elif info['request-type'] == "approve_request":

        approve_query = "UPDATE editor_request SET status = 'APPROVED' WHERE editor_ID = {0}".format(info["user_ID"])
        approve = cursor.execute(approve_query)
        if approve > 0:
            sql.connection.commit()
            return {"status" : "Success"}
        else:
            return {"status" : "Update failed"}

    elif info["request-type"] == "decline_request":
        
        delete_request = "DELETE FROM editor_request WHERE editor_ID = {0}".format(info["user_ID"])
        delete_success = cursor.execute(delete_request)
        if delete_success > 0:
            delete_editor = "DELETE FROM editor WHERE editor_ID = {0}".format(info["user_ID"])
            delete_success = cursor.execute(delete_editor)
            if delete_success > 0:
                delete_slip = "DELETE FROM bet_slip WHERE creator_ID = {0}".format(info["user_ID"])
                delete_success = cursor.execute(delete_slip)
                if delete_success > 0:
                    delete_creator = "DELETE FROM slip_creator WHERE creator_ID = {0}".format(info["user_ID"])
                    delete_success = cursor.execute(delete_creator)
                    if delete_success > 0:
                        delete_user = "DELETE FROM user WHERE user_ID = {0}".format(info['user_ID'])
                        delete_success = cursor.execute(delete_user)
                        if delete_success > 0:
                            return { "status" : "success" }
                        else:
                            return { "status" : "Could not delete user" }
                    else:
                        return { "status" : "Could not delete slip creator" }
                else:
                    return { "status" : "Could not delete bet slip" }
            else:
                return { "status" : "Could not delete editor" }
        else:
            return { "status" : "Could not delete request" }
            
    
@app.route('/admin/ban-users', methods=['GET', 'POST'])
def ban_users():
    cursor = sql.connection.cursor()

    info = request.get_json(force=True)

    if info['request_type'] == "search_user":

        search_query = "SELECT user_ID, username FROM user WHERE username LIKE {0}".format('\'' + info["username"] + '%\'')
        cursor.execute(search_query)

        user_results = []
        username_cols = [col[0] for col in cursor.description]

        for r in cursor.fetchall():
            user_results.append( dict( zip( username_cols, r ) ) )
            
        return { "users" : user_results }
    
    elif info['request_type'] == "display_user":
        cursor.execute("SELECT * FROM user WHERE username = %s", ([info["username"]]))
        search_user = cursor.fetchone()
        search_normal_user = cursor.execute("SELECT * FROM normal_user WHERE n_user_ID = %s", ([search_user[0]]))
        if search_normal_user > 0:

            select_query = "SELECT n_user_ID, username, name, surname, birth_year, mail, balance, winning_cnt, address, coupons FROM normal_user as n INNER JOIN user as u ON n.n_user_ID = u.user_ID WHERE n.n_user_ID = {0}".format(search_user[0])
            cursor.execute(select_query)

            val = cursor.fetchall()
            user_des = []

            for r in val:
                isBanned = cursor.execute("SELECT n_user_ID FROM banned_users WHERE n_user_ID = {0}".format(r[0]))
                if isBanned:
                    user = [{
                        "banned": True,
                        "username": val[1], 
                        "name": val[2],
                        "surname": val[3],
                        "birth_year": val[4],
                        "mail": val[5],
                        "balance": val[6],
                        "winning_cnt": val[7],
                        "address": val[8],
                        "coupons": val[9]
                    }]
                else:
                    user = [{
                        "banned": False,
                        "username": val[1], 
                        "name": val[2],
                        "surname": val[3],
                        "birth_year": val[4],
                        "mail": val[5],
                        "balance": val[6],
                        "winning_cnt": val[7],
                        "address": val[8],
                        "coupons": val[9]
                    }]
                user_des.append(user)
            
            result = { "user_info" : user_des }
        
        else:
            search_editor = cursor.execute("SELECT * FROM editor WHERE editor_ID = %s", ([search_user[0]]))
            if search_editor > 0:
                select_query = "SELECT editor_ID, username, win_rate, winning_cnt FROM editor as e INNER JOIN user as u ON e.editor_ID = u.user_ID WHERE e.editor_ID = {0}".format(search_user[0])
                cursor.execute(select_query)
                val = cursor.fetchall()
                user_des = []

                for r in val:
                    isBanned = cursor.execute("SELECT editor_ID FROM banned_editors WHERE editor_ID = {0}".format(r[0]))
                    if isBanned:
                        user = [{
                            "banned": True,
                            "username": val[1], 
                            "win_rate": val[2],
                            "winning_cnt": val[3]
                        }]
                    else:
                        user = [{
                            "banned": True,
                            "username": val[1], 
                            "win_rate": val[2],
                            "winning_cnt": val[3]
                        }]
                    user_des.append(user)
            
                result = { "user_info" : user_des }
            else:
                result = {}
            return jsonify({"result": result})

    elif info['request_type'] == "ban_user":
        search_normal_user = cursor.execute("SELECT * FROM normal_user WHERE n_user_ID = %s", ([info["user_ID"]]))
        if search_normal_user > 0:
            val = (info["admin_ID"], info["user_ID"])
            ban_query = "INSERT INTO banned_users (admin_ID, n_user_ID) VALUES ( %s, %s )"
            ban_user = cursor.execute(ban_query, val)
            
            if ban_user > 0:
                sql.connection.commit()
                return {"status": "success"}
            else:
                return {"status": "Ban failed"}
        else:
            search_editor = cursor.execute("SELECT * FROM editor WHERE n_user_ID = %s", ([info["user_ID"]]))
            
            if search_editor > 0:
                ban_query = "INSERT INTO banned_editors (admin_ID, editor_ID) VALUES ({0}, {1})".format(info["admin_ID"], info["user_ID"])
                ban_user = cursor.execute(ban_query)
                
                
                if ban_user > 0:
                    sql.connection.commit()
                    return {"status": "success"}
                else:
                    return {"status": "Ban failed"}
            else:
                return {"status": "User could not be found"}
    
    elif info['request_type'] == "remove_ban":
        search_normal_user = cursor.execute("SELECT * FROM normal_user WHERE n_user_ID = %s", ([info["user_ID"]]))
        if search_normal_user > 0:
            ban_query = "DELETE FROM banned_users WHERE n_user_ID = {1}".format(info["user_ID"])
            ban_user = cursor.execute(ban_query)
            
            if ban_user > 0:
                sql.connection.commit()
                return {"status": "success"}
            else:
                return {"status": "Ban failed"}
        else:
            search_editor = cursor.execute("SELECT * FROM editor WHERE n_user_ID = %s", ([info["user_ID"]]))
            if search_editor > 0:
                ban_query = "DELETE FROM banned_editors WHERE editor_ID = {1}".format(info["user_ID"])
                ban_user = cursor.execute(ban_query)
                if ban_user > 0:
                    sql.connection.commit()
                    return {"status": "success"}
                else:
                    return {"status": "Ban failed"}
            else:
                return {"status": "User could not be found"}
        

@app.route('/admin/edit-bets', methods=['GET', 'POST'])
def admin_edit_bets():
    cursor = sql.connection.cursor()

    info = request.get_json(force=True)

    if info["request_type"] == "change_bet":

        values = (info["bet_ID"], info["match_ID"])
        bet_search_query = "SELECT bet_type, mbn FROM bet WHERE bet_ID = %s AND match_ID = %s"
        existedBet = cursor.execute(bet_search_query, values)
        if existedBet > 0:
            bet = cursor.fetchone()

            bet_type = bet[0]
            mbn = bet[1]

            values = (info["bet_ID"], info["match_ID"])
            deactivate_bet = "UPDATE bet SET active = FALSE WHERE bet_ID = %s AND match_ID = %s"
            deactivation = cursor.execute(deactivate_bet, values)
            if deactivation > 0:
                sql.connection.commit()

                values = (info["bet_ID"], info["match_ID"], mbn, info["new_ratio"], bet_type)
                update_bet_query = "INSERT INTO bet (bet_ID, match_ID, mbn, ratio, change_date, bet_type, active, result) VALUES (%s, %s, %s, %s, NOW(), %s, TRUE, 'PENDING') "
                update_bet = cursor.execute(update_bet_query, values)

                if update_bet > 0:
                    sql.connection.commit()
                    return {"status" : "success"}
                else:
                    return {"status" : "Ratio could not be added"}
            else:
                return {"status" : "Failed to deactivate"}
        else:
            return {"status" : "No bet exists with this ID"}

    elif info["request_type"] == "remove_bet":

        values = (info["bet_ID"], info["match_ID"])
        deactivate_bet = "UPDATE bet SET active = FALSE WHERE bet_ID = %s AND match_ID = %s"
        deactivation = cursor.execute(deactivate_bet, values)
        if deactivation > 0:
                sql.connection.commit()
                return {"status" : "success"}
        else:
            return {"status" : "Bet could not be cancelled"}

    elif input["request_type"] == "insert_bet":

        search_unfinished_matches = "SELECT m.match_ID, m.sport_name FROM matches m WHERE NOT EXISTS ( SELECT match_ID FROM matches NATURAL JOIN results WHERE m.match_ID = match_ID)"
        unfinished_match = cursor.execute(search_unfinished_matches)
        if unfinished_match > 0:
            unfinished_matches = []

            unfinished_matches_columns = [column[0] for column in cursor.description]
        
            unfinished_match_tuple = cursor.fetchall()
        
            for r in unfinished_match_tuple:
                unfinished_matches.append( dict( zip( unfinished_matches_columns, r ) ) )

            for r in unfinished_matches:

                if r["sport_name"] == "FOOTBALL":
                    home_half_score = 0
                    away_half_score = 0

                    home_score = randint(0,8)
                    away_score = randint(0,8)

                    yellow_card = randint(0,9)
                    red_card = randint(0,5)

                    corner_cnt = randint(0,15)

                    if home_score > 0:
                        home_half_score = randint(0,home_ft_score)

                    if away_score > 0:
                        away_half_score = randint(0,away_ft_score)

                    values = (r["match_ID"], home_score, away_score)
                    result_query = "INSERT INTO results (match_ID, home_score, away_acore) VALUES (%s, %s, %s) "

                    match_result = cursor.execute(result_query, values)

                    if match_result > 0:
                        cursor.execute("SELECT LAST_INSERT_ID()")

                        last_result_ID = cursor.fetchone()[0]

                        values = ( last_result_ID, yellow_card, red_card, corner_cnt, home_half_score, away_half_score )
                        result_query = "INSERT INTO football_results (f_result_ID, yellow_card_num, red_card_num, corner_count, first_half_home_goals, first_half_away_goals) VALUES (%s, %s, %s, %s, %s, %s)"

                        match_result = cursor.execute(result_query, values)
                        if match_result > 0:
                            sql.connection.commit()

                        else:
                            return {"status": "Football result insertion failed"}

                    else:
                        return {"status": "Result insertion failed"}

                elif r["sport_name"] == "BASKETBALL":
                    home_half_score = 80
                    away_half_score = 80

                    home_score = randint(80, 125)
                    away_score = randint(80, 125)

                    home_total_rebound_count = randint(0,30)
                    away_total_rebound_count = randint(0,30)

                    if home_score > 80:
                        home_half_score = randint(40, home_score-1)

                    if away_score > 80:
                        away_half_score = randint(40, away_score-1)

                    values = (r["match_ID"], home_score, away_score)
                    result_query = "INSERT INTO results (match_ID, home_score, away_acore) VALUES (%s, %s, %s) "

                    match_result = cursor.execute(result_query, values)

                    if match_result > 0:
                        cursor.execute("SELECT LAST_INSERT_ID()")

                        last_result_ID = cursor.fetchone()[0]

                        values = ( last_result_ID, home_half_score, away_half_score, home_total_rebound_count, away_total_rebound_count )
                        result_query = "INSERT INTO basketball_results (b_result_ID, home_half_score, away_half_score, home_total_rebound_score, away_total_rebound_score) VALUES (%s, %s, %s, %s, %s)"

                        match_result = cursor.execute(result_query, values)
                        if match_result > 0:
                            sql.connection.commit()

                        else:
                            return {"status": "Basketball result insertion failed"}

                    else:
                        return {"status": "Result insertion failed"}
                
                elif r['sport_name'] == 'VOLLEYBALL':
                    home_score = randint(0,3)
                    away_score = 0
                    scores = []
                    if home_score == 3:
                        away_score = randint(0,2)
                        if away_score == 0:
                            for i in range(3):
                                isLongSet = randint(0,1)
                                if isLongSet:
                                    home_set_score = randint(26,30)
                                    away_set_score = randint(25,home_set_score-1)
                                    scores.append(home_set_score, away_set_score)
                                else:
                                    home_set_score = 25
                                    away_set_score = randint(23)
                                    scores.append(home_set_score, away_set_score)
                        elif away_score == 1:
                            away_set_win = 0
                            home_set_win = 0
                            for i in range(4):
                                set_winner = randint(0,1)
                                isLongSet = randint(0,1)
                                if set_winner == 0:
                                    if home_set_win < 3:
                                        home_set_win += 1
                                        if isLongSet:
                                            home_set_score = randint(26,30)
                                            away_set_score = randint(25,home_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            home_set_score = 25
                                            away_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    elif away_set_win < 1:
                                        away_set_win += 1
                                        if isLongSet:
                                            away_set_score = randint(26,30)
                                            home_set_score = randint(25,away_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            away_set_score = 25
                                            home_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    else:
                                        continue
                                else:
                                    if away_set_win < 1:
                                        away_set_win += 1
                                        if isLongSet:
                                            away_set_score = randint(26,30)
                                            home_set_score = randint(25,away_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            away_set_score = 25
                                            home_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    elif home_set_win < 3:
                                        home_set_win += 1
                                        if isLongSet:
                                            home_set_score = randint(26,30)
                                            away_set_score = randint(25,home_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            home_set_score = 25
                                            away_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    else:
                                        continue
                        else:
                            away_set_win = 0
                            home_set_win = 0
                            for i in range(5):
                                set_winner = randint(0,1)
                                isLongSet = randint(0,1)
                                if set_winner == 0:
                                    if home_set_win < 3:
                                        home_set_win += 1
                                        if isLongSet:
                                            home_set_score = randint(26,30)
                                            away_set_score = randint(25,home_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            home_set_score = 25
                                            away_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    elif away_set_win < 2:
                                        away_set_win += 1
                                        if isLongSet:
                                            away_set_score = randint(26,30)
                                            home_set_score = randint(25,away_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            away_set_score = 25
                                            home_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    else:
                                        continue
                                else:
                                    if away_set_win < 2:
                                        away_set_win += 1
                                        if isLongSet:
                                            away_set_score = randint(26,30)
                                            home_set_score = randint(25,away_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            away_set_score = 25
                                            home_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    elif home_set_win < 3:
                                        home_set_win += 1
                                        if isLongSet:
                                            home_set_score = randint(26,30)
                                            away_set_score = randint(25,home_set_score-1)
                                            scores.append(home_set_score, away_set_score)
                                        else:
                                            home_set_score = 25
                                            away_set_score = randint(23)
                                            scores.append(home_set_score, away_set_score)
                                    else:
                                        continue
                    elif home_score == 2:
                        away_score = 3
                        away_set_win = 0
                        home_set_win = 0
                        for i in range(5):
                            set_winner = randint(0,1)
                            isLongSet = randint(0,1)
                            if set_winner == 0:
                                if home_set_win < 2:
                                    home_set_win += 1
                                    if isLongSet:
                                        home_set_score = randint(26,30)
                                        away_set_score = randint(25,home_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        home_set_score = 25
                                        away_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                elif away_set_win < 3:
                                    away_set_win += 1
                                    if isLongSet:
                                        away_set_score = randint(26,30)
                                        home_set_score = randint(25,away_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        away_set_score = 25
                                        home_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                else:
                                    continue
                            else:
                                if away_set_win < 3:
                                    away_set_win += 1
                                    if isLongSet:
                                        away_set_score = randint(26,30)
                                        home_set_score = randint(25,away_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        away_set_score = 25
                                        home_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                elif home_set_win < 2:
                                    home_set_win += 1
                                    if isLongSet:
                                        home_set_score = randint(26,30)
                                        away_set_score = randint(25,home_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        home_set_score = 25
                                        away_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                else:
                                    continue
                    elif home_score == 1:
                        away_score = 3
                        away_set_win = 0
                        home_set_win = 0
                        for i in range(4):
                            set_winner = randint(0,1)
                            isLongSet = randint(0,1)
                            if set_winner == 0:
                                if home_set_win < 1:
                                    home_set_win += 1
                                    if isLongSet:
                                        home_set_score = randint(26,30)
                                        away_set_score = randint(25,home_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        home_set_score = 25
                                        away_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                elif away_set_win < 3:
                                    away_set_win += 1
                                    if isLongSet:
                                        away_set_score = randint(26,30)
                                        home_set_score = randint(25,away_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        away_set_score = 25
                                        home_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                else:
                                    continue
                            else:
                                if away_set_win < 3:
                                    away_set_win += 1
                                    if isLongSet:
                                        away_set_score = randint(26,30)
                                        home_set_score = randint(25,away_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        away_set_score = 25
                                        home_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                elif home_set_win < 1:
                                    home_set_win += 1
                                    if isLongSet:
                                        home_set_score = randint(26,30)
                                        away_set_score = randint(25,home_set_score-1)
                                        scores.append(home_set_score, away_set_score)
                                    else:
                                        home_set_score = 25
                                        away_set_score = randint(23)
                                        scores.append(home_set_score, away_set_score)
                                else:
                                    continue
                    else:
                        away_score = 3
                        for i in range(3):
                            isLongSet = randint(0,1)
                            if isLongSet:
                                away_set_score = randint(26,30)
                                home_set_score = randint(25,away_set_score-1)
                                scores.append(home_set_score, away_set_score)
                            else:
                                away_set_score = 25
                                home_set_score = randint(23)
                                scores.append(home_set_score, away_set_score)
                    home_total = 0
                    away_total = 0
                    for i in range(len(scores)):
                        if i % 2 == 0:
                            home_total += scores[i]
                        else:
                            away_total += scores[i]
                    
                    total_score = home_total + away_total

                    values = (r["match_ID"], home_score, away_score)
                    result_query = "INSERT INTO results (match_ID, home_score, away_acore) VALUES (%s, %s, %s) "

                    match_result = cursor.execute(result_query, values)
                    if match_result > 0:
                        cursor.execute("SELECT LAST_INSERT_ID()")

                        last_result_ID = cursor.fetchone()[0]

                        values = ( last_result_ID, total_score, home_total, away_total )
                        result_query = "INSERT INTO volleyball_results (v_result_ID, total_score, home_set_score, away_set_score) VALUES (%s, %s, %s, %s, %s)"

                        match_result = cursor.execute(result_query, values)
                        if match_result > 0:
                            sql.connection.commit()

                        else:
                            return {"status": "Volleyball result insertion failed"}

                    else:
                        return {"status": "Result insertion failed"}
                elif r['sport_name'] == 'LOL':
                    home_score = 0
                    away_score = 0
                    sides = ('HOME', 'AWAY')
                    objectives = []
                    for i in range(6):
                        taken_by = randint(0,1)
                        objectives.append(taken_by)
                    winner = sides[objectives[0]]
                    elder = sides[objectives[0]]
                    baron = sides[objectives[0]]
                    soul = sides[objectives[0]]
                    f_tower = sides[objectives[0]]
                    f_blood = sides[objectives[0]]
                    if winner == 'HOME':
                        home_score = 1
                    else:
                        away_score = 1

                    values = (r["match_ID"], home_score, away_score)
                    result_query = "INSERT INTO results (match_ID, home_score, away_acore) VALUES (%s, %s, %s) "

                    match_result = cursor.execute(result_query, values)
                    if match_result > 0:
                        cursor.execute("SELECT LAST_INSERT_ID()")

                        last_result_ID = cursor.fetchone()[0]

                        values = ( last_result_ID, winner, elder, baron, soul, f_tower, f_blood )
                        result_query = "INSERT INTO lol_results (l_result_ID, winner_side, elder_dragon_side, baron_side, soul_side, first_tower_side, first_blood_side) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                        match_result = cursor.execute(result_query, values)
                        if match_result > 0:
                            sql.connection.commit()

                        else:
                            return {"status": "LOL result insertion failed"}

                    else:
                        return {"status": "Result insertion failed"}

            match_IDs = []

            for r in unfinished_match_tuple:
                match_IDs.append(r[0])

            if len( match_IDs ) != 0:
                
                match_IDs = tuple(match_IDs)

                select_slip_query = "SELECT DISTINCT bet_slip_ID FROM placed_on WHERE match_ID IN %s"
                select_slip = cursor.execute(select_slip_query, match_IDs)
                if select_slip > 0:
                    betslips = cursor.fetchall()
                    slip_list = []

                    for r in betslips:
                        slip_list.append( r[0] )
                    
                    if len(slip_list) != 0:
                        slip_list = tuple(slip_list)

                        winning_query = "WITH bet_data AS ( SELECT * FROM placed_on NATURAL JOIN bet), winning_slips AS ( SELECT bet_data.bet_slip_ID, ratio FROM bet_data WHERE bet_slip_ID IN %s AND NOT EXISTS ( SELECT bet_ID FROM placed_on NATURAL JOIN bet WHERE bet_data.bet_slip_ID = bet_slip_ID AND (result = 'LOST' OR result = 'PENDING'))) SELECT DISTINCT * FROM winning_slips NATURAL JOIN bet_slip"
                        winnings = cursor.execute(winning_query, slip_list)
                        if winnings > 0:
                            winning_slips = []
                            winning_slips_cols = [col[0] for col in cursor.description]

                            for r in cursor.fetchall():
                                winning_slips.append( dict( zip(winning_slips_cols, r)) )
                            
                            payment = []

                            for r in winning_slips:
                                user_found = False

                                for data in payment:
                                    if r["creator_ID"] == data["creator_ID"]:
                                        user_found = True
                                        data["money"] = data["money"] * r["ratio"]
                                if not user_found:
                                    payment_add = {
                                        "creator_ID": r["creator_ID"],
                                        "money" : r["total_amount"] * r["ratio"]
                                    }

                                    payment.append(payment_add)
                            
                            for r in payment:
                                value = (r["money"], r["creator_ID"])
                                update_query = "UPDATE normal_user SET balance = normal_user.balance + %s WHERE n_user_ID = %s "
                                update = cursor.execute(update_query, value)
                                if update > 0:
                                    sql.connection.commit()
                                else:
                                   {"status": "Update values failed"} 
                            return {"status": "success"}
                        else:
                            {"status": "No winning slips"}
            else:
                {"status": "No ended matches"}

                
        

                                                                         


app.run(debug=True)