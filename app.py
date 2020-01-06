from flask import Flask, render_template, request
import requests
import pprint

app = Flask(__name__)

apod_link ='https://api.nasa.gov/planetary/apod?'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apod')
def apod_image():
    return render_template('earth.html')


if __name__ == '__main__':
    app.run()