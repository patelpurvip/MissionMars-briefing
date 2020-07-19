from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import datetime
from dotenv import load_dotenv
import os
import tweepy


def scrape():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.nasamars_db
    mars_data = db.articles

    executable_path = {'executable_path': r"C:\Users\Purvi Patel\Documents\Chromedriver\chromedriver.exe"}
    browser = Browser('chrome', 'executable_path')
    # browser = Browser('chrome', **executable_path, headless=False)

    ##########################################################################
    # START SCRAPES
    ##########################################################################
    # Mars News
    ##########################################################################
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html')
    
    # ORIGINAL SCRAPE CODE (first_title)
    first_article = soup.select_one("ul.item_list li.slide")
    first_title = first_article.find('div', class_='content_title').get_text()
    #------------------------------------------------------------------------
    # ALTERNATIVE SCRAPE CODE (first_title)
    # all_titles = soup.find_all('div', class_='content_title')
    # first_title = all_titles[1].text
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # ORIGINAL SCRAPE CODE (first_paragraph)
    first_paragraph = first_article.find('div', class_='article_teaser_body').get_text()
    #------------------------------------------------------------------------
    # ALTERNATIVE SCRAPE CODE (first_paragraph)
    # first_paragraph = soup.find('div', class_ = 'article_teaser_body').text
    

    ##########################################################################
     #Featured Image
    ########################################################################## 
    url2 = 'https://mars.nasa.gov'
    browser.visit(url2)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_featured_image = soup.find('img', class_='img-holder-img')
    image_name_section = soup.find('div', class_="window")
    mars_img_url = mars_featured_image.get('src')

    featured_image_name = image_name_section.find('h1', class_="media_feature_title").text
    featured_image_url = url2 + mars_img_url

    ##########################################################################
    # Mars Facts
    ##########################################################################
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)

    mars_table = pd.read_html(url4)

    table_df = mars_table[0]
    table_df.columns = ['Measurement', 'Value']
    table_df.set_index('Measurement', inplace=True)

    table_df.rename(columns={"Value":""})

    # html_table = table_df.to_html("./facts_table.html")
    html_table = table_df.to_html(header = False)
    final_facts_table = html_table.replace('\n', '')
    # final_facts_table = print(html_table)
    
    ##########################################################################
    # Mars Hemispheres
    ##########################################################################    
    # ORIGINAL SCRAPE CODE, BUT THE PAGE WAS AT ONE POINT DELETED BY NASA AND THE CODE WAS REWRITTEN FOR A NEW PAGE
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url5)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_hemispheres_dict = []
    mars_hemipage_list = []

    # mars_hemisphere_data = soup.find_all('div', class_='item')

    mars_hemipage_list.clear()
    hemi_name_tags = soup.find_all('h3')    

    for i in hemi_name_tags:
        hemi_page_name = i.text
        mars_hemipage_list.append(hemi_page_name)
            

    for i in mars_hemipage_list:
        hemi_page = browser.find_link_by_partial_text(''+(i)+'')
        hemi_page.click()
        
        html = browser.html
        soup = bs(html, 'html.parser')

        page_title = soup.find('h2').text
        title_split = page_title.split((" "))
        title_split.pop()
        title = ' '.join(title_split)
        title

        img = soup.find('li')
        img_url = img.a.get('href')

        Hemisphere = {'title':title, 'img_url':img_url}
        mars_hemispheres_dict.append(Hemisphere)
        
        browser.back()
    #------------------------------------------------------------------------------
    # ALTERNATIVE SCRAPE CODE
    # mars_hemispheres_dict = []

    # url5 = 'https://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html'
    # browser.visit(url5)
    # html = browser.html
    # soup = bs(html, 'html.parser')

    # mars_hemi_data = soup.find_all('img', class_='img840')

    # for i in mars_hemi_data:
    #     hemi_name_header = i.get('alt')
    #     header_split = hemi_name_header.split((" "))
    #     header_split.pop(0)
    #     title = ' '.join(header_split)
    #     print(title)

    #     img_url = i.get('src')
    #     print(img_url)
        
    #     Hemisphere = {'title':title, 'img_url':img_url}
    #     mars_hemispheres_dict.append(Hemisphere)
    
    # mars_hemispheres_dict
    #------------------------------------------------------------------------------
    
    ##########################################################################
    # Mars Weather
    ##########################################################################
     #------------------------------------------------------------------------------
     # ORIGINAL SCRAPE CODE, BUT IT WILL NOT RUN HERE DUE TO TWITTER PERMISSIONS
    # url3 = 'https://twitter.com/marswxreport?lang=en'
    # browser.visit(url3)
    # html = browser.html
    # soup = bs(html, 'html.parser')
    # mars_weather_update = soup.select_one('article')
    # mars_weather = mars_weather_update.find('div', lang='en').get_text()
    #------------------------------------------------------------------------------

    # ALTERNATIVE SCRAPE CODE
    load_dotenv()
    API_key = os.getenv('API_key')
    API_secret_key = os.getenv('API_secret_key')
    auth = tweepy.OAuthHandler(API_key, API_secret_key)    
    api = tweepy.API(auth)    
    username = 'MarsWxReport'    
    tweets = []    
    data = api.user_timeline(id=username, tweet_mode="extended")    
    for t in data:
        tweets.append(t.full_text)
    mars_weather = tweets[0]
    mars_weather = mars_weather.split(' http',1)[0]


    ##########################################################################
    # Export collection of articles
    ##########################################################################
    mars_data = {
        "first_title": first_title,
        "first_paragraph": first_paragraph,
        "featured_image_url": featured_image_url,
        "featured_image_name": featured_image_name,
        "facts_table": final_facts_table,
        "weather": mars_weather,
        "hemispheres": mars_hemispheres_dict,
        "timestamp": str(datetime.datetime.today())
        }
    ##########################################################################
    # Close the browser after scraping & Return results
    ##########################################################################
    browser.quit()
    return mars_data
    print(mars_data)


