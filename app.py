from flask import Flask, render_template, request, redirect, url_for
import requests
import pprint
from pymongo import MongoClient

client = MongoClient()
db = client.Astra
comments = db.comments
blogs = db.blogs




app = Flask(__name__)

pp = pprint.PrettyPrinter(indent=4)

API_KEY='iEXQ64MtrOAU8qpIul6IWbSFiohIhil8eJTo2Dvc'

apod_url ='https://api.nasa.gov/planetary/apod'

image_url = "https://images-api.nasa.gov/search"

earth_imagery = "https://api.nasa.gov/planetary/earth/imagery"

mars_url = "https://api.nasa.gov/insight_weather/"

# Homepage
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

# TODO fix earth imagery
@app.route('/earth_imagery')
def earth_image():
    pass
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
    

    results = r.json()
    day = results["date"]
    # url = results['url']
    pass
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
@app.route('/search/results')
def search_results():
    user_search = request.args.get('item')

    params = {
        'q' : user_search,
        'media_type' : 'image',
    }
    
    r = requests.get(image_url, params=params)

    results = r.json()

    collection = results["collection"]["items"][1]
    links = collection["links"]
    img = links[0]["href"]
    description = collection["data"][0]["description"]
    title = collection["data"][0]["title"]


    
    
    # Come back to this later finish planned routes and endpoints
    return render_template('search_results.html',img=img,description=description,title=title)

@app.route('/mars/weather')
def mars_weather():
    params = {
        'api_key' : API_KEY,
        'feedtype' : 'json',
        'version' : 1.0
    }

    r = requests.get(mars_url, params=params)

    results = r.json()
    sol = results["391"]
    temp = sol["AT"]
    min_temp = temp["mn"]
    max_temp = temp["mx"]
    

    return render_template('mars_weather.html',temp=temp,min_temp=min_temp,max_temp=max_temp)

# blog = [
#     { 'title': 'test', 'content': 'Cats acting weird' }
# ]



@app.route('/blog')
def blogs_index():
    return render_template('blogs_index.html', blogs=blogs.find())

# @app.route('/blog/create')
# def create_blog():
#     return render_template('create_blog.html')

# @app.route('/blog',methods=['POST'])
# def blog_submit():
#     blg = {
#         'title' : request.form.get('title'),
#         'content' : request.form.get('content')
#     }
#     blog.insert_one(blg)
#     return redirect(url_for('blogs_index'))





if __name__ == '__main__':
    app.run()