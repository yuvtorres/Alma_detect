from flask import render_template
from src.app import app

# Call the home of the app web
@app.route("/")
def home_present():
    return render_template('home.html')

