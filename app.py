from flask import Flask, render_template, request
import requests
import pprint

app = Flask(__name__)

apod_link ='https://api.nasa.gov/planetary/apod'

image_link = "https://images-api.nasa.gov/search"

earth_imagery = "https://api.nasa.gov/planetary/earth/imagery"

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

    API_KEY='iEXQ64MtrOAU8qpIul6IWbSFiohIhil8eJTo2Dvc'

    params = {
        'lon' : longitude,
        'lat' : latitude,
        'date' : date,
        'api_key' : API_KEY  
    }

    r = requests.get(earth_imagery, params=params)
    
    if not r.status_code == 200:
        print('error')
    
    results = r.json()
    day = results['date']
    url = results['url']

    return render_template('earth_img_result.html', day=day, url=url)


if __name__ == '__main__':
    app.run()