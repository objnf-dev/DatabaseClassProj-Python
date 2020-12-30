from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


# Homepage
@routes.route('/')
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template('index.html')


# Login
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if utils.database.checkLogin(utils.database.DBConn, request.form['username'], request.form['password']):
            session["user"] = request.form['username']
            return redirect("/")
        else:
            abort(401)
