# Mission to Mars

## Overview
This repository houses a web Scraping and Flask project to consolidate information on Mars from various webpages.  Results of the scrape are saved in MongoDB and displayed in one page via Flask, with a link to a separate page for images of the planet's hemispheres. 

![Image](images/nasa-mars-mission-plan.png)


## Background
The scrape code gathers various pieces of information, images, and urls from different websites with information on Mars, and stores the return value in Mongo as a Python dictionary.  MongoDB with Flask (jinja) templating feeds into a HTML page that displays all of the information that was scraped from the URLs listed below. 

Initial scraping and code building was done using Jupyter Notebook, BeautifulSoup, Pandas, and Splinter. 
