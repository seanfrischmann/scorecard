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

@app.route('/delete_game/<courseName>')
def delete_game(courseName):
	data = {
			'database':g.db,
			'courseName':courseName}
	courseInfo = [data['courseName'], query.getCourseGames(data)]
	return render_template('delete_game.html', courseInfo=courseInfo)

@app.route('/remove_game/<courseName>', methods=['GET', 'POST'])
def remove_game(courseName):
	data = {
			'database':g.db,
			'gameId':request.form['gameId'],
			'courseName':courseName}
	flash(query.removeGame(data))
	return redirect(url_for('get_course', courseName=courseName))

@app.route('/add_game/<courseName>')
def add_game(courseName):
	data ={
			'database':g.db,
			'courseName':courseName}
	courseInfo = [courseName]
	courseInfo.append(query.getCourseInfo(data))
	return render_template('add_game.html', courseInfo=courseInfo)

@app.route('/post_game/<courseName>', methods=['GET', 'POST'])
def post_game(courseName):
	data ={
			'database':g.db,
			'date':request.form['date'],
			'courseName':courseName}
	numberOfHoles = query.getNumberOfHoles(data)
	i = 1
	score = ''
	while i <= numberOfHoles:
		score = score + request.form[str(i)]
		if i is not numberOfHoles:
			score = score + ' '
		i += 1
	data['score'] = score
	flash(query.postGame(data))
	return redirect(url_for('get_course', courseName=courseName))

@app.route('/delete_course')
def delete_course():
	data = {
			'database':g.db}
	courseList = query.getCourseList(data)
	return render_template('delete_course.html', courseList=courseList)

@app.route('/remove_course', methods=['GET', 'POST'])
def remove_course():
	print ('here')
	data = {
			'database':g.db,
			'courseName':request.form['courseName']}
	print ('here')
	flash(query.removeCourse(data))
	print ('here')
	return redirect(url_for('profile'))

@app.route('/get_course/<courseName>')
def get_course(courseName):
	data = {
			'database':g.db,
			'courseName':courseName}
	courseInfo = [data['courseName'], query.getCourseGames(data)]
	return render_template('course_info.html', courseInfo=courseInfo)

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
