from flask import Flask, request, render_template,flash,redirect,session,abort,jsonify,url_for
import sqlite3
from models import Model
import os

app = Flask(__name__)

con=sqlite3.connect("base1.db")
con.execute("create table if not exists users(pid integer primary key,name text,address text,contact integer,mail text)")
con.close()


@app.route('/')
def index():
    return render_template('login.html')

# def root():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return render_template('index.html')


# @app.route('/login', methods=['POST'])
# def do_admin_login():
#     if request.form['password'] == 'admin' and request.form['username'] == 'admin':
#         session['logged_in'] = True
#     else :
#         flash('wrong password!')
#     return root()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("base1.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where name=? and contact=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"] = data["name"]
            session["contact"] = data["contact"]
            return redirect(url_for("user"))
        else:
            flash("Username and Password Mismatch", "danger")
    return redirect(url_for("index"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("base1.db")
            cur=con.cursor()
            cur.execute("insert into users(name, address, contact, mail)values(?,?,?,?)",(name,address,contact,mail))
            con.commit()
            flash("Record Added Successfully", "success")
        except:
            flash("Error in Insert Operation", "danger")
        finally:
            return redirect(url_for("index"))
            con.close()
    return render_template('register.html')


@app.route('/user',methods=["GET","POST"])
def user():
    return render_template("index.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

# @app.route("/logout")
# def logout():
#     session['logged_in'] = False
#     return root()


@app.route('/predict', methods=["POST"])
def predict():
    q1 = int(request.form['a1'])
    q2 = int(request.form['a2'])
    q3 = int(request.form['a3'])
    q4 = int(request.form['a4'])
    q5 = int(request.form['a5'])
    q6 = int(request.form['a6'])
    q7 = int(request.form['a7'])
    q8 = int(request.form['a8'])
    q9 = int(request.form['a9'])
    q10 = int(request.form['a10'])

    values = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    model = Model()
    classifier = model.svm_classifier()
    prediction = classifier.predict([values])
    if prediction[0] == 0:
            result = 'Your Depression test result : No Depression'
    if prediction[0] == 1:
            result = 'Your Depression test result : Mild Depression'
    if prediction[0] == 2:
            result = 'Your Depression test result : Moderate Depression'
    if prediction[0] == 3:
            result = 'Your Depression test result : Moderately severe Depression'
    if prediction[0] == 4:
            result = 'Your Depression test result : Severe Depression'
    return render_template("result.html", result=result)

app.secret_key = os.urandom(12)
app.run(port=3000, host='127.0.0.1', debug=True)