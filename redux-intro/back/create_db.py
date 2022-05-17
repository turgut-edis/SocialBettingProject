import mysql.connector

''' mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd = "password123"
)
my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE db_project") '''

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd = "password123",
  db = "db_project"
)
my_cursor = mydb.cursor()


my_cursor.execute("DROP TABLE IF EXISTS buys, edits, shared_slip, like_comment, \
                   plays, banned_editors, placed_on, banned_users, competitor_contest, \
                   bet_slip_comment, match_comment, team, esports_team, competitors,\
                   lol_results, football_results, basketball_results, volleyball_results,\
                   results, item_coupon, comments, bet_slip_like, bet_slip, suggested_bet, bet, matches, contest,\
                   sports, editor_request, normal_user_follows, normal_user_friend,\
                   editor, normal_user, slip_creator, admin, user")


#student_Table = "CREATE TABLE student " + "(sid CHAR(12)," + "sname VARCHAR(50) NOT NULL," + "bdate DATE NOT NULL," + "address VARCHAR(50) NOT NULL," + "scity VARCHAR(20) NOT NULL," + "year CHAR(20) NOT NULL," + "gpa FLOAT NOT NULL," + "nationality VARCHAR(20) NOT NULL," + "PRIMARY KEY(sid))"

user = "CREATE TABLE user( user_ID INT AUTO_INCREMENT, username VARCHAR(16) NOT NULL UNIQUE, password VARCHAR(16) NOT NULL, name VARCHAR(20) NOT NULL, surname VARCHAR(20) NOT NULL, birth_year INT NOT NULL, mail VARCHAR(255) NOT NULL UNIQUE, PRIMARY KEY(user_ID) )"

normal_user = "CREATE TABLE normal_user( n_user_ID INT, balance INT, winning_cnt INT, address VARCHAR (2000), coupons INT, PRIMARY KEY (n_user_ID), FOREIGN KEY (n_user_ID) REFERENCES slip_creator(creator_ID) ON DELETE CASCADE )"

normal_user_friend = "CREATE TABLE normal_user_friend( user_ID INT, friend_ID INT, PRIMARY KEY (user_ID, friend_ID), FOREIGN KEY (user_ID) REFERENCES normal_user(n_user_ID) ON DELETE CASCADE, FOREIGN KEY (friend_ID) REFERENCES normal_user(n_user_ID) ON DELETE CASCADE )"

normal_user_follows = "CREATE TABLE normal_user_follows( \
                                    editor_ID INT, \
                                    user_ID INT, \
                                    PRIMARY KEY (editor_ID, user_ID), \
                                    FOREIGN KEY (editor_ID) REFERENCES \
                                    editor(editor_ID) ON DELETE CASCADE, \
                                    FOREIGN KEY (user_ID) REFERENCES \
                                    normal_user(n_user_ID) ON DELETE CASCADE \
                                    )"

editor = "CREATE TABLE editor( \
editor_ID INT, \
win_rate INT, \
winning_cnt INT, \
PRIMARY KEY (editor_ID), \
FOREIGN KEY (editor_ID) REFERENCES \
slip_creator(creator_ID) ON DELETE CASCADE \
)"

editor_request = "CREATE TABLE editor_request(\
editor_ID INT, \
status VARCHAR(10), \
PRIMARY KEY (editor_ID), \
FOREIGN KEY (editor_ID) REFERENCES \
editor(editor_ID)\
ON DELETE CASCADE ON UPDATE CASCADE, \
CHECK( status IN ( 'APPROVED', 'PENDING' ) ) \
)"

slip_creator = "CREATE TABLE slip_creator(\
creator_ID INT, \
PRIMARY KEY (creator_ID), \
FOREIGN KEY (creator_ID) REFERENCES \
user(user_ID)\
ON DELETE CASCADE ON UPDATE CASCADE \
)"

admin = "CREATE TABLE admin( \
admin_ID INT, \
PRIMARY KEY (admin_ID), \
FOREIGN KEY (admin_ID) REFERENCES \
user(user_ID) ON DELETE CASCADE \
)"

bet = "CREATE TABLE bet( bet_ID INT AUTO_INCREMENT, match_ID INT, mbn INT, ratio FLOAT (2,2), change_date TIMESTAMP, bet_type VARCHAR(30), active BOOLEAN, result VARCHAR(10), PRIMARY KEY (bet_ID, match_ID), FOREIGN KEY (match_ID) REFERENCES matches(match_ID) ON DELETE CASCADE ON UPDATE CASCADE, CHECK (result IN ('WON', 'LOST', 'PENDING')) )"

bet_slip = "CREATE TABLE bet_slip(\
bet_slip_ID INT AUTO_INCREMENT, \
creator_ID INT, \
bet_count INT, \
total_amount INT, \
isPlayed BOOLEAN, \
PRIMARY KEY (bet_slip_ID), \
FOREIGN KEY (creator_ID) REFERENCES slip_creator(creator_ID) \
)"

comments = "CREATE TABLE comments( \
comment_ID INT AUTO_INCREMENT, \
user_ID INT, \
comment VARCHAR(20000), \
comment_date TIMESTAMP, \
like_count INT, \
PRIMARY KEY (comment_ID), \
FOREIGN KEY(user_ID) REFERENCES \
user(user_ID) ON DELETE CASCADE ON UPDATE \
CASCADE \
)"

item_coupon = "CREATE TABLE item_coupon( \
item_ID INT AUTO_INCREMENT, \
description VARCHAR(2000), \
coupon_amount INT, \
coupon_count INT, \
sold_coupons INT, \
PRIMARY KEY (item_ID) \
)"

matches = "CREATE TABLE matches( \
match_ID INT AUTO_INCREMENT, \
start_date TIMESTAMP, \
contest_ID INT, \
season VARCHAR(20), \
sport_name VARCHAR(15), \
PRIMARY KEY(match_ID), \
FOREIGN KEY(contest_ID, season, sport_name) \
REFERENCES contest(contest_ID, season, \
sport_name) ON DELETE CASCADE ON UPDATE \
CASCADE, \
FOREIGN KEY(sport_name) REFERENCES \
sports(sport_name) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

results = "CREATE TABLE results( \
result_ID INT AUTO_INCREMENT, \
match_ID INT, \
home_score INT, \
away_score INT, \
PRIMARY KEY(result_ID), \
FOREIGN KEY(match_ID) REFERENCES \
matches(match_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

volleyball_results = "CREATE TABLE volleyball_results( \
v_result_ID INT, \
total_score INT, \
home_set_score INT, \
away_set_score INT, \
PRIMARY KEY(v_result_ID), \
FOREIGN KEY (v_result_ID) REFERENCES \
results(result_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

basketball_results = "CREATE TABLE basketball_results( \
b_result_ID INT, \
home_half_score INT, \
away_half_score INT, \
home_total_rebound_score INT, \
away_total_rebound_score INT, \
PRIMARY KEY(b_result_ID), \
FOREIGN KEY (b_result_ID) REFERENCES \
results(result_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

football_results = "CREATE TABLE football_results( \
f_result_ID INT, \
yellow_card_num INT, \
red_card_num INT, \
corner_cnt INT, \
first_half_home_goals INT, \
first_half_away_goals INT, \
PRIMARY KEY(f_result_ID), \
FOREIGN KEY (f_result_ID) REFERENCES \
results(result_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

lol_results = "CREATE TABLE lol_results(\
l_result_ID INT, \
winner_side VARCHAR(4), \
elder_dragon_side VARCHAR(4), \
baron_side VARCHAR(4), \
soul_side VARCHAR(4), \
first_tower_side VARCHAR(4), \
first_blood_side VARCHAR(4), \
PRIMARY KEY(l_result_ID), \
FOREIGN KEY (l_result_ID) REFERENCES \
results(result_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
CHECK(winner_side IN ('HOME', 'AWAY')), \
CHECK(elder_dragon_side IN ('HOME', 'AWAY')), \
CHECK(baron_side IN ('HOME', 'AWAY')), \
CHECK(soul_side IN ('HOME', 'AWAY')), \
CHECK(first_tower_side IN ('HOME', 'AWAY')), \
CHECK(first_blood_side IN ('HOME', 'AWAY')) \
)"

esports_team = "CREATE TABLE esports_team( \
competitor_ID INT, \
PRIMARY KEY(competitor_ID), \
FOREIGN KEY (competitor_ID) REFERENCES \
competitors(competitor_ID) ON DELETE CASCADE \
ON UPDATE CASCADE \
)" 


team = "CREATE TABLE team( \
competitor_ID INT, \
name VARCHAR(50) NOT NULL, \
location VARCHAR(200) NOT NULL, \
PRIMARY KEY(competitor_ID), \
FOREIGN KEY (competitor_ID) REFERENCES \
competitors(competitor_ID) ON DELETE CASCADE \
ON UPDATE CASCADE \
)"

sports = "CREATE TABLE sports( \
sport_name VARCHAR(15), \
PRIMARY KEY(sport_name) \
)"

contest = "CREATE TABLE contest( \
contest_ID INT AUTO_INCREMENT, \
sport_name VARCHAR(15), \
name VARCHAR(30), \
season VARCHAR(20), \
PRIMARY KEY (contest_ID, sport_name, season), \
FOREIGN KEY (sport_name) REFERENCES \
sports(sport_name) ON DELETE CASCADE ON UPDATE CASCADE \
)"

competitors = "CREATE TABLE competitors( \
competitor_ID INT AUTO_INCREMENT, \
team_name VARCHAR(50), \
win_rate FLOAT, \
colors VARCHAR(30), \
coach_name VARCHAR(2000), \
estab_date INT, \
PRIMARY KEY(competitor_ID) \
)"

match_comment = "CREATE TABLE match_comment( \
match_ID INT, \
comment_ID INT, \
PRIMARY KEY(match_ID, comment_ID), \
FOREIGN KEY(match_ID) REFERENCES \
matches(match_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY(comment_ID) REFERENCES \
comments(comment_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

bet_slip_comment = "CREATE TABLE bet_slip_comment( \
comment_ID INT, \
bet_slip_ID INT, \
PRIMARY KEY(comment_ID, bet_slip_ID), \
FOREIGN KEY(comment_ID) REFERENCES \
comments(comment_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY(bet_slip_ID) REFERENCES \
bet_slip(bet_slip_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"



suggested_bet = "CREATE TABLE suggested_bet( \
editor_ID INT, \
bet_ID INT, \
match_ID INT, \
comment VARCHAR(2000), \
PRIMARY KEY(editor_ID, bet_ID), \
FOREIGN KEY(editor_ID) REFERENCES editor(editor_ID) ON DELETE CASCADE ON UPDATE CASCADE, \
FOREIGN KEY(bet_ID, match_ID) REFERENCES bet(bet_ID, match_ID) ON DELETE CASCADE ON UPDATE CASCADE \
)"

competitor_contest = "CREATE TABLE competitor_contest( \
competitor_ID INT, \
contest_ID INT, \
sport_name VARCHAR(15), \
season VARCHAR(20), \
points INT, \
PRIMARY KEY(competitor_ID, contest_ID, season), \
FOREIGN KEY (competitor_ID) REFERENCES \
competitors(competitor_ID) ON DELETE CASCADE \
ON UPDATE CASCADE, \
FOREIGN KEY(contest_ID, sport_name, season) REFERENCES \
contest(contest_ID, sport_name, season) ON DELETE CASCADE \
ON UPDATE CASCADE \
)"

banned_users = "CREATE TABLE banned_users( \
admin_ID INT, \
n_user_ID INT, \
PRIMARY KEY(admin_ID, n_user_ID), \
FOREIGN KEY(admin_ID) REFERENCES \
admin(admin_ID) ON DELETE CASCADE, \
FOREIGN KEY(n_user_ID) REFERENCES \
normal_user(n_user_ID) ON DELETE CASCADE \
)"

placed_on = "CREATE TABLE placed_on( \
bet_slip_ID INT, \
bet_ID INT, \
match_ID INT, \
PRIMARY KEY(bet_slip_ID, match_ID), \
FOREIGN KEY(bet_slip_ID) REFERENCES \
bet_slip(bet_slip_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY(bet_ID, match_ID) REFERENCES \
bet(bet_ID, match_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY(match_ID) REFERENCES \
matches(match_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

banned_editors = "CREATE TABLE banned_editors( \
admin_ID INT, \
editor_ID INT, \
PRIMARY KEY(admin_ID, editor_ID), \
FOREIGN KEY(admin_ID) REFERENCES \
admin(admin_ID) ON DELETE CASCADE, \
FOREIGN KEY(editor_ID) REFERENCES \
editor(editor_ID) ON DELETE CASCADE \
)"


plays = "CREATE TABLE plays( \
match_ID INT, \
competitor_ID INT, \
side VARCHAR(4), \
PRIMARY KEY(match_ID, competitor_ID), \
FOREIGN KEY(match_ID) REFERENCES \
matches(match_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY (competitor_ID) REFERENCES \
competitors(competitor_ID) ON DELETE CASCADE \
ON UPDATE CASCADE, \
CHECK ( side IN ( 'HOME', 'AWAY' ) ) \
) \
"

like_comment = "CREATE TABLE like_comment( \
comment_ID INT, \
n_user_ID INT, \
PRIMARY KEY(comment_ID, n_user_ID), \
FOREIGN KEY(n_user_ID) REFERENCES \
normal_user(n_user_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY (comment_ID) REFERENCES \
comments(comment_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)" \

bet_slip_like = "CREATE TABLE bet_slip_like( \
n_user_ID INT, \
bet_slip_ID INT, \
PRIMARY KEY(n_user_ID, bet_slip_ID), \
FOREIGN KEY(n_user_ID) REFERENCES normal_user(n_user_ID) ON DELETE CASCADE ON UPDATE CASCADE, \
FOREIGN KEY(bet_slip_ID) REFERENCES bet_slip(bet_slip_ID) ON DELETE CASCADE ON UPDATE CASCADE)"

shared_slip = "CREATE TABLE shared_slip( \
bet_slip_ID INT, \
sharer_ID INT, \
PRIMARY KEY(bet_slip_ID, sharer_ID), \
FOREIGN KEY(bet_slip_ID) REFERENCES \
bet_slip(bet_slip_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY (sharer_ID) REFERENCES \
slip_creator(creator_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
)"

edits = "CREATE TABLE edits( \
admin_ID INT, \
bet_ID INT, \
match_ID INT, \
PRIMARY KEY(admin_ID, bet_ID, match_ID), \
FOREIGN KEY (admin_ID) REFERENCES \
admin(admin_ID) ON DELETE CASCADE ON \
UPDATE CASCADE, \
FOREIGN KEY(bet_ID, match_ID) REFERENCES \
bet(bet_ID, match_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
) \
"

buys = "CREATE TABLE buys( \
item_ID INT, \
n_user_ID INT, \
PRIMARY KEY(item_ID, n_user_ID), FOREIGN \
KEY(item_ID) REFERENCES item_coupon(item_ID) \
ON DELETE CASCADE ON UPDATE CASCADE, \
FOREIGN KEY(n_user_ID) REFERENCES \
normal_user(n_user_ID) ON DELETE CASCADE ON \
UPDATE CASCADE \
) \
"

my_cursor.execute(user)
my_cursor.execute(admin)
my_cursor.execute(slip_creator)
my_cursor.execute(normal_user)
my_cursor.execute(editor)
my_cursor.execute(normal_user_friend)
my_cursor.execute(normal_user_follows)
my_cursor.execute(editor_request)
my_cursor.execute(sports)
my_cursor.execute(contest)
my_cursor.execute(matches)
my_cursor.execute(bet)
my_cursor.execute(suggested_bet)
my_cursor.execute(bet_slip)
my_cursor.execute(bet_slip_like)
my_cursor.execute(comments)
my_cursor.execute(item_coupon)
my_cursor.execute(results)
my_cursor.execute(volleyball_results)
my_cursor.execute(basketball_results)
my_cursor.execute(football_results)
my_cursor.execute(lol_results)
my_cursor.execute(competitors)
my_cursor.execute(esports_team)
my_cursor.execute(team)
my_cursor.execute(match_comment)
my_cursor.execute(bet_slip_comment)
my_cursor.execute(competitor_contest)
my_cursor.execute(banned_users)
my_cursor.execute(placed_on)
my_cursor.execute(banned_editors)
my_cursor.execute(plays)
my_cursor.execute(like_comment)
my_cursor.execute(shared_slip)
my_cursor.execute(edits)
my_cursor.execute(buys)

my_cursor.execute("INSERT INTO user(username, password, name, surname, birth_year, mail) VALUES ('admin', 'admin', 'admin', 'admin', 0, 'admin@gmail.com')")
mydb.commit()
my_cursor.execute("INSERT INTO admin(admin_ID) VALUES (1)")
mydb.commit()



