import os
from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
from database import db
from models import User as User
from models import Balance, Expense, Purchase, Income
from forms import LoginForm, RegisterForm, BalanceForm, IncomeForm
import bcrypt
import altair as alt
import pandas as pd


def generate_chart(df, start_date, end_date):
    # Filter the dataframe based on the selected date range
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Define the selection for date range
    date_range_selector = alt.selection(type='interval', encodings=['x'])

    # Create the line chart
    line_chart = alt.Chart(df).mark_line().encode(
        x='date:T',
        y='balance:Q',
        tooltip=['date:T', 'balance:Q']
    ).add_selection(date_range_selector).transform_filter(date_range_selector)

    # Create the area chart to show the selected date range
    area_chart = alt.Chart(df).mark_area(opacity=0.3).encode(
        x='date:T',
        y='balance:Q',
    ).transform_filter(date_range_selector)

    # Combine the line chart and area chart
    chart = (line_chart + area_chart).properties(
        width=600,
        height=400,
        title='Account Balance'
    )

    return chart

def create_app(config_name):
    app = Flask(__name__)

    if config_name == 'production':
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget_all.db"
        app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'SE3155'
    elif config_name == 'test':
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'SE3155'

    # Dynamically bind SQLAlchemy to application
    db.init_app(app)

    with app.app_context():
        db.create_all()

        @app.route("/")
        @app.route("/index")
        def index():
            if session.get('user'):
                # grabs balance and income from last submitted entry
                balance = Balance.query.filter_by(user_id=session['user_id']).order_by(Balance.bal_at.desc()).first()
                income = Income.query.filter_by(user_id=session['user_id']).order_by(Income.inc_at.desc()).first()
                # grabs all balance history to create chart
                balance_history = Balance.query.filter_by(user_id=session['user_id']).order_by(Balance.bal_at.asc()).all()
                # create dataframe for use with altair
                df = pd.DataFrame([(b.bal_at, b.bal) for b in balance_history], columns=['date', 'balance'])

                time_range = request.args.get('time_range')

                # create filters for each dropdown option, pandas date offset makes this very easy
                if time_range == '1_week':
                    start_date = pd.Timestamp.now() - pd.DateOffset(weeks=1)
                    end_date = pd.Timestamp.now()
                elif time_range == '1_month':
                    start_date = pd.Timestamp.now() - pd.DateOffset(months=1)
                    end_date = pd.Timestamp.now()
                elif time_range == '6_months':
                    start_date = pd.Timestamp.now() - pd.DateOffset(months=6)
                    end_date = pd.Timestamp.now()
                elif time_range == '1_year':
                    start_date = pd.Timestamp.now() - pd.DateOffset(years=1)
                    end_date = pd.Timestamp.now()
                else:
                    start_date = df['date'].min()
                    end_date = df['date'].max()

                # call generate_chart to create chart
                chart = generate_chart(df, start_date, end_date)
                # turn chart data into json for html formatting
                chart_json = chart.to_json()
                return render_template('index.html', user=session['user'], balance=balance, income=income,
                                       chart=chart_json)
            return render_template("index.html")

        @app.route("/set_balance", methods=['POST', 'GET'])
        def set_balance():
            form = BalanceForm()

            if session.get('user'):
                if request.method == "POST" and form.validate_on_submit():
                    bal = request.form['balance']
                    new_record = Balance(bal, session['user_id'])
                    db.session.add(new_record)
                    db.session.commit()
                    latest_balance = Balance.query.filter_by(user_id=session['user_id']).order_by(
                        Balance.bal_at.desc()).first()

                    return redirect(url_for('index', balance=latest_balance))
                return render_template("set_balance.html", user=session['user'], form=form)
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

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
                # give new users 0 balance
                bal = 0
                new_balance = Balance(bal, session['user_id'])
                db.session.add(new_balance)
                db.session.commit()
                # Give new users 0 income
                inc = 0
                new_income = Income(inc, session['user_id'])
                db.session.add(new_income)
                db.session.commit()
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

        @app.route('/view_expenses', methods=['POST', 'GET'])
        def view_expenses():
            if session.get('user'):
                expenses = Expense.query.filter_by(user_id=session['user_id'])
                return render_template("view_expenses.html", user=session['user'], expenses=expenses)
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

        @app.route('/add_expenses', methods=['POST', 'GET'])
        def add_expenses():
            if request.method == 'POST':
                exp_name = request.form.get('expense_description')
                exp = request.form.get('expense_amount')
                if float(exp) < 0:
                    flash('Expense amount cannot be negative')
                    return redirect(url_for('view_expenses'))
                exp_cat = request.form.get('expense_category')
                new_exp = Expense(exp_name=exp_name,
                                  exp=exp,
                                  exp_cat=exp_cat,
                                  user_id=session['user_id']
                                  )
                db.session.add(new_exp)
                db.session.commit()
                expenses = Expense.query.filter_by(user_id=session['user_id'])
                return render_template("view_expenses.html", user=session['user'], expenses=expenses)
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

        @app.route("/set_income", methods=['POST', 'GET'])
        def set_income():
            form = IncomeForm()

            if session.get('user'):
                if request.method == "POST" and form.validate_on_submit():
                    inc = request.form['income']
                    new_record = Income(inc, session['user_id'])
                    db.session.add(new_record)
                    db.session.commit()
                    latest_income = Income.query.filter_by(user_id=session['user_id']).order_by(
                        Income.inc_at.desc()).first()

                    return redirect(url_for('index', income=latest_income))
                return render_template("set_income.html", user=session['user'], form=form)
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

        @app.route('/total_income', methods=['POST', 'GET'])
        def total_income():
            if session.get('user'):
                user_id = session['user_id']
                balance = Balance.query.filter_by(user_id=user_id).order_by(Balance.bal_at.desc()).first()
                income = Income.query.filter_by(user_id=user_id).order_by(Income.inc_at.desc()).first()
                income_value = round(float(income.inc) / 26, 2)
                return render_template("total_income.html", user=session['user'], balance=balance.bal if balance else 0,
                                       income=income_value if income else 0)
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

        @app.route('/delete/<int:id>', methods=['POST', 'GET'])
        def delete_expense(id):
            expense_to_delete = Expense.query.get_or_404(id)

            db.session.delete(expense_to_delete)
            db.session.commit()
            flash("Expense Deleted Successfully")
            expenses = Expense.query.filter_by(user_id=session['user_id'])
            return render_template("view_expenses.html", user=session['user'], expenses=expenses)
        
        @app.route('/update/<int:id>', methods=['POST', 'GET'])
        def update_expense(id):
            session.query(Expense)
            exp_name = request.form.get('update_exp_name'),
            exp = request.form.get('update_exp'),
            exp_cat = request.form.get('update_exp_cat')
            db.session.commit()
            expenses = Expense.query.filter_by(user_id=session['user_id'])
            return render_template("view_expenses.html", user=session['user'], expenses=expenses)

        @app.route('/purchases')
        def purchases():
            if session.get('user'):
                purchases = Purchase.query.filter_by(user_id=session['user_id'])
                return render_template("purchases.html", user=session['user'], purchases=purchases)
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

        @app.route('/add_purchases', methods=['POST', 'GET'])
        def add_purchases():
            if session.get('user'):
                if request.method == 'POST':
                    pur_name = request.form.get('product_name')
                    pur = request.form.get('product_amount')
                    if float(pur) < 0:
                        flash('Purchase amount cannot be negative')
                        return redirect(url_for('purchases'))
                    new_pur = Purchase(pur_name=pur_name,
                                       pur=pur,
                                       user_id=session['user_id']
                                       )
                    db.session.add(new_pur)
                    db.session.commit()
                    purchases = Purchase.query.filter_by(user_id=session['user_id'])
                    return redirect(url_for('purchases', user=session['user'], purchases=purchases))
                return render_template("add_purchases.html", user=session['user'])
            else:
                login_form = LoginForm()
                return render_template('login.html', form=login_form)

        @app.route('/advice')
        def advice():
            if session.get('user'):
                return render_template("advice.html", user=session['user'])
            return render_template("advice.html")

        return app


if __name__ == "__main__":
    app = create_app('production')
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)