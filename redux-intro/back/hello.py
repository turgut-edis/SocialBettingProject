import json
import time
from turtle import update
from unittest import result
from flask import Flask, render_template, request, flash, session, jsonify, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
from random import randint


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'db_project'
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
                        "esport_filter AS (SELECT match_ID FROM plays NATURAL JOIN competitors NATURAL JOIN esports_team WHERE team_name LIKE %s), " \
                        "team_filter AS (SELECT match_ID FROM plays NATURAL JOIN competitors NATURAL JOIN team WHERE team_name LIKE %s), " \
                        "competitor_union AS (SELECT match_ID FROM esport_filter UNION TABLE team_filter), "\
                        "final_filter AS (SELECT DISTINCT match_ID FROM s_filter INNER JOIN b_filter USING(match_ID) INNER JOIN c_filter USING(match_ID) INNER JOIN c_filter USING(match_ID) " \
                        "INNER JOIN competitor_union USING(match_ID))"
        continuing_filter = filter_query + ", data AS (SELECT * FROM final_filter NATURAL JOIN matches), " \
                            "all_competitors AS (SELECT team_name, competitor_ID FROM competitors), " \
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
                    home_side = r["team_name"]
                    away_side = ""
                else:
                    home_side = ""
                    away_side = r["team_name"]

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
        select_user_query = "SELECT user_ID FROM user WHERE username = %s"
        value = (info["username"])
        execute_select = cursor.execute(select_user_query, value)
        if execute_select > 0:
            user_ID = cursor.fetchone()[0]
            select_bet_slip_query = "SELECT bet_slip_ID FROM bet_slip WHERE isPlayed = FALSE AND creator_ID = %s"
            value = (user_ID)
            execute_select_slip = cursor.execute(select_bet_slip_query, value)
            if execute_select_slip > 0:
                bet_slip_ID = cursor.fetchone()[0]
                insert_shared_slip = "INSERT INTO shared_slip (bet_slip_ID, sharer_ID) VALUES (%s, %s)"
                value = (bet_slip_ID, user_ID)
                execute_insert_shared = cursor.execute(insert_shared_slip, value)
                if execute_insert_shared > 0:
                    
                    update_slip = "UPDATE bet_slip SET total_amount = 0, isPlayed = TRUE WHERE creator_ID = %s AND bet_slip_ID = %s"
                    value = (user_ID, bet_slip_ID)
                    execute_update = cursor.execute(update_slip, value)
                    if execute_update > 0:
                        insert_slip = "INSERT INTO bet_slip (creator_ID, bet_count, total_amount, isPlayed) VALUES (%s, 0, 0, FALSE)"
                        value = (user_ID)
                        execute_insert = cursor.execute(insert_slip, value)
                        if execute_insert > 0:
                            sql.connection.commit()
                            return {"status" : "success"}
                        else:
                            return {"status" : "insert_slip_failed"}
                    else:
                        return {"status" : "update_slip_failed"}
                else:
                  return {"status" : "share_slip_failed"}
            else:
                return {"status" : "select_slip_failed"}
        else:
            return {"status" : "select_user_failed"}
            
    elif info["request_type"] == "suggest_bet":
        select_user_query = "SELECT user_ID FROM user WHERE username = %s"
        value = (info["username"])
        execute_select = cursor.execute(select_user_query, value)
        if execute_select > 0:
            user_ID = cursor.fetchone()[0]
            insert_suggested = "INSERT INTO suggested_bet (editor_ID, bet_ID, match_ID, comment) VALUES (%s, %s, %s, %s)"
            value = (user_ID, info["bet_ID"], info["match_ID"], info["editor_comment"])
            execute_insert = cursor.execute(insert_suggested, value)
            if execute_insert > 0:
                sql.connection.commit()
                return {"status" : "success"}
            else:
                return {"status" : "suggest_bet_failed"}
        else:
            return {"status" : "select_user_failed"}
            
    elif info["request_type"] == "add_bet_to_betslip":
        select_user_query = "SELECT user_ID FROM user WHERE username = %s"
        value = (info["username"])
        execute_select = cursor.execute(select_user_query, value)
        if execute_select > 0:
            user_ID = cursor.fetchone()[0]
            select_bet_slip_query = "SELECT bet_slip_ID FROM bet_slip WHERE isPlayed = FALSE AND creator_ID = %s"
            value = (user_ID)
            execute_select_slip = cursor.execute(select_bet_slip_query, value)
            if execute_select_slip > 0:
                bet_slip_ID = cursor.fetchone()[0]
                update_bet_cnt = "UPDATE bet_slip SET bet_count = bet_slip.bet_count + 1 WHERE creator_ID = %s AND bet_slip_ID = %s"
                values = (user_ID, bet_slip_ID)
                execute_update = cursor.execute(update_bet_cnt, values)
                if execute_update:
                    insert_placed_on = "INSERT INTO placed_on (bet_slip_ID, bet_ID, match_ID) VALUES (%s, %s, %s)"
                    value = (bet_slip_ID, info["bet_ID"], info["match_ID"])
                    execute_insert = cursor.execute(insert_placed_on, value)
                    if execute_insert > 0:
                        sql.connection.commit()
                        return {"status" : "success"}
                    else:
                        return {"status" : "insert_placed_on_failed"}
                else:
                    return {"status" : "update_bet_slip_failed"}
            else:
                return {"status" : "select_user_failed"}
        else:
            return {"status" : "select_user_failed"}

    elif info["request_type"] == "remove_bet_from_betslip":
        select_user_query = "SELECT user_ID FROM user WHERE username = %s"
        value = (info["username"])
        execute_select = cursor.execute(select_user_query, value)
        if execute_select > 0:
            user_ID = cursor.fetchone()[0]
            select_bet_slip_query = "SELECT bet_slip_ID FROM bet_slip WHERE isPlayed = FALSE AND creator_ID = %s"
            value = (user_ID)
            execute_select_slip = cursor.execute(select_bet_slip_query, value)
            if execute_select_slip > 0:
                bet_slip_ID = cursor.fetchone()[0]
                update_bet_cnt = "UPDATE bet_slip SET bet_count = bet_slip.bet_count - 1 WHERE creator_ID = %s AND bet_slip_ID = %s"
                values = (user_ID, bet_slip_ID)
                execute_update = cursor.execute(update_bet_cnt, values)
                if execute_update:
                    insert_placed_on = "DELETE placed_on FROM placed_on WHERE bet_slip_ID = %s AND bet_ID = %s AND match_ID = %s"
                    value = (bet_slip_ID, info["bet_ID"], info["match_ID"])
                    execute_insert = cursor.execute(insert_placed_on, value)
                    if execute_insert > 0:
                        sql.connection.commit()
                        return {"status" : "success"}
                    else:
                        return {"status" : "insert_placed_on_failed"}
                else:
                    return {"status" : "update_bet_slip_failed"}
            else:
                return {"status" : "select_user_failed"}
        else:
            return {"status" : "select_user_failed"}

    elif info["request_type"] == "display_user_bet_slip":
        select_bets_query = "WITH user_bet_slips AS (SELECT bet_slip_ID FROM bet_slip WHERE creator_ID = %s AND placed = FALSE), " \
                            "all_bet_data AS (SELECT * FROM user_bet_slips NATURAL JOIN placed_on NATURAL JOIN bet), " \
                            "match_data AS (SELECT * FROM all_bet_data NATURAL JOIN plays), all_competitors AS " \
                            "(SELECT team_name, competitor_id FROM competitors) SELECT * FROM match_data NATURAL JOIN " \
                            "all_competitors"
        value = (info["user_ID"])
        execute_select = cursor.execute(select_bets_query, value)
        if execute_select > 0:
            user_bets_results = []

            user_bets_columns = [col[0] for col in cursor.description]

            for row in cursor.fetchall():
                user_bets_results.append(dict(zip(user_bets_columns, row)))

            user_map = {
                "user_ID": info["user_ID"],
                "bets": []
            }

            for row in user_bets_results:
                composite_already_added = False

                if row["side"] == "HOME":
                    home_side = row["team_name"]
                    away_side = ""

                else:
                    home_side = ""
                    away_side = row["team_name"]

                total_ratio = row["ratio"]

                for bet in user_map["bets"]:
                    if bet["bet_ID"] == row["bet_ID"] and bet["match_ID"] == row["match_ID"]:
                        composite_already_added = True

                        if bet["home_side"] == "":
                            bet["home_side"] = row["team_name"]
                        else:
                            bet["away_side"] = row["team_name"]
                if not composite_already_added:
                    bet_to_add = {
                        "bet_ID": row["bet_ID"],
                        "match_ID": row["match_ID"],
                        "home_side": home_side,
                        "away_side": away_side,
                        "result": row["result"],
                        "mbn": row["mbn"],
                        "ratio": total_ratio,
                        "bet_type": row["bet_type"]
                    }
                    user_map["bets"].append(bet_to_add)

            return user_map 
        else:
            return {"status" : "select_user_failed"}
        
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

@app.route('/feed', methods=['GET', 'POST'])
def feed():
    cursor = sql.connection.cursor()
    info = request.get_json(force=True)

    if info["request_type"] == "display_shared_bets": #Requires ["user_id"]

        friend_slip_ID_query = "WITH friend_ID_set AS (SELECT friend_ID AS user_ID FROM normal_user_friend \
                               WHERE user_ID = %s), friend_info AS (SELECT username, user_ID AS sharer_ID FROM friend_ID_set \
                               NATURAL JOIN user), friend_slip_ID AS (SELECT * FROM (shared_slip NATURAL JOIN (SELECT \
                               user_ID AS sharer_ID FROM friend_ID_set) AS sharing_user ))"
        value = (info["user_ID"])
        comment_query = friend_slip_ID_query + " SELECT bet_slip_ID, comment_ID, comment, username FROM friend_slip_ID NATURAL JOIN bet_slip_comment NATURAL JOIN comments NATURAL JOIN user"
        execute_query = cursor.execute(comment_query, value)
        if execute_query:
            comment_res = []

            comment_columns = [col[0] for col in cursor.description]

            for r in cursor.fetchall():
                comment_res.append( dict( zip( comment_columns, r ) ) )
            
            like_query = friend_slip_ID_query + " SELECT comment_ID, Count(user_ID) as comment_like_count FROM friend_slip_ID NATURAL JOIN bet_slip_comment NATURAL JOIN like_comment GROUP BY comment_ID"
            execute_like = cursor.execute(like_query, value)
            if execute_like:
                
                comment_like_results = []

                comment_like_columns = [col[0] for col in cursor.description]

                for r in cursor.fetchall():
                    comment_like_results.append(dict(zip(comment_like_columns, r)))
                
                slip_like_query = friend_slip_ID_query + " SELECT bet_slip_ID, Count(bet_slip_ID) as slip_like_count FROM friend_slip_ID NATURAL JOIN bet_slip_like GROUP BY bet_slip_ID"
                execute_slip_like = cursor.execute(slip_like_query, value)
                if execute_slip_like:
                    bet_slip_like_results = []

                    bet_slip_like_columns = [col[0] for col in cursor.description]

                    for r in cursor.fetchall():
                        bet_slip_like_results.append(dict(zip(bet_slip_like_columns, r)))
                        
                        friend_bet_slip_query = friend_slip_ID_query + ", friend_slip_bet AS ( SELECT * FROM (placed_on NATURAL JOIN friend_slip_ID) ), \
                                                friend_slip_bet_data AS (SELECT * FROM friend_slip_bet NATURAL JOIN bet), match_data AS (SELECT * FROM friend_slip_bet_data NATURAL JOIN plays), \
                                                all_competitors AS ( SELECT team_name, competitor_ID FROM competitors ) \
                                                SELECT DISTINCT *  FROM match_data NATURAL JOIN all_competitors NATURAL JOIN (SELECT sharer_ID, username FROM friend_data) AS friend_temp"
                        execute_f_bet = cursor.execute(friend_bet_slip_query, value)
                        if execute_f_bet:
                            
                            friend_bet_slip_results = []

                            feed_columns = [col[0] for col in cursor.description]

                            for r in cursor.fetchall():
                                friend_bet_slip_results.append( dict( zip( feed_columns, r ) ) )

                            friend_bet_slip_map = []

                            for row in friend_bet_slip_results:
                                composite_already_added = False
                                bet_slip_found = False
                                friend_found = False

                                if row["side"] == "HOME":
                                    home_side = row["team_name"]
                                    away_side = ""
                                else:
                                    home_side = ""
                                    away_side = row["team_name"]

                                total_ratio = row["ratio"]
                                sharer_ID = row["sharer_ID"]

                                for friend in friend_bet_slip_map:
                                    if friend["user_ID"] == sharer_ID:

                                        friend_found = True
                                        for bet_slip in friend["bet_slips"]:

                                            if bet_slip["bet_slip_ID"] == row["bet_slip_ID"]:
                                                bet_slip_found = True
                                                for bet in bet_slip["bets"]:
                                                    if bet["bet_ID"] == row["bet_ID"] and bet["match_ID"] == row["match_ID"]:
                                                        composite_already_added = True

                                                        if bet["home_side"] == "":
                                                            bet["home_side"] = row["team_name"]
                                                        else:
                                                            bet["away_side"] = row["team_name"]
                                                if not composite_already_added:
                                                    bet_to_add = {
                                                        "bet_ID": row["bet_ID"],
                                                        "match_ID": row["match_ID"],
                                                        "home_side": home_side,
                                                        "away_side": away_side,
                                                        "ratio": total_ratio,
                                                        "result": row["result"],
                                                        "bet_type": row["bet_type"]
                                                    }
                                                    bet_slip["bets"].append(bet_to_add)

                                        if not bet_slip_found:
                                            bets = [{
                                                "bet_ID": row["bet_ID"],
                                                "match_ID": row["match_ID"],
                                                "home_side": home_side,
                                                "away_side": away_side,
                                                "ratio": total_ratio,
                                                "result": row["result"],
                                                "bet_type": row["bet_type"]
                                            }]
                                            friend["bet_slips"].append({
                                                "bet_slip_ID": row["bet_slip_ID"],
                                                "bets": bets
                                            })
                                if not friend_found:
                                    friend_to_add = {
                                        "user_ID": sharer_ID,
                                        "username": row["username"],
                                        "bet_slips": []
                                    }

                                    bets = [{
                                        "bet_ID": row["bet_ID"],
                                        "match_ID": row["match_ID"],
                                        "home_side": home_side,
                                        "away_side": away_side,
                                        "ratio": total_ratio,
                                        "result": row["result"],
                                        "bet_type": row["bet_type"]
                                    }]

                                    friend_to_add["bet_slips"].append({
                                        "bet_slip_ID": row["bet_slip_ID"],
                                        "bets": bets
                                    })
                                    friend_bet_slip_map.append(friend_to_add)

                            comment_map = []

                            for row in comment_res:
                                bet_slip_found = False

                                comment_to_add = {
                                    "username": row["username"],
                                    "comment_ID": row["comment_ID"],
                                    "comment": row["comment"],
                                    "comment_like_count": ""
                                }

                                for liked_comment in comment_like_results:
                                    if liked_comment["comment_ID"] == comment_to_add["comment_ID"]:
                                        comment_to_add["comment_like_count"] = liked_comment["comment_like_count"]

                                for bet_slip in comment_map:

                                    if row["bet_slip_ID"] == bet_slip["bet_slip_ID"]:
                                        bet_slip_found = True

                                        bet_slip["bet_slip_comments"].append(comment_to_add)
                                if not bet_slip_found:
                                    comment_map_to_add = {
                                        "bet_slip_ID": row["bet_slip_ID"],
                                        "bet_slip_comments": [comment_to_add]
                                    }

                                    comment_map.append(comment_map_to_add)

                            for friend in friend_bet_slip_map:

                                for friend_bet_slip in friend["bet_slips"]:

                                    for like in bet_slip_like_results:
                                        if like["bet_slip_ID"] == friend_bet_slip["bet_slip_ID"]:
                                            friend_bet_slip["like_count"] = like["like_count"]

                                    for bet_slip_comments in comment_map:

                                        if bet_slip_comments["bet_slip_ID"] == friend_bet_slip["bet_slip_ID"]:
                                            friend_bet_slip["comments"] = bet_slip_comments["bet_slip_comments"]

                            return {"users": friend_bet_slip_map}
                        else:
                            return{"status" : "select_friend_slip_failed"}
                else:
                    return{"status" : "select_slip_like_failed"}
            else:
                return{"status" : "select_comment_like_failed"}
        else:
            return{"status" : "select_comment_failed"}
            
    elif info["request_type"] == "user_like_bet_slip":
        insert_slip_query = "INSERT INTO bet_slip_like (n_user_ID, bet_slip_ID) VALUES (%s, %s)"
        value = (info["user_ID"], info["focused_bet_slip_ID"])
        execute_insert = cursor.execute(insert_slip_query, value)
        if execute_insert:
            sql.connection.commit()
            return {"status": "success"}
        else:
            return {"status": "Could not insert into bet_slip_like"}

    elif info["request_type"] == "comment_on_bet_slip":
        insert_comment_query = "INSERT INTO comments (user_ID, comment, comment_date, like_count) VALUES ( %s, %s , NOW(), 0)"
        value = (info["user_ID"], info["comment_text"])
        execute_insert = cursor.execute(insert_comment_query, value)
        if execute_insert:

            cursor.execute("SELECT LAST_INSERT_ID()")

            last_comment_ID = cursor.fetchone()[0]
            insert_slip_comment_query = "INSERT INTO bet_slip_comment(comment_ID, bet_slip_ID) VALUES (%s, %s)"
            value = (last_comment_ID, info["focused_bet_slip_ID"])
            execute_insert = cursor.execute(insert_slip_comment_query, value)
            if execute_insert:
                cursor.connection.commit()
                return {"status": "success"}
            else:
                return {"status": "Could not insert into bet_slip_comment"}
        else:
            return {"status": "Could not insert into comment table"}

    elif info["request_type"] == "like_comment":
        like_query = "INSERT INTO like_comment (comment_ID, n_user_ID) VALUES (%s, %s)"
        value = info["comment_ID"], info["user_ID"]
        execute_like = cursor.execute(like_query, value)
        if execute_like:
            sql.connection.commit()
            return {"status": "success"}
        else:
            return {"status": "Could not like comment"}

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
                                "user_ID" : user[0],
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

    elif info["request_type"] == "insert_bet":

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
                
@app.route('/profile', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
def profile():
    info = request.get_json()
    if info["request_type"] == "get_user_info":
        cursor = sql.connection.cursor()
        statement = "WITH current AS (SELECT n_user_ID, balance, winning_cnt FROM normal_user) \
                    SELECT username, name, surname, balance, winning_cnt, birth_year, mail FROM current \
                    NATURAL JOIN user WHERE user_ID = {0}".format(info["user_ID"])
        value = (info["user_ID"])
        cursor.execute(statement)
        
        user = cursor.fetchone()
        result = {
            "username" : user[0],
            "name" : user[1],
            "surname" : user[2],
            "balance" : user[3],
            "winning_cnt" : user[4],
            "birth_year" : user[5],
            "mail" : user[6]
        }

        return jsonify({"result" : result})

    if info["request_type"] == "get_pending_bet_slips":
        cursor = sql.connection.cursor()

        cursor.execute("WITH user_bet_slips AS (SELECT bet_slip_ID FROM bet_slip WHERE creator_ID = {0} AND isPlayed = TRUE), \
                        pending_slip AS (SELECT DISTINCT bet_slip_ID FROM user_bet_slips NATURAL JOIN placed_on NATURAL JOIN bet WHERE result = 'PENDING'), \
                        bet_data AS (SELECT * FROM pending_slip NATURAL JOIN placed_on NATURAL JOIN bet), match_data AS (SELECT * FROM bet_data NATURAL JOIN \
                        plays), all_competitors AS (SELECT team_name, competitor_ID FROM competitors) SELECT * FROM match_data NATURAL JOIN all_competitors".format(info["user_ID"]))
        
        bet_slip_results_pending = []
        
        pending_bet_slips_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            bet_slip_results_pending.append(dict(zip(pending_bet_slips_columns, row)))

        user_hash = {
            "user_ID" : info["user_ID"],
            "bet_slips" : []
        }

        for row in bet_slip_results_pending:
            already_added = False
            bet_slip_found = False

            if row["side"] == "HOME":
                home_side = row["team_name"]
                away_side = ""
            else:
                home_side = ""
                away_side = row["team_name"]

            total_ratio = row["ratio"]

            for bet_slip in user_hash["bet_slips"]:
                if bet_slip["bet_slip_ID"] == row["bet_slip_ID"]:
                    bet_slip_found = True
                    
                    for bet in bet_slip["bets"]:
                        if bet["bet_ID"] == row["bet_ID"] and bet["match_ID"] == row["match_ID"]:
                            already_added = True
                            if bet["home_side"] == "":
                                bet["home_side"] = row["team_name"]
                            else:
                                bet["away_side"] = row["team_name"]
                    if not already_added:
                        bet_to_add = {
                            "bet_ID": row["bet_ID"],
                            "match_ID": row["match_ID"],
                            "home_side": home_side,
                            "away_side": away_side,
                            "result": row["result"],
                            "mbn": row["mbn"],
                            "ratio": total_ratio,
                            "bet_type": row["bet_type"]
                        }
                        bet_slip["bets"].append(bet_to_add)
            if not bet_slip_found:
                bets = [{
                    "bet_ID": row["bet_ID"],
                    "match_ID": row["match_ID"],
                    "home_side": home_side,
                    "away_side": away_side,
                    "result": row["result"],
                    "mbn": row["mbn"],
                    "ratio": total_ratio,
                    "bet_type": row["bet_type"]
                }]
                user_hash["bet_slips"].append({
                    "bet_slip_ID": row["bet_slip_ID"],
                    "bets": bets
                })           

        return user_hash

    if info["request_type"] == "get_ended_bet_slips":
        cursor = sql.connection.cursor()

        cursor.execute("WITH user_bet_slips AS (SELECT bet_slip_ID FROM bet_slip WHERE creator_id = {0}), ended_slip AS"
                    " (SELECT DISTINCT u.bet_slip_ID FROM user_bet_slips u WHERE NOT EXISTS (SELECT bet_ID FROM "
                    " user_bet_slips NATURAL JOIN placed_on NATURAL JOIN bet WHERE bet_slip_ID = u.bet_slip_ID AND"
                    " result = 'PENDING')), all_bet_data AS (SELECT * FROM ended_slip NATURAL JOIN placed_on"
                    " NATURAL JOIN bet), match_data AS (SELECT * FROM all_bet_data NATURAL JOIN plays),"
                    " all_competitors AS (SELECT team_name, competitor_ID FROM competitors) SELECT * FROM match_data \
                        NATURAL JOIN all_competitors".format(info["user_ID"]))

        bet_slip_results_ended = []

        ended_bet_slips_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            bet_slip_results_ended.append(dict(zip(ended_bet_slips_columns, row)))

        user_hash = {
            "user_ID": info["user_ID"],
            "bet_slips": []
        }

        for row in bet_slip_results_ended:
            composite_already_added = False
            bet_slip_found = False

            if row["side"] == "HOME":
                home_side = row["team_name"]
                away_side = ""

            else:
                home_side = ""
                away_side = row["team_name"]

            total_ratio = row["ratio"]

            for bet_slip in user_hash["bet_slips"]:

                if bet_slip["bet_slip_ID"] == row["bet_slip_ID"]:
                    bet_slip_found = True
                    for bet in bet_slip["bets"]:
                        if bet["bet_ID"] == row["bet_ID"] and bet["match_ID"] == row["match_id"]:
                            composite_already_added = True

                            if bet["home_side"] == "":
                                bet["home_side"] = row["team_name"]
                            else:
                                bet["away_side"] = row["team_name"]
                    if not composite_already_added:
                        bet_to_add = {
                            "bet_ID": row["bet_ID"],
                            "match_ID": row["match_ID"],
                            "home_side": home_side,
                            "away_side": away_side,
                            "result": row["result"],
                            "mbn": row["mbn"],
                            "ratio": total_ratio,
                            "bet_type": row["bet_type"]
                        }
                        bet_slip["bets"].append(bet_to_add)

            if not bet_slip_found:
                bets = [{
                    "bet_ID": row["bet_ID"],
                    "match_ID": row["match_ID"],
                    "home_side": home_side,
                    "away_side": away_side,
                    "result": row["result"],
                    "mbn": row["mbn"],
                    "ratio": total_ratio,
                    "bet_type": row["bet_type"]
                }]
                user_hash["bet_slips"].append({
                    "bet_slip_ID": row["bet_slip_ID"],
                    "bets": bets
                })

        return user_hash
    
    if info["request_type"] == "get_friends":
        cursor = sql.connection.cursor()

        cursor.execute("WITH friends AS (SELECT friend_ID, user_ID "
                    "FROM normal_user_friend) SELECT username FROM friends NATURAL JOIN user "
                    "WHERE user_ID = '{0}'".format(info["user_ID"]))

        user = cursor.fetchall()
        friends = []

        for row in user:
            friends.append(row[0])

        result = {
            "friends": friends
        }
        return jsonify({"result": result})
    
    if info["request_type"] == "search_users":
        cursor = sql.connection.cursor()
        cursor.execute("SELECT n_user_ID, username FROM normal_user AS n INNER JOIN user AS u ON n.n_user_ID = u.user_ID "
                    "WHERE username LIKE {0} AND n.n_user_ID <> {1}"
                    .format('\'' + info["search_text"] + '%\'', info["user_ID"]))

        val = cursor.fetchall()
        users = []

        for row in val:
            friend = {"user_ID": row[0], "username": row[1]}
            users.append(friend)

        result = {
            "searched_users": users
        }
        return jsonify({"result": result})

    if info["request_type"] == "add_friend":
        cursor = sql.connection.cursor()
        val1 = cursor.execute("INSERT INTO normal_user_friend (user_ID, friend_ID) VALUES ({0}, {1})"
                           .format(info["user_ID"], info["friend_ID"]))
        sql.connection.commit()

        val2 = cursor.execute("INSERT INTO normal_user_friend (user_ID, friend_ID) VALUES ({1}, {0})"
                           .format(info["user_ID"], info["friend_ID"]))
        sql.connection.commit()

        if val1 > 0 and val2 > 0:
            result = {
                "success": True
            }
        else:
            result = {
                "success": False
            }

        return jsonify({"result": result})

    if info["request_type"] == "update_balance":
        cursor = sql.connection.cursor()
        val = cursor.execute("UPDATE normal_user SET balance = ( normal_user.balance + {1} ) "
                          "WHERE n_user_ID = {0}".format(info["user_ID"], info["balance_change"]))

        sql.connection.commit()

        if val > 0:
            result = {
                "success": True
            }
        else:
            result = {
                "success": False
            }

        return jsonify({"result": result})
    
    if info["request_type"] == "edit_profile":
        cursor = sql.connection.cursor()
        check = cursor.execute("SELECT * FROM user WHERE username = '{0}'".format(info["new_username"]))
        
        if check > 0:
            result = {
                "success": False
            }
            return jsonify({"result": result})
        else:
            val1 = cursor.execute("UPDATE user SET username = '{1}' WHERE user_ID = '{0}'"
                               .format(info["user_ID"], info["new_username"]))
            sql.connection.commit()

            val2 = cursor.execute("UPDATE user SET password = '{1}' WHERE user_ID = '{0}'"
                               .format(info["user_ID"], info["new_password"]))
            sql.connection.commit()

            if val1 > 0 and val2 > 0:
                result = {
                    "success": True
                }
            else:
                result = {
                    "success": False
                }

            return jsonify({"result": result})

@app.route('/editor', methods=["GET", "POST"])
def editor():
    cursor = sql.connection.cursor()

    info = request.get_json(force=True)
    print(info)
    if info["request_type"] == "display_editors":  

        cursor.execute("SELECT name, surname, editor_id_table.win_rate, winning_cnt, user_ID AS editor_ID FROM "
                    "( (SELECT editor.editor_ID AS user_ID, win_rate, winning_cnt FROM editor) AS editor_id_table "
                    "NATURAL JOIN user)")

        editor_results = []
        editor_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            editor_results.append(dict(zip(editor_columns, row)))

        cursor.execute("SELECT editor_ID FROM normal_user_follows WHERE user_ID = {0}".format(info["user_ID"]))

        user_follows_results = []

        user_follows_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            user_follows_results.append(dict(zip(user_follows_columns, row)))

        cursor.execute("WITH editor_slip_data AS (SELECT * FROM ( (SELECT bet_slip_ID, sharer_ID as editor_ID FROM "
                    "shared_slip WHERE sharer_ID IN (SELECT editor_ID FROM editor)) as editor_slips NATURAL JOIN"
                    " placed_on NATURAL JOIN bet)), match_data AS (SELECT * FROM editor_slip_data NATURAL JOIN "
                    "plays), all_competitors AS (SELECT team_name, competitor_ID FROM competitors)"
                    ", match_date AS (SELECT match_ID, start_date FROM matches NATURAL JOIN "
                    "editor_slip_data) SELECT DISTINCT * FROM (match_data NATURAL JOIN editor_slip_data NATURAL JOIN"
                    " all_competitors NATURAL JOIN match_date)")

        editor_slips_results = []

        editor_slip_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            editor_slips_results.append(dict(zip(editor_slip_columns, row)))

        editor_bet_slip_comment_query = \
            "WITH editor_bet_slips AS (SELECT bet_slip_ID, sharer_ID as editor_ID FROM shared_slip WHERE" \
            " sharer_ID IN (SELECT editor_ID FROM editor)) "

        cursor.execute(editor_bet_slip_comment_query + " SELECT bet_slip_ID, comment_ID, comment, username "
                                                    "FROM editor_bet_slips NATURAL JOIN"
                                                    " bet_slip_comment NATURAL JOIN comments NATURAL JOIN user")

        bet_slip_comments_results = []

        bet_slip_comments_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            bet_slip_comments_results.append(dict(zip(bet_slip_comments_columns, row)))

        cursor.execute(editor_bet_slip_comment_query + " SELECT bet_slip_ID, Count(bet_slip_ID) as like_count FROM"
                                                    " editor_bet_slips NATURAL JOIN bet_slip_like GROUP BY bet_slip_ID")

        bet_slip_like_results = []

        bet_slip_like_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            bet_slip_like_results.append(dict(zip(bet_slip_like_columns, row)))

        cursor.execute(editor_bet_slip_comment_query + " SELECT comment_ID, Count(n_user_ID) as comment_like_count FROM"
                                                    " editor_bet_slips NATURAL JOIN bet_slip_comment "
                                                    "NATURAL JOIN like_comment GROUP BY comment_ID")

        bet_slip_comments_likes_results = []

        bet_slip_comments_likes_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            bet_slip_comments_likes_results.append(dict(zip(bet_slip_comments_likes_columns, row)))
        

        bet_slip_comment_map = []

        for row in bet_slip_comments_results:
            bet_slip_found = False

            comment_to_add = {
                "username": row["username"],
                "comment_ID": row["comment_ID"],
                "comment": row["comment"],
                "like_count": ""
            }

            for liked_comment in bet_slip_comments_likes_results:
                if liked_comment["comment_ID"] == comment_to_add["comment_ID"]:
                    comment_to_add["like_count"] = liked_comment["like_count"]

            for bet_slip in bet_slip_comment_map:

                if row["bet_slip_ID"] == bet_slip["bet_slip_ID"]:
                    bet_slip_found = True

                    bet_slip["bet_slip_comments"].append(comment_to_add)
            if not bet_slip_found:
                comment_map_to_add = {
                    "bet_slip_ID": row["bet_slip_ID"],
                    "bet_slip_comments": [comment_to_add]
                }

                bet_slip_comment_map.append(comment_map_to_add)

        cursor.execute("SELECT editor_ID FROM editor")

        editor_id_results = []

        editor_id_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            editor_id_results.append(dict(zip(editor_id_columns, row)))

        editor_won_lost_results_dict = []

        for editor_id in editor_id_results:
  
            editor_to_add = {
                "editor_ID": editor_id["editor_ID"],
                "bet_slips_won": 0,
                "bet_slips_lost": 0,
                "single_bet_win_count": 0,
                "single_bet_lose_count": 0
            }
            if cursor.execute("WITH editor_slips AS (SELECT bet_slip_ID, creator_ID as editor_ID FROM bet_slip WHERE "
                           "creator_ID = {0}), editor_bet_ID AS (SELECT * FROM placed_on NATURAL JOIN editor_slips)"
                           " SELECT COUNT(bet_slip_ID) AS won_bet_slip_count FROM editor_slips WHERE NOT EXISTS (SELECT"
                           " bet_ID, match_ID FROM editor_bet_ID NATURAL JOIN bet WHERE bet_slip_ID = bet_slip_ID "
                           "AND (result = 'LOST' OR result = 'PENDING')) GROUP BY editor_ID"
                                   .format(editor_id["editor_ID"])) > 0:
                won_count = cursor.fetchone()[0]
                editor_to_add["bet_slips_won"] = won_count

            if cursor.execute("WITH editor_slips AS (SELECT bet_slip_ID, creator_ID as editor_ID FROM bet_slip WHERE"
                           " creator_ID = {0}), editor_bet_ID AS (SELECT * FROM placed_on NATURAL JOIN editor_slips)"
                           "SELECT COUNT(bet_slip_ID) AS lost_bet_slip_count FROM editor_slips WHERE NOT "
                           "EXISTS (SELECT bet_ID, match_ID FROM editor_bet_ID NATURAL JOIN bet WHERE "
                           "editor_slips.bet_slip_ID = bet_slip_ID AND (result = 'LOST')) GROUP BY editor_ID"
                                   .format(editor_id["editor_ID"])) > 0:
                lost_count = cursor.fetchone()[0]
                editor_to_add["bet_slips_lost"] = lost_count

            if cursor.execute("WITH editor_bets AS (SELECT bet_ID, match_ID, editor_ID FROM suggested_bet WHERE editor_ID"
                           " = {0}) SELECT COUNT(bet_ID) AS won_count FROM editor_bets NATURAL JOIN bet"
                           " GROUP BY editor_ID, result HAVING result = 'WON'".format(editor_id["editor_ID"])) > 0:
                single_bet_win_count = cursor.fetchone()[0]
                editor_to_add["single_bet_win_count"] = single_bet_win_count

            if cursor.execute("WITH editor_bets AS (SELECT bet_ID, match_ID, editor_ID FROM suggested_bet WHERE editor_ID"
                           " = {0}) SELECT COUNT(bet_ID) AS won_count FROM editor_bets NATURAL JOIN bet"
                           " GROUP BY editor_ID, result HAVING result = 'LOST'".format(editor_id["editor_ID"])) > 0:
                single_bet_lose_count = cursor.fetchone()[0]
                editor_to_add["single_bet_lose_count"] = single_bet_lose_count

            editor_won_lost_results_dict.append(editor_to_add)

        cursor.execute("WITH suggested_bet_data AS (SELECT * FROM ((SELECT * FROM suggested_bet) as suggested NATURAL JOIN"
                    " bet)), match_data AS (SELECT * FROM suggested_bet_data NATURAL JOIN "
                    "plays), all_competitors AS (SELECT team_name, competitor_ID FROM competitors), match_date AS (SELECT match_ID, start_date FROM `matches` NATURAL JOIN "
                    "suggested_bet_data) SELECT * FROM match_data NATURAL JOIN suggested_bet_data NATURAL JOIN"
                    " all_competitors NATURAL JOIN match_date")

        suggested_bet_results = []

        suggested_bet_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            suggested_bet_results.append(dict(zip(suggested_bet_columns, row)))

        suggested_bet_map = []

        for row in suggested_bet_results:
            composite_already_added = False
            editor_found = False

            if row["side"] == "HOME":
                home_side = row["team_name"]
                away_side = ""

            else:
                home_side = ""
                away_side = row["team_name"]

            total_ratio = row["ratio"]
            editor_ID = row["editor_ID"]

            for editor in suggested_bet_map:

                if editor["editor_ID"] == editor_ID:
                    editor_found = True

                    for bet in editor["suggested_bets"]:
                        if bet["bet_ID"] == row["bet_ID"] and bet["match_ID"] == row["match_ID"]:
                            composite_already_added = True

                            if bet["home_side"] == "":
                                bet["home_side"] = row["team_name"]
                            else:
                                bet["away_side"] = row["team_name"]
                    if not composite_already_added:
                        bet_to_add = {
                            "bet_ID": row["bet_ID"],
                            "match_ID": row["match_ID"],
                            "home_side": home_side,
                            "away_side": away_side,
                            "ratio": total_ratio,
                            "result": row["result"],
                            "mbn": row["mbn"],
                            "start_date": row["start_date"],
                            "bet_type": row["bet_type"],
                            "comment": row["comment"]                     
                        }
                        editor["suggested_bets"].append(bet_to_add)
            if not editor_found:
                editor_to_add = {
                    "editor_ID": editor_ID,
                    "suggested_bets": []
                }

                suggested_bet = {
                    "bet_ID": row["bet_ID"],
                    "match_ID": row["match_ID"],
                    "home_side": home_side,
                    "away_side": away_side,
                    "ratio": total_ratio,
                    "result": row["result"],
                    "mbn": row["mbn"],
                    "start_date": row["start_date"],
                    "bet_type": row["bet_type"],
                    "comment": row["comment"]
                }

                editor_to_add["suggested_bets"].append(suggested_bet)

                suggested_bet_map.append(editor_to_add)

        editor_bet_slip_map = []

        for row in editor_slips_results:
            composite_already_added = False
            bet_slip_found = False
            editor_found = False

            if row["side"] == "HOME":
                home_side = row["team_name"]
                away_side = ""

            else:
                home_side = ""
                away_side = row["team_name"]

            total_ratio = row["ratio"]
            editor_ID = row["editor_ID"]

            for editor in editor_bet_slip_map:
                if editor["editor_ID"] == editor_ID:

                    editor_found = True
                    for bet_slip in editor["bet_slips"]:

                        if bet_slip["bet_slip_ID"] == row["bet_slip_ID"]:
                            bet_slip_found = True
                            for bet in bet_slip["bets"]:
                                if bet["bet_ID"] == row["bet_ID"] and bet["match_ID"] == row["match_ID"]:
                                    composite_already_added = True

                                    if bet["home_side"] == "":
                                        bet["home_side"] = row["team_name"]
                                    else:
                                        bet["away_side"] = row["team_name"]
                            if not composite_already_added:
                                bet_to_add = {
                                    "bet_ID": row["bet_ID"],
                                    "match_ID": row["match_ID"],
                                    "home_side": home_side,
                                    "away_side": away_side,
                                    "ratio": total_ratio,
                                    "result": row["result"],
                                    "mbn": row["mbn"],
                                    "start_date": row["start_date"],
                                    "bet_type": row["bet_type"]
                                }
                                bet_slip["bets"].append(bet_to_add)

                    if not bet_slip_found:
                        bets = [{
                            "bet_ID": row["bet_ID"],
                            "match_ID": row["match_ID"],
                            "home_side": home_side,
                            "away_side": away_side,
                            "ratio": total_ratio,
                            "result": row["result"],
                            "mbn": row["mbn"],
                            "start_date": row["start_date"],
                            "bet_type": row["bet_type"]
                        }]
                        editor["bet_slips"].append({
                            "bet_slip_ID": row["bet_slip_ID"],
                            "bets": bets,
                            "comments": [],
                            "bet_slip_like_count": 0
                        })
            if not editor_found:
                editor_to_add = {
                    "editor_ID": editor_ID,
                    "bet_slips": []
                }

                bets = [{
                    "bet_ID": row["bet_ID"],
                    "match_ID": row["match_ID"],
                    "home_side": home_side,
                    "away_side": away_side,
                    "ratio": total_ratio,
                    "result": row["result"],
                    "mbn": row["mbn"],
                    "start_date": row["start_date"],
                    "bet_type": row["bet_type"]
                }]

                editor_to_add["bet_slips"].append({
                    "bet_slip_ID": row["bet_slip_ID"],
                    "bets": bets,
                    "comments": [],
                    "bet_slip_like_count": 0
                })

                editor_bet_slip_map.append(editor_to_add)

        for editor in editor_bet_slip_map:
  
            for editor_bet_slip in editor["bet_slips"]:

                for like in bet_slip_like_results:
                    if like["bet_slip_ID"] == editor_bet_slip["bet_slip_ID"]:
                        editor_bet_slip["bet_slip_like_count"] = like["like_count"]

                for bet_slip_comments in bet_slip_comment_map:

                    if bet_slip_comments["bet_slip_ID"] == editor_bet_slip["bet_slip_ID"]:
                        editor_bet_slip["comments"] = bet_slip_comments["bet_slip_comments"]
        
        editor_final = []

        for editor in editor_results:
            editor_to_add = {
                "editor_ID": editor["editor_ID"],
                "name": editor["name"],
                "surname": editor["surname"],
                "win_rate": editor["win_rate"],
                "winning_cnt": editor["winning_cnt"],
                "followed_by_user": False,
                "single_bet_win_count": 0,
                "single_bet_lose_count": 0,
                "bet_slips_won": 0,
                "bet_slips_lost": 0,
                "bet_slips": [],
                "suggested_bets": []
            }
            for row in user_follows_results:
                if editor["editor_ID"] == row["editor_ID"]:
                    editor_to_add["followed_by_user"] = True

            for row in editor_won_lost_results_dict:
                if editor["editor_ID"] == row["editor_ID"]:
                    editor_to_add["single_bet_win_count"] = row["single_bet_win_count"]
                    editor_to_add["single_bet_lose_count"] = row["single_bet_lose_count"]
                    editor_to_add["bet_slips_won"] = row["bet_slips_won"]
                    editor_to_add["bet_slips_lost"] = row["bet_slips_lost"]

            for editor_map in editor_bet_slip_map:
                if editor_map["editor_ID"] == editor["editor_ID"]:
                    editor_to_add["bet_slips"] = editor_map["bet_slips"]

            for suggested_map in suggested_bet_map:
                if suggested_map["editor_ID"] == editor["editor_ID"]:
                    editor_to_add["suggested_bets"] = suggested_map["suggested_bets"]

            editor_final.append(editor_to_add)

        return {"editors": editor_final}
    
    elif info["request_type"] == "follow_editor":

        val = cursor.execute("INSERT INTO normal_user_follows (editor_ID, user_ID) VALUES ({0}, {1})".format(info["editor_ID"],
                                                                                             info["user_ID"]))

        sql.connection.commit()

        if val > 0:
            result = {
                "success": True
            }
        else:
            result = {
                "success": False
            }
        return jsonify({"result": result})

    elif info["request_type"] == "unfollow_editor":

        val = cursor.execute("DELETE FROM normal_user_follows WHERE user_ID = {0} AND editor_ID = {1}".format(info["user_ID"],
                                                                                              info["editor_ID"]))
        sql.connection.commit()
        if val > 0:
            result = {
                "success": True
            }
        else:
            result = {
                "success": False
            }
        return jsonify({"result": result})
    
    elif info["request_type"] == "play_editor_bet_slip":
  
        cursor.execute("SELECT match_ID, bet_ID FROM (SELECT match_ID, bet_ID FROM placed_on WHERE bet_slip_ID = {0})"
                    " bets NATURAL JOIN bet WHERE result = 'PENDING'".format(info["bet_slip_ID"]))

        editor_pending_bets_results = []

        editor_pending_bets_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            editor_pending_bets_results.append(dict(zip(editor_pending_bets_columns, row)))

        cursor.execute("WITH user_bet_slip AS (SELECT bet_slip_ID FROM bet_slip WHERE creator_ID = {0} AND isPlayed = FALSE)"
                    " SELECT match_ID, bet_ID FROM user_bet_slip NATURAL JOIN placed_on".format(info["user_ID"]))

        user_current_bets_results = []

        user_current_bets_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            user_current_bets_results.append(dict(zip(user_current_bets_columns, row)))

        for row in editor_pending_bets_results:

            bet_found = False

            for bet in user_current_bets_results:

                if bet["match_ID"] == row["match_ID"] and bet["bet_ID"] == row["bet_ID"]:
                    bet_found = True
                    break
            if not bet_found:
                cursor.execute("SELECT bet_slip_ID FROM bet_slip WHERE creator_ID = {0} AND isPlayed = FALSE"
                            .format(info["user_ID"]))

                user_bet_slip_id = cursor.fetchone()[0]

                if cursor.execute("INSERT INTO placed_on (bet_slip_ID, bet_ID, match_ID) VALUES ({0}, {1}, {2})"
                                       .format(user_bet_slip_id, row["bet_ID"], row["match_ID"])) > 0:

                    sql.connection.commit()

                else:
                    return {"status": "Could not add bet to user betslip."}
        return {"status": "success"}

    elif info["request_type"] == "like_comment":

        if cursor.execute("INSERT INTO like_comment (comment_ID, n_user_ID) VALUES ({0}, {1})"
                               .format(info["comment_ID"], info["user_ID"])) > 0:

            sql.connection.commit()
            return {"status": "success"}

        else:
            return {"status": "Could not like comment"}


@app.route('/admin/modify-raffle', methods=["GET", "POST"])
def admin_modify_raffle():

    cursor = sql.connection.cursor()

    info = request.get_json(force=True)

    if info["request_type"] == "add_item":

        if cursor.execute("INSERT INTO item_coupon(description, coupon_amount, coupon_count, sold_coupons) VALUES ('{0}', '{1}', '{2}', '{3}')"
                               .format(info["description"], info["coupon_amount"],
                                       info["coupon_count"], info["sold_coupons"])) > 0:
            sql.connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")

            last_item_id = cursor.fetchone()[0]
            return {"status" : "success"}

        else:
            return {"status": "Could not add to shop_item"}

    elif info["request_type"] == "display_all_items":

        cursor.execute("SELECT * FROM item_coupon")

        item_results = []

        item_results_columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            item_results.append(dict(zip(item_results_columns, row)))

        return {"items": item_results}

    # Needs to be updated ??
    elif info["request_type"] == "update_total_amount":

        if cursor.execute("SELECT item_ID FROM shop_item WHERE item_ID = {0}"
                               .format(info["selected_item_id"])) > 0:

            item_ID = cursor.fetchone()[0]

            if cursor.execute("UPDATE item_coupon SET coupon_amount = {0}"
                                   .format(info["new_amount"])) > 0:

                sql.connection.commit()
                return {"status": "success"}
            else:
                return {"status": "fail"}
        else:
            return {"status": "No item found"}

    # Needs to be updated ??
    elif info["request_type"] == "update_description":

        if cursor.execute("SELECT item_ID FROM item_coupons WHERE item_ID = {0}"
                               .format(info["selected_item_id"])) > 0:
            item_ID = cursor.fetchone()[0]

            if cursor.execute("UPDATE item_coupon SET description = {0}"
                                   .format(info["new_description"])) > 0:

                sql.connection.commit()
                return {"status": "success"}
            else:
                return {"status": "fail"}

    elif info["request_type"] == "remove_item":

        if cursor.execute("DELETE FROM item_coupon WHERE item_ID = {0}"
                               .format(info["selected_item_ID"])) > 0:

            sql.connection.commit()
            return {"status": "success"}
        else:
            return {"status": "Could not remove the item."}

@app.route('/raffle', methods=["GET", "POST"])
def raffle():
    cursor = sql.connection.cursor()

    info = request.get_json()

    # get request_type, user_id
    if info["request_type"] == "get_items":
        cursor.execute("SELECT * FROM item_coupon").format(input['user_ID'])
        val = cursor.fetchall()
        items = []

        for row in val:
            item = [{"item_ID": row[0],
                     "description": row[1],
                     "coupon_amount": row[2],
                     "coupon_count" : row[3],
                     "sold_coupons": row[4]}]
            items.append(item)

        result = {
            "items": items
        }
        return jsonify({"result": result})

    if info["request_type"] == "buy_item":

        cursor.execute("SELECT coupon_amount FROM item_coupon WHERE item_ID = {0}".format(info["item_ID"]))
        total_amount = cursor.fetchone()

        cursor.execute("SELECT balance FROM normal_user WHERE user_ID = {0}".format(info["user_ID"]))
        balance = cursor.fetchone()

        if total_amount[0] > balance[0]:
            result = {
                "success": False
            }
        else:
            new_balance = balance[0] - total_amount[0]
            cursor.execute("UPDATE normal_user SET balance = {0} WHERE user_ID = {1}".format(new_balance, info["user_ID"]))
            sql.connection.commit()

            result = {
                "success": True
            }

        return jsonify({"result": result})



    
        

app.run(debug=True)