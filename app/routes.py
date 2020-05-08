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
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    q5 = 0
    q6 = 0
    q7 = 0
    q8 = 0
    q9 = 0
    q10 = 0
    score = 0

    question_form = classes.QuestionForm()
    if question_form.validate_on_submit():
        age = question_form.age.data
        if int(age)>=18 & int(age)<22:
            q1 = 10
        elif int(age)>=22 & int(age)<26:
            q1 = 7.5
        elif int(age)>=26 & int(age)<30:
            q1 = 5
        else:
            q1 = 2.5

        num_income_source = question_form.num_income_source.data
        if num_income_source =='1':
            q2 = 10
        elif num_income_source == '2':
            q2 = 7.5
        elif num_income_source == '3':
            q2 = 5
        else:
            q2 = 2.5

        marriage = question_form.marriage.data
        if marriage == 'Single':
            q3 = 10
        else:
            q3 = 5

        household = question_form.household.data
        if household == 'R':
            q4 = 10
        else:
            q4 = 5

        mortgage_loan = question_form.mortgage_loan.data
        if mortgage_loan == 'N':
            q5 = 5
        else:
            q5 = 10

        investment_horizon = question_form.investment_horizon.data
        if investment_horizon <= 5:
            q6 = 10
        elif investment_horizon >5 & investment_horizon <=7:
            q6 = 7.5
        elif investment_horizon > 7 & investment_horizon <=10:
            q6 = 5
        else:
            q6 = 2.5

        yearly_income = question_form.yearly_income.data
        if yearly_income == '1':
            q7 = 10
        elif yearly_income =='2':
            q7 = 8
        elif yearly_income == '3':
            q7 = 6
        elif yearly_income =='4':
            q7 = 4
        elif yearly_income == '5':
            q7 = 2
        else:
            q7 = 0

        monthly_expense = question_form.monthly_expense.data
        if monthly_expense == '1':
            q8 = 2
        elif monthly_expense == '2':
            q8 = 4
        elif monthly_expense == '3':
            q8 =6
        elif monthly_expense == '4':
            q8 = 8
        else:
            q8 = 10

        knowledge = question_form.knowledge.data
        if knowledge == '1':
            q9 = 2.5
        elif knowledge == '2':
            q9 = 5
        elif knowledge == '3':
            q9 = 7.5
        else:
            q9 = 10

        aum = question_form.aum.data
        if aum == '1':
            q10 = 10
        elif aum == '2':
            q10 = 8
        elif aum == '3':
            q10 = 6
        elif aum == '4':
            q10 = 4
        elif aum == '5':
            q10 = 2

        score = q1+q2+q3+q4+q5+q6+q7+q8+q9+q10

        info = classes.Question(age, num_income_source, marriage, household, mortgage_loan, investment_horizon, yearly_income, monthly_expense, aum, knowledge, score)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('score'))

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

@application.route('/score', methods=['GET', 'POST'])
def score():
    info = classes.Question.query.order_by("id").all()
    score = info[-1].score
    return render_template('score.html', score = score)


@application.route('/logout')
def logout():
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    #return before_logout + after_logout
    return redirect(url_for('index'))
