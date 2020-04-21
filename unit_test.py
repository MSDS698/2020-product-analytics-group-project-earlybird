from app import classes, application, db
from werkzeug.security import check_password_hash, generate_password_hash


# def test_colname():
# 	user_colname = []
# 	project_colname = []
# 	for i in classes.User.__table__.columns:
# 		user_colname.append(i)
# 	for i in classes.Project.__table__.columns:
# 		project_colname.append(i)
#
# 	assert user_colname == ['id','username','email','password_hash']
# 	assert project_colname == ['id','user_name','Net_Wealth','Annual_Income','Age']


def test_qualifieduser():
	#Assume user has entered a age>= 22 or net_wealth >=10000 to be a qualified user
	assert classes.Project.query.filter_by(user_name='ddd').first().Age >=22
	assert classes.Project.query.filter_by(user_name='ddd').first().Net_Wealth >=10000


def test_user():
	# Assuming that "ddd, d@gmail.com, 1234" is always in the database
	assert classes.User.query.filter_by(username='ddd').first().email == 'd@gmail.com'
	assert classes.User.query.filter_by(username='ddd').first().username == 'ddd'
	assert check_password_hash(classes.User.query.filter_by(username='ddd').first().password_hash, "1234")
