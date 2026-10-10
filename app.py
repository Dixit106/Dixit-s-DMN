from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Database configuration
#first we tell flask to create a file "diary.db" in my project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
db =SQLAlchemy(app)

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)# finally i can use my highschool study knowlege somewhere,(Primarykey= unique ID for every post)
    title = db.Column(db.String(100), nullable=False)#title of my entry
    content = db.Column(db.Text, nullable=False)#yapping
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)#for autosaving time

    def __repr__(self):
        return f"Entry('{self.title}','{self.date_posted}')"

#The Home page
@app.route('/')
def home():
    return render_template('index.html')

#The diary page
@app.route('/diary')
def diary():
    return render_template('diary.html')

#The about page
@app.route('/about')
def about():
    return render_template('about.html')

#The eye page
@app.route('/eye')
def eye():
    return render_template('eye.html')

#The mail
@app.route('/mail')
def mail():
    return render_template('mail.html')

#Secret Admin Page(for me)
@app.route('/secret-admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_content = request.form['content']

        new_entry = DiaryEntry(title=entry_title, content=entry_content)

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('diary'))

    return render_template('admin.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)