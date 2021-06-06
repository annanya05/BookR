from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__, template_folder='template')

@app.route('/')
def main():
    return render_template('welcome.html')

@app.route('/user_register')
def new_user():
    return render_template('register.html')

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form.get('nm')
            age = request.form.get('no')
            sex = request.form.get('s')
            location = request.form.get('loc')
            username = request.form.get('us')
            password = request.form.get('ps')
            with sqlite3.connect('userdb.sqlite') as conn:
                cur = conn.cursor()
                cur.execute('''INSERT INTO User (Name, Age, Sex, Location, username, password) VALUES (?, ?, ?, ?, ?, ?)''', (name, age, sex, location, username, password,))
                conn.commit()
                msg = "Record added successfully."
        except:
            conn.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/user_login')
def log():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def user():
    msg = "msg"
    if request.method == 'POST':
        try:
            global username
            username = request.form.get('us')
            password = request.form.get('ps')
            with sqlite3.connect('userdb.sqlite') as conn:
                cur = conn.cursor()
                cur.execute('SELECT password FROM User WHERE username=?', (username,))
                result = cur.fetchone()
                if result is None:
                    msg = "No Record Found"
                    return render_template("error.html")
                else:
                    if password == result[0]:
                        return redirect('/profile.html')
                    else:
                        msg = "Incorrect password"
                        return render_template("logresult.html", msg=msg)
        except:
            conn.rollback()
            msg = "Error logging in."
        finally:
            conn.close()

@app.route('/profile.html', methods=['POST', 'GET'])
def profile():
        con = sqlite3.connect('userdb.sqlite')
        db = con.cursor()
        res = db.execute('select Name from User WHERE username=?', (username,))
        data = res.fetchone()
        return render_template('profile.html', data=data[0])

@app.route('/admin_register')
def areg():
    return render_template('AdminReg.html')

@app.route('/regi', methods=['POST', 'GET'])
def regi():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form.get('nm')
            admin_id = request.form.get('aid')
            password = request.form.get('ps')
            with sqlite3.connect('admindb.sqlite') as conn:
                cur = conn.cursor()
                cur.execute('''INSERT INTO Administrator (Name, admin_id, password) VALUES (?, ?, ?)''', (name, admin_id, password,))
                conn.commit()
                msg = "Record added successfully."
        except:
            conn.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/admin_login')
def alog():
    return render_template('AdminLogin.html')

@app.route('/index.html', methods=['POST', 'GET'])
def admin():
    msg = "msg"
    if request.method == 'POST':
        try:
            global admin_id
            admin_id = request.form.get('aid')
            password = request.form.get('ps')
            with sqlite3.connect('admindb.sqlite') as conn:
                cur = conn.cursor()
                cur.execute('SELECT password FROM Administrator WHERE admin_id=?', (admin_id,))
                result = cur.fetchone()
                if result is None:
                    msg = "No Record Found"
                    return render_template("error.html")
                else:
                    if password == result[0]:
                        return redirect("/AdminProfile.html")
                    else:
                        msg = "Incorrect password"
                        return render_template("logresult.html", msg=msg)
        except:
            conn.rollback()
            msg = "Error logging in."
        finally:
            conn.close()

@app.route('/AdminProfile.html', methods=['POST', 'GET'])
def apro():
    con = sqlite3.connect('admindb.sqlite')
    db = con.cursor()
    res = db.execute('select Name from Administrator WHERE admin_id=?', (admin_id,))
    data = res.fetchone()
    return render_template('AdminProfile.html', data=data[0])

@app.route('/error.html')
def err():
    return render_template('error.html')

@app.route('/AdminEdit.html')
def aedit():
    return render_template('AdminEdit.html')

@app.route('/Book.html', methods=['POST', 'GET'])
def books():
    con = sqlite3.connect('booklist.sqlite')
    db = con.cursor()
    res = db.execute('select * from Books_List')
    data = res.fetchall()
    return render_template('Book.html', data=data)

@app.route('/AddBook.html', methods=['POST', 'GET'])
def abook():
    return render_template("AddBook.html")

@app.route('/addb', methods=['POST', 'GET'])
def addb():
    msg = "msg"
    if request.method == "POST":
        try:
            book_id = request.form.get('bid')
            title = request.form.get('ti')
            with sqlite3.connect('bookdb.sqlite') as connA:
                cur = connA.cursor()
                cur.execute('''INSERT INTO Book (book_id, Title) VALUES (?, ?)''',
                            (book_id, title,))
                connA.commit()
                msg = "Book added successfully."
        except:
            connA.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)
    if request.method == "POST":
        try:
            au_name = request.form.get('an')
            with sqlite3.connect('authordb.sqlite') as connB:
                cur = connB.cursor()
                cur.execute('''INSERT INTO Author (Name) VALUES (?)''',
                            (au_name,))
                connB.commit()
                msg = "Book added successfully."
        except:
            connB.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)
    if request.method == "POST":
        try:
            b_rate = request.form.get('br')
            with sqlite3.connect('ratings (2).sqlite') as connC:
                cur = connC.cursor()
                cur.execute('''INSERT INTO Ratings (rating) VALUES (?)''',
                            (b_rate,))
                connC.commit()
                msg = "Book added successfully."
        except:
            connC.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/UserEdit.html')
def uedit():
    return render_template('UserEdit.html')

@app.route('/rating.html', methods=['POST', 'GET'])
def rati():
    return render_template("rating.html")

@app.route('/rate', methods=['POST', 'GET'])
def rate():
    msg = "msg"
    if request.method == "POST":
        try:
            book_id = request.form.get('bi')
            addR = request.form.get('ar')
            with sqlite3.connect('ratings (2).sqlite') as conn:
                cur = conn.cursor()
                cur.execute('''INSERT INTO Ratings (book_id, rating) VALUES (?, ?)''',
                            (book_id, addR,))
                conn.commit()
                msg = "Rating added successfully."
        except:
            conn.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/search.html', methods=['GET', 'POST'])
def search():
    con = sqlite3.connect('recommendations (1).sqlite')
    db = con.cursor()
    res = db.execute('select * from Recommendation_List')
    data1 = res.fetchall()
    return render_template('profile.html', data1=data1)


if __name__ == '__main__':
    app.run()