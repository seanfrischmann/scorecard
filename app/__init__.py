# ===========================================================================
# +++Init File+++|
# _______________|
#
# Sean Frischmann 
# Scorecard -- Score Keeping App
# ===========================================================================

# Imports
import sqlite3
import app.queries as query
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash


#create app
app = Flask(__name__)

# Configuration
app.config.from_object('config')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/profile')
def profile():
	data = {
			'database':g.db}
	courseList = 'false'
	if query.courseExists(data):
		courseList = query.getCourseList(data)
	return render_template('profile.html', courseList=courseList)

@app.route('/add_course')
def add_course():
	return render_template('add_course.html')

@app.route('/post_course', methods=['GET', 'POST'])
def post_course():
	i = 0
	data = {
			'database':g.db,
			'courseName':request.form['courseName'],
			'numberOfHoles':request.form['numberOfHoles']}
	parList = '' 
	courseLength = int(data['numberOfHoles'])
	while i < courseLength:
		hole = 'hole'+str(i)
		parList += request.form[hole]
		if (i+1) != courseLength:
			parList += ' '
		i += 1
	data['par'] = parList
	flash(query.postCourse(data))
	return redirect(url_for('profile'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('profile'))
	return render_template('index.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()
