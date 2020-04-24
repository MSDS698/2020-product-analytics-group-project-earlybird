from app import application, classes, db
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user
import numpy as np
import pandas as pd
import boto3

from flask_bootstrap import Bootstrap



@application.route('/index')
@application.route('/')
def index():

   return render_template('index.html', authenticated_user=current_user.is_authenticated)

@application.route('/register', methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data
        ##################################
        #### UPDATE THIS (EXERCISE 1) ####
        ##################################
        user_count = classes.User.query.filter_by(username=username).count() + classes.User.query.filter_by(email=email).count()
        if (user_count == 0):
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('question'))
        else:
            flash('Username or Email already exist!')
    return render_template('register.html', form=registration_form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = classes.User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username and password combination!')

    return render_template('login.html', form=login_form, authenticated_user=current_user.is_authenticated)



@application.route('/question', methods=['GET', 'POST'])
def question():
    question_form = classes.QuestionForm()
    if question_form.validate_on_submit():
        age = question_form.age.data
        gender = question_form.gender.data
        marriage = question_form.marriage.data
        household = question_form.household.data
        mortgage_loan = question_form.mortgage_loan.data
        investment_horizon = question_form.investment_horizon.data
        yearly_income = question_form.yearly_income.data
        monthly_expense = question_form.monthly_expense.data

        info = classes.Question(age, gender, marriage, household, mortgage_loan, investment_horizon, yearly_income, monthly_expense)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('index'))

        # if Age >= 22 and Net_Wealth >= 100000:
        #     return redirect(url_for('login'))
        # else:
        #     return redirect(url_for('not_qualify'))
    return render_template('question.html', form=question_form, authenticated_user=current_user.is_authenticated)

@application.route('/example')
def example():

   return render_template('example.html')

@application.route('/dashboard')
@login_required
def dashboard():
    # assign cluster: test case
    n_clusters = 4
    cluster = np.random.randint(0, n_clusters, 1)[0]

    # fetch cluster data from S3
    bucket = "earlybird-data"
    file_name = f"stock/cluster{cluster}.csv"

    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    df = pd.read_csv(obj["Body"])

    # some processing steps
    recommend = df.sample(5)[['company', 'symbol', 'Market Cap', 'PE ratio', 'PB ratio', 'Revenue per Share', 'Net Income per Share']]
    recommend['Market Cap'] = recommend['Market Cap'] / 1e9
    recommend = np.round(recommend, 1).to_numpy()

    return render_template('dashboard.html', data=recommend)

@application.route('/not_qualify', methods=['GET', 'POST'])
def not_qualify():
    return render_template('not_qualify.html')



@application.route('/logout')
def logout():
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    #return before_logout + after_logout
    return redirect(url_for('index'))
