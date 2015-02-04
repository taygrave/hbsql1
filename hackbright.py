import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def query_by_title(proj_title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (proj_title,))
    row = DB.fetchone()
    print """%s: %s where the maximum grade is %d.""" %(row[1], row[2], row[3])

def add_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?,?,?) """
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % (title)

def get_grade(github, proj_title):
    query = """SELECT Students.first_name, Students.last_name, Grades.project_title, Grades.grade FROM Students INNER JOIN Grades ON (Students.github=Grades.student_github) WHERE Students.github = ? AND project_title=?"""
    DB.execute(query, (github, proj_title))
    row = DB.fetchone()
    print """Student %s %s received %d points on the %s project""" %(row[0], row[1], row[3], row[2])

def give_grade(github, proj_title, grade):
    grade = int(grade)
    query = """INSERT INTO Grades VALUES (?,?,?)"""
    DB.execute(query, (github, proj_title, grade))
    CONN.commit()
    print "Student %s was successfully assigned %d points for %s." %(github, grade, proj_title)

def student_grades(github):
    query = """SELECT s.first_name, s.last_name, p.title,g.grade FROM Students AS s JOIN Grades AS g ON (s.github = g.student_github) JOIN Projects AS p ON (p.title=g.project_title) WHERE s.github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    print row #(u'Katie', u'Kicksit', u'Blockly', 79)
    print """Report Card for %s %s""" %(row[0][0], row[0][1])
    print "*" * 20
    for i in row:
        f_name, l_name, proj, score = i
        print score, ":", proj

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_project":
            query_by_title(*args)
        elif command == "add_project":
            add_project(*args)
        elif command == "get_grade":
            get_grade(*args)
        elif command == "grade":
            give_grade(*args)
        elif command == "report_card":
            student_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()

