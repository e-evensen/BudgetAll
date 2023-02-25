# Nick Warren Git comment
from datetime import datetime
import os
from flask import Flask
from flask import render_template, request, redirect, url_for, session
from database import db
from models import User as User
from models import Balance as Balance
from forms import LoginForm, RegisterForm, BalanceForm
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_all.db'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/index")
def index():
    # check if a user is saved in a session
    if session.get('user'):
        balance = Balance.query.filter_by(user_id=session['user_id']).order_by(Balance.bal_at.desc()).first()
        return render_template('index.html', user=session['user'], balance=balance)
    return render_template("index.html")


@app.route("/update_balance", methods=['POST', 'GET'])
def update_balance():
    form = BalanceForm()

    if session.get('user'):
        if request.method == "POST" and form.validate_on_submit():
            bal = request.form['balance']
            new_record = Balance(bal, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            latest_balance = Balance.query.filter_by(user_id=session['user_id']).order_by(Balance.bal_at.desc()).first()

            return redirect(url_for('index', balance=latest_balance))
        return render_template("update_balance.html", user=session['user'], form=form)
    else:
        return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        username = request.form['username']
        # create user model
        new_user = User(username, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = username
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('index'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.username
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('index'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in a session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))

@app.route('/calculator', methods=['POST', 'GET'])
def calculator():
    if session.get('user'):
        return render_template("calculator.html", user=session['user'])
    return render_template("calculator.html")


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
