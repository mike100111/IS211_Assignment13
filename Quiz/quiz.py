import os
import sqlite3
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'hw13.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password'
))

###Database####

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
		
##############

####User Control####

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
            return redirect(url_for('show_dashboard'))
            return redirect(url_for('show_dashboard'))
    return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_dashboard'))
	
##############


####Views#####		

@app.route('/dashboard')
def show_dashboard():
	db = get_db()
	cur = db.execute('select * from student')
	students = cur.fetchall()
	cur = db.execute('select * from quiz')
	quiz = cur.fetchall()
	return render_template('show_dashboard.html', students=students, quiz=quiz)
	
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
	try:
		if not session.get('logged_in'):
			abort(401)
		if request.method == 'GET':
			return render_template('add_student.html')
		elif request.method == 'POST':
			db = get_db()
			db.execute('insert into student (first, last) values (?, ?)',[request.form['first'], request.form['last']])
			db.commit()
			flash('New student was successfully posted')
		return redirect(url_for('show_dashboard'))
	except:
		flash('An error occured')
		return redirect(url_for('show_dashboard'))
	
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
	try:
		if not session.get('logged_in'):
			abort(401)
		if request.method == 'GET':
			return render_template('add_quiz.html')
		elif request.method == 'POST':
			db = get_db()
			db.execute('insert into quiz (subject, questionNum, quizDate) values (?, ?, ?)',[request.form['subject'], request.form['questionNum'], request.form['quizDate']])
			db.commit()
			flash('New quiz was successfully posted')
		return redirect(url_for('show_dashboard'))
	except:
		flash('An error occured')
		return redirect(url_for('show_dashboard'))
	
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
	try:
		if not session.get('logged_in'):
			abort(401)
		if request.method == 'GET':
			db = get_db()
			cur = db.execute('select * from student')
			students = cur.fetchall()
			cur = db.execute('select * from quiz')
			quiz = cur.fetchall()	
			return render_template('add_result.html', quizzes=quiz, students=students)
		elif request.method == 'POST':
			db = get_db()
			db.execute('insert into student_quiz (student_id, quiz_id, score) values (?, ?, ?)',[request.form['students'], request.form['quizzes'], request.form['score']])
			db.commit()
			flash('New quiz score was successfully posted')
		return redirect(url_for('show_dashboard'))
	except:
		flash('An error occured')
		return redirect(url_for('show_dashboard'))
		
@app.route('/student/<id>', methods=['GET'])
def display_results(id):
	try:
		if not session.get('logged_in'):
			abort(401)
		db = get_db()
		cur = db.execute('select * from student')
		students = cur.fetchall()
		cur = db.execute('select * from quiz')
		quiz = cur.fetchall()
		db = get_db()
		cur = db.execute('select quiz.id, quiz.subject, quiz.quizDate, student_quiz.score from quiz join student_quiz on student_quiz.quiz_id = quiz.id where student_quiz.student_id = ?', id )
		results = cur.fetchall()
		return render_template('show_dashboard.html', students=students, quiz=quiz, results=results)
	except:
		flash('An error occured')
		return redirect(url_for('show_dashboard'))
	
if __name__ == "__main__":
	init_db()
	app.run(debug=True)