from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

mars_info = {}

def scrape_mars_news():
    browser = init_browser()

    n_url = 'https://mars.nasa.gov/news/'
    browser.visit(n_url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')
    slides = soup.find_all('li', class_='slide')
    the_title = slides[0].find('div', class_ = 'content_title')
    news_title = the_title.text.strip()
    article_tease_body = slides[0].find('div', class_ = 'article_teaser_body')
    news_par = article_tease_body.text.strip()
    print("Title: ",news_title)
    print("Body: ",news_par)

    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_par

    return mars_info
    browser.quit()

def scrape_mars_image():
    browser = init_browser()

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    THE_url = "https://www.jpl.nasa.gov"
    image_url = THE_url + image_url
    image_url 
    mars_info['image_url'] = image_url     
    
    return mars_info
    browser.quit()


def scrape_mars_facts():
    browser = init_browser()

    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    soup2 = bs(response.text, 'html.parser')
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ["Category", "Value"]

    mars_html = mars_df.to_html(table_id="html_tbl_css",justify='left',index=False)
    
    mars_info['tables'] = mars_html

    return mars_info


def scrape_mars_hemispheres():
    browser = init_browser()
    
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item') 
    hiu = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 
    
    for i in items:
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
        browser.quit() 

        return mars_info
