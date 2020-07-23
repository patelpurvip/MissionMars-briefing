from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_data_scrape
import sys
from dotenv import load_dotenv
import os


load_dotenv()
password = os.getenv('password')

flask_app = Flask(__name__)

mongo = PyMongo(flask_app, uri=f"mongodb+srv://patelpurvip:{password}@cluster0.bfrvo.mongodb.net/mars_app?retryWrites=true&w=majority")


@flask_app.route("/")
def index():
    # return render_template("index.html", first_title=first_title, first_paragraph=first_paragraph)
    collection_data = mongo.db.articles.find_one()
    return render_template("index.html", stuff=collection_data)


@flask_app.route("/scrape/")
def scraper():
    mars_data = mars_data_scrape.scrape()
    print(mars_data)
    mongo.db.articles.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


@flask_app.route("/hemispheres")
def hemispheres():
    collection_data = mongo.db.articles.find_one()
    return render_template("hemispheres.html", stuff=collection_data)
    

if __name__ == "__main__":
    flask_app.run(debug=True)