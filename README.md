# Mission to Mars

## Overview
This repository houses a web Scraping and Flask project to consolidate information on Mars from various webpages.  Results of the scrape are saved in MongoDB and displayed in one page via Flask, with a link to a separate page for images of the planet's hemispheres. Original scrape codes were developed in the jupyter notebooks housed in the repository, before being transferred into the python scrape files.

### Visit the deployed Mission Mars [briefing page](https://mars-data-scrape.herokuapp.com/)!

![Image](images/nasa-mars-mission-plan.png)


## Background
The scrape code gathers various pieces of information, images, and urls from different websites with information on Mars, and stores the return value in Mongo as a Python dictionary.  MongoDB with Flask (jinja) templating feeds into a HTML page that displays all of the information that was scraped from the URLs listed below. 

Initial scraping and code building was done using Jupyter Notebook, BeautifulSoup, Pandas, and Splinter. 

## Scrape Features & Information
The scrape is initiated through a button at the center of the page's Jumbotron/header.  The date and time of the last scrape used to gather the data currently displayed is shown at the bottom of the jumbotron. 

The final Flask app deploys a webpage that will feed the information from the scrape into several sections:
1. Latest Mars News
2. Featured Mars Image
3. Mars Weather
4. a Mars Facts table
5. Thumbnail images of Mars Hemispheres

A link from the "Mars Hemispheres" heading will take you to a second page with larger images of each hemisphere, linked to the full online images. A link on the upper lefthand corner of the hemispheres page ("Mars Data Mainpage") will return you to the main scrape page. 

The following table lists the sources of information for each section of the scrape:

|Information Section|Source|Link|
|:---:|:---:|:---:|
|Latest Mars News|NASA Mars Exploration Program|https://mars.nasa.gov/news/|
|Featured Mars Image |NASA Mars Exploration Program|https://mars.nasa.gov ("Image of the Week")| 
|Current Weather on Mars|@MarsWxReport Twitter account (InSight updates from the REMS weather instrument aboard the Mars Curiosity rover)|https://twitter.com/marswxreport?lang=en|
|Mars Facts| Space Facts online|https://space-facts.com/mars/|
|Mars Hemispheres|The Planetary Society|https://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html|
|Mars Hemispheres alternate code|US Geological Survey|https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars|
|Mars Opportunity Comic|Squarespace Images|https://images.squarespace-cdn.com/content/v1/53924fa8e4b0e30215363474/1550692066119-F2SK4DCJW6Z1KQV0PUB9/ke17ZwdGBToddI8pDm48kPx25wW2-RVvoRgxIT6HShBZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpx0Qh3eD5PfZ_nDR0M7OIGaTx-0Okj4hzQeRKYKbt7WfTYFScRKDTW78PcnUqBGqX8/blog2.png/|


## Flask app versions & Installation

### 1) Local deployment w/a local MongoDB database (using splinter)
run file: app_local.py

folder: fully-local-version

The original version is designed to store information collected from the scrape in a local mongo database, and to run the app deploying the webpage locally, through Flask.  The scrape (initiated by clicking the scrape button on the webpage while flask is running the app) is run through Chromedriver. Chromedriver visits each url in the scrape code, scrapes the requested information, stores it locally in MongoDB, and closes out.  Mongo then provides the information from the latest scrape to the webpage via Flask while the Flask app is running locally. 

To run the local version, you will first need to make sure you have MongoDB installed on your local computer and set up to recieve and store information from apps run from your terminal (and replace your local mongodb connection path in app_local.py, line 8). Run the app_local.py file in your terminal, and you can open the page in your web browser on your http://localhost:8000/ port. If any portion of the scrape code fails to work, alternate code has been provided for most of the scrape sections in the mars_data_scrape.py file.

You will also need to provide your own Twitter developer keys to run the Mars Weather portion of the scrape, and save them as environment variables in a .env file.  If you do not have a developer account, an alternate scrape code has been provided (currently commented out) in the mars_data_scrape.py file. 


### 2) Local deployment w/ online Mongo Atlas database (using splinter)
run file: app2.py

folder: local-with-MongoAtlas

The second version uses the same code as the first, and also runs locally, as detailed above.  The only change is that instead of saving the scrape data on a local Mongo database, the data is scraped into an online db via Mongo Atlas. To run this version, you will have to create a Mongo Atlas account (or other online no-SQL DB of choice) to recieve the scrape information, and then make sure the Flask app (app2.py) can access Atlas with your personal `password`, which you can save in the same .env file as your Twitter keys. You will also need to replace the uri path with your Atlas uri path in the app2.py file, line 14.

As with the fully local version, run the app_local.py file in your terminal, and you can open the page in your web browser on your http://localhost:8000/ port. The scrape function will run by clicking the "Scrape" button. The data will scrape to the Atlas database, and populate the data into the HTML files through Flask. 


### 3) Public deployment via Heroku
run file: app3.py (calling mars_data_scrape2.py)

deployment site: https://mars-data-scrape.herokuapp.com/

The intention of this final version was to deploy the Flask app publicly via Heroku.  This version, like version 2, still makes use of Mongo Atlas to store the scraped information through an online service and the feed it into the final webpage. However, the main difficulty was the dependance of prior models on the chromedriver to scrape the content from the websites listed above.  One option I had considered was to see if I could get a headless driver to work with selenium to scrape the necessary information.  However, the easier option was to change the code to use `urllib.request` instead of a webdriver.  However, request works a bit differently and does not always return the full code on a given webpage, especially with code fed to the page through Javascript instead being written of directly into the webpage's HTML.  Due to this, the scrape code had to be adjusted in some parts of the scrape in order to return content. 

For example, one trade-off was that request will usually not return the first (most recent) article on the NASA Mars News webpage, but will return article 2 or article 4 pretty regularly.  I decided that this was acceptable enough for the funcionality in order to make the scrape work, even if I do not always have the MOST recent article displayed on the publicly deployed page.  The other big change in the code was with the "Mars Hemisphere" information, particularly the hemisphere images. The original code relied on webdriver functions such as `browser.find_link_by_partial_text()` or `browser.back()`.  I decided the easiest solution for the moment was to simply scrape the code from another site that would not require nagivating between pages within the scrape code loop.  Therfore, the public deployment takes the hemisphere information from the Planetary Society's page instead of the US Geological Survey's pages (both source URLs listed above). 

-----
### Additional Copyright
The opening image was taken from an [article](https://bgr.com/2017/07/13/nasa-mars-mission-no-money-to-land/) on the BGE news and commentary website. 
