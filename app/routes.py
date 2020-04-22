from app import application, classes, db
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user
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
            return redirect(url_for('register_project'))
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
            return redirect(url_for('example'))
        else:
            flash('Invalid username and password combination!')

    return render_template('login.html', form=login_form, authenticated_user=current_user.is_authenticated)



@application.route('/question', methods=['GET', 'POST'])
def register_project():
    project_form = classes.ProjectForm()
    if project_form.validate_on_submit():
        Net_Wealth = project_form.Net_Wealth.data
        Annual_Income = project_form.Annual_Income.data
        Age = project_form.Age.data
        user_name = project_form.username.data
        project = classes.Project(Net_Wealth, Annual_Income, Age, user_name)
        db.session.add(project)
        db.session.commit()
        #return redirect(url_for('index'))

        if Age >= 22 and Net_Wealth >= 100000:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('not_qualify'))
    return render_template('question.html', form=project_form, authenticated_user=current_user.is_authenticated)

@application.route('/example')
def example():
   return render_template('example.html')

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
