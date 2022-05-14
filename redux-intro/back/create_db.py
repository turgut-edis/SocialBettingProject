import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd = "password123",
  db="our_users",
)

#my_cursor.execute("CREATE DATABASE our_users")

my_cursor = mydb.cursor()


#student_Table = "CREATE TABLE student " + "(sid CHAR(12)," + "sname VARCHAR(50) NOT NULL," + "bdate DATE NOT NULL," + "address VARCHAR(50) NOT NULL," + "scity VARCHAR(20) NOT NULL," + "year CHAR(20) NOT NULL," + "gpa FLOAT NOT NULL," + "nationality VARCHAR(20) NOT NULL," + "PRIMARY KEY(sid))"

user = "CREATE TABLE user( user_ID INT, username VARCHAR(16) NOT NULL UNIQUE, password VARCHAR(16) NOT NULL, name VARCHAR(20) NOT NULL, surname VARCHAR(20) NOT NULL, birth_year INT NOT NULL, mail VARCHAR(255) NOT NULL UNIQUE, PRIMARY KEY(user_ID) )"

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
admin_ID INT, \
status VARCHAR(10), \
PRIMARY KEY (editor_ID), \
FOREIGN KEY (admin_ID) REFERENCES \
admin(admin_ID)\
ON DELETE CASCADE ON UPDATE CASCADE, \
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



my_cursor.execute(user)
my_cursor.execute(admin)
my_cursor.execute(slip_creator)
my_cursor.execute(normal_user)
my_cursor.execute(editor)
my_cursor.execute(normal_user_friend)
my_cursor.execute(normal_user_follows)
my_cursor.execute(editor_request)




