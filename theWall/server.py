from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re

#imports the Bcrypt module
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'secretkeyforsession'

#regexes
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

mysql=MySQLConnector(app, 'thewall') #our DB is called 'thewall'

def getUserData():
	query = "SELECT id, first_name, last_name FROM users WHERE id=:user_ID"
	data = {'user_ID': session['user_id']}
	return mysql.query_db(query,data)

def getMsgs():
	query = "SELECT users.first_name, users.last_name, messages.created_at, messages.message, messages.id AS message_id FROM users JOIN messages ON messages.user_id = users.id ORDER BY messages.created_at DESC"
	return mysql.query_db(query)

def getComments():
	query = "SELECT comments.user_id, users.first_name, users.last_name, comments.messages_id, comments.comment, comments.created_at From comments JOIN users ON users.id = comments.user_id"
	return mysql.query_db(query) 

#method for Form Validation on Register
def formValidate():
	isValid = True
	if len(request.form['firstname']) < 0:
		isValid = False
	if len(request.form['lastname']) < 0:
		isValid = False
	if len(request.form['email']) < 0:
		isValid = False
	if len(request.form['password']) < 0:
		isValid = False

	if len(request.form['password']) < 8:
		isValid = False
		flash("Password must be at least 8 characters long!")

	if not EMAIL_REGEX.match(request.form['email']):
		isValid = False
		flash("Invalid Email Address!")

	if not PASSWORD_REGEX.match(request.form['password']):
		isValid = False
		flash("Password must contain at least 1 Upper case and one Digit from 0-9")

	if not request.form['firstname'].isalpha() or not request.form['lastname'].isalpha(): 
		isValid = False
		flash("First or Last Name can only be Letters")

	if request.form['password'] != request.form['confirmpass']:
		isValid = False
		flash("Password and Password Confirmation do not Match, Please Re-enter")

	#check if existing email exists
	query = "SELECT * FROM users WHERE email = :email"
	data={"email": request.form['email']}
	userEmail = mysql.query_db(query, data)
	
	if userEmail:
		flash('Email already in use, please try another one', 'regerror')
		isValid = False

	return isValid


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	isValid = False
	loginEmail = request.form['user']
	loginPass = request.form['password']

	query = "SELECT id, first_name, password FROM users WHERE email=:loginEmail"
	data = {'loginEmail': loginEmail} #using key to reference, don't pass it password, bcrypt does magic
	queryResult= mysql.query_db(query,data)

	#if queryResult finds nothing, it gives empty array '[]', which is 
	#considered 'falsey', this is same as if len(queryResult) == 0
	#Create/send quearyResult in userData so we can edit our own data in login
	if not queryResult:
		flash("Invalid Login Credentials")
		return redirect('/')
	elif bcrypt.check_password_hash(queryResult[0]['password'], loginPass):
		session['user_id'] = queryResult[0]['id']
		return redirect('/wall')
	else:
		return redirect('/')

@app.route('/wall')
def theWall():
	userMsg = getMsgs()
	comments = getComments()
	userData = getUserData()
	return render_template('profile.html', userData = userData, userMsg = userMsg, comments = comments)


@app.route('/register', methods=['POST'])
def register():

	isValid = formValidate()

	#if everything is valid, store the PW in hash and submit the SQL query
	#we store the form data in variables to make it easier to submit the query
	if isValid:
		flash('Registration Successful') #user display to show success
		Fname = request.form['firstname']
		Lname = request.form['lastname']
		Email = request.form['email']
		password = request.form['password']

		#create PW hash with Bcrypt
		pw_hash = bcrypt.generate_password_hash(password)
		#submit SQL query
		query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(:firstname, :lastname, :email, :pw_hash, NOW(), NOW())"
		data = {'firstname': Fname, 'lastname': Lname, 'email': Email, 'pw_hash': pw_hash}
		
		mysql.query_db(query, data)
		return redirect('/')
	else:
		return redirect('/')

@app.route('/messageBoard', methods=['POST'])
def postMessage():
	message = request.form['msgBox']
	query="INSERT INTO messages(message, user_id, created_at, updated_at) VALUES(:message, :user_id, NOW(), NOW())"
	data = {'message': message, 'user_id':session['user_id']}
	userMSG = mysql.query_db(query,data)

	return redirect('/wall')

@app.route('/comment', methods=['POST'])
def postComment():
	comment = request.form['comment']
	message_id = request.form['message_id']
	query="INSERT INTO comments(comment, messages_id ,user_id, created_at, updated_at) VALUES(:comment, :msgID, :user_id, NOW(), NOW())"
	data = {'comment':comment, 'msgID': message_id, 'user_id':session['user_id']}
	userComment = mysql.query_db(query,data)

	return redirect('/wall')


@app.route('/deactivate/<userID>', methods=['POST'])
def deactivate(userID):
	delUserQuery = "DELETE FROM users WHERE id=:id"
	data_id={'id': userID}
	mysql.query_db(delUserQuery,data_id)
	return redirect('/')

@app.route('/deleteMsg/<message_id>')
def delete_message(message_id):
	message = mysql.query_db("SELECT * FROM messages WHERE id = :id LIMIT 1", {"id":message_id})
	if not message:
		return redirect('/wall')
	else:
		message = message[0]

	if message['user_id'] != session['user_id']:
		return redirect('/wall')

@app.route('/deleteComment', methods=['GET'])
def delete_comment():
	return redirect('/wall')


@app.route('/logout', methods=['POST'])
def logout():
	#deletes session user id
	del session['user_id']
	return redirect('/')

app.run(debug=True)


#DELETE FROM comments WHERE message_id =:message_id
#data={'msg_id': message_id}


#write a query that's for this user and this message, give comment


#SELECT * FROM comments 
#WHERE message_id = i.message_id
# select * from thewall.comments where user_id = :user_id and messages_id = :user_msg;
#data = {'user_id': i.user_id}

