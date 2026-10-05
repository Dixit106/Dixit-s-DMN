from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)