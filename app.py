from flask import Flask, render_template, request
import requests
import pprint
from random import random




app = Flask(__name__)

API_KEY='iEXQ64MtrOAU8qpIul6IWbSFiohIhil8eJTo2Dvc'

apod_url ='https://api.nasa.gov/planetary/apod'

image_url = "https://images-api.nasa.gov/search"

earth_imagery = "https://api.nasa.gov/planetary/earth/imagery"

mars_url = "https://api.nasa.gov/insight_weather/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/earth')
def earth():
    return render_template('earth.html')

@app.route('/mars')
def mars():
    return render_template('mars.html')


@app.route('/earth_search')
def earth_form():
    return render_template('imagery_form.html')

@app.route('/earth_imagery')
def earth_image():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    date = request.args.get('date')


    params = {
        'lon' : longitude,
        'lat' : latitude,
        'date' : date,
        'api_key' : API_KEY  
    }

    r = requests.get(earth_imagery, params=params)
    
    if not r.status_code == 200:
        print('error')
    pprint(r)
    results = r.json()
    day = results["date"]
    # url = results['url']

    return render_template('earth_img_result.html', day=day)
@app.route('/apod')
def apod():
    return render_template('apod.html')


@app.route('/apod/results')
def apod_results():
    params = {
        'api_key' : API_KEY
    }

    r = requests.get(apod_url, params=params)

    results = r.json()
    description = results["explanation"]
    title = results["title"]
    url = results["url"]

    
    return render_template('apod_results.html', description=description, title=title, url=url)

def search_results():
    user_search = request.args.get('item')

    params = {
        'q' : user_search,
    }
    
    r = requests.get(image_url, params=params)

    results = r.json()
    # Come back to this later finish planned routes and endpoints
    pass

@app.route('/mars/weather')
def mars_weather():
    params = {
        'api_key' : API_KEY,
        'feedtype' : 'json',
        'version' : 1.0
    }

    r = requests.get(mars_url, params=params)

    results = r.json()
    sol = results["389"]
    temp = sol["AT"]
    min_temp = temp["mn"]
    max_temp = temp["mx"]
    

    return render_template('mars_result.html',temp=temp,min_temp=min_temp,max_temp=max_temp)






if __name__ == '__main__':
    app.run()