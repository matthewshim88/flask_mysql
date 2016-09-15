from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)

mysql = MySQLConnector(app, 'friendsdb')

#Will Add Form Validation Later!!! (regex, etc)

#displays all friends on main page
@app.route('/')
def index():
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	return render_template('index.html', all_friends=friends)

#creates a friend and inserts to DB
@app.route('/friends', methods=['POST'])
def create():
	#first Perform Form Validation
	#insert SQL query
	query = 'INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())'
	data = {
				'first_name': request.form['first_name'],
				'last_name': request.form['last_name'],
				'email': request.form['email']

			}
	mysql.query_db(query,data)
	return redirect('/')

#Goes to edit page, takes friend_id
@app.route('/friends/<friend_id>/edit')
def edit(friend_id):
	query="SELECT * FROM friends WHERE id=:variable"
	data = {
				'variable':friend_id
			}

	selectFriend = mysql.query_db(query,data)
	return render_template('/editfriends.html', editFriend=selectFriend)

#updates friends
@app.route('/friends/<friend_id>', methods=['POST'])
def update(friend_id):
	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id=:id"
	data = {
				'first_name': request.form['fname_edit'],
				'last_name': request.form['lname_edit'],
				'occupation': request.form['email_edit'],
				'id': friend_id
			}
	mysql.query_db(query, data)
	return redirect('/')

#deletes friends
@app.route('/friends/<friend_id>/delete', methods=['POST'])
def destroy(friend_id):
	query = "DELETE FROM friends WHERE id=:id"
	data = {'id': friend_id}
	mysql.query_db(query,data)
	return redirect('/')

app.run(debug=True)





