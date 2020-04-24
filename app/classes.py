from flask_login import UserMixin
from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import  DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

from app import db, login_manager

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    marriage = db.Column(db.String(80), nullable=False)
    household = db.Column(db.String(80), nullable=False)
    mortgage_loan = db.Column(db.String(80), nullable=False)
    investment_horizen = db.Column(db.Integer, nullable=False)
    yearly_income = db.Column(db.String(80), nullable=False)
    monthly_expense = db.Column(db.String(80), nullable=False)

    def __init__(self, age, gender, marriage, household,mortgage_loan, investment_horizon, yearly_income, monthly_expense):
        self.age = age
        self.gender = gender
        self.marriage = marriage
        self.household = household
        self.mortgage_loan = mortgage_loan
        self.investment_horizen =  investment_horizon
        self.yearly_income = yearly_income
        self.monthly_expense = monthly_expense


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    gender = SelectField('Gender', choices=[('F', 'Female'), ('M', 'Male')])
    age = IntegerField('Age:', validators=[DataRequired()])
    marriage = SelectField('Marriage Status', choices=[('Single', 'Single'), ('Married', 'Married')])
    household = SelectField('Household', choices=[('H', 'Own House'), ('R', 'Rent Apartment')])
    mortgage_loan = SelectField('Mortgage Loan', choices=[('Y', 'Yes'), ('N', 'No')])
    investment_horizon = IntegerField('Investment Horizen:', validators=[DataRequired()])
    yearly_income=SelectField('Annual Income', choices=[('1', '30,000-70,000'), ('2', '70,000-100,000'),
                                                   ('3', '100,000-130,000'), ('4', '130,000-160,000'),
                                                   ('5', '160,000-200,000'), ('6', '200,000-240,000'),
                                                   ('3', '100,000-130,000') ])
    monthly_expense = SelectField('Monthly Expense', choices=[('1', '500-1,000'), ('2', '1,000-2,500'),
                                                   ('3', '2,500-4,000'), ('4', '4,000-5,500'),
                                                   ('5', '5,500&up') ])
    submit = SubmitField('Submit')

class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

db.create_all()
db.session.commit()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
