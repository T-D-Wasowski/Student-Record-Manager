import sqlite3

def main():
    pass
    #conn, cur = connectDB()

    #dropTable(conn, cur)
    #createTable(conn, cur)

    #conn.close()

#----- TESTS -----

    #add("Gwen", "Maple", "56", "Images/test.jpg")
    #update("1", "Stanley", "Bridget", "14", "Images/NotDawid.jpg", "0")
    #delete(3)
    #search("", "Dawid", "", "", "")
    #view()

#----- DATABASE FUNCTIONS -----

def connectDB():
    
    conn = sqlite3.connect("studentRecords.db")
    cur = conn. cursor()

    return conn, cur

def createTable(conn, cur):

    cur.execute("CREATE TABLE IF NOT EXISTS student (\
        stdntID INTEGER PRIMARY KEY AUTOINCREMENT, \
        stdntFirstName VARCHAR(25) NOT NULL CHECK(stdntFirstName!=''), \
        stdntLastName VARCHAR(25) NOT NULL CHECK(stdntLastName!=''), \
        stdntMark INTEGER NOT NULL CHECK(stdntMark!=''), \
        stdntImgLoc VARCHAR(25), \
        stdntStatus BOOLEAN NOT NULL DEFAULT 1)")
    conn.commit() 

def dropTable(conn, cur):

    cur.execute("DROP TABLE IF EXISTS student")
    conn.commit()

#----- CRUD FUNCTIONS -----

def view():

    conn, cur = connectDB()

    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()

    return rows

    conn.close()

def add(name, surname, mark, img): #might need to insert 'stat' parameter

    conn, cur = connectDB()

    cur.execute("INSERT INTO student(stdntID, stdntFirstName, stdntLastName, \
        stdntMark, stdntImgLoc) VALUES(NULL,?,?,?,?)", (name, surname, mark, img))
    conn.commit()

    conn.close()

def update(id, name, surname, mark, img, stat):

    conn, cur = connectDB()

    cur.execute("UPDATE student SET stdntFirstName=?, stdntLastName=?, \
        stdntMark=?, stdntImgLoc=?, stdntStatus=? WHERE stdntID=?",
        (name, surname, mark, img, stat, id))
    conn.commit()

    conn.close()

def delete(id):

    conn, cur = connectDB()

    cur.execute("DELETE FROM student WHERE stdntID=?", (id,))
    conn.commit()

    conn.close()

def search(id, name, surname, mark, stat):

    conn, cur = connectDB()

    cur.execute("SELECT * FROM student WHERE stdntID=? OR stdntFirstName=? \
        OR stdntLastName=? OR stdntMark=? OR stdntStatus=?",
        (id, name, surname, mark, stat))
    rows=cur.fetchall()

    return rows

    conn.close()

main()
