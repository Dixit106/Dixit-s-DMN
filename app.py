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
    image_url = db.Column(db.String(500), nullable=True)
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
    # to get all entries from the database, ordered by newest date first
    all_entries = DiaryEntry.query.order_by(DiaryEntry.date_posted.desc()).all()

    #Send those entries to the HTML file so it can display them
    return render_template('diary.html', entries=all_entries)

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
        entry_image_url = request.form.get('image_url', '')

        new_entry = DiaryEntry(title=entry_title, content=entry_content, image_url=entry_image_url)

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('diary'))
    all_entries = DiaryEntry.query.order_by(DiaryEntry.date_posted.desc()).all()
    return render_template('admin.html', entries=all_entries)

#Delete route for database
@app.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('diary'))

#Edit route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        entry.image_url = request.form.get('image_url', '')
        db.session.commit()
        return redirect(url_for('diary'))

    return render_template('edit.html', entry=entry)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)