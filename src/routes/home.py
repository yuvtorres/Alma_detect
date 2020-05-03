from flask import render_template,send_file
from src.app import app

# Call the home of the app web
@app.route("/")
def home_present():
    return render_template('home.html')

@app.route("/chat_sentiment")
def get_image():
    return send_file('templates/sentiment.png', mimetype='image/png')
