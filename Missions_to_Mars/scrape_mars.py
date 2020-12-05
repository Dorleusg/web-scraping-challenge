import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests


def request_soup(url):
   
    response = requests.get(url)
  
    soup = bs(response.text, 'html.parser')

    return soup

def init_browser():
    
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
 
 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div',class_='rollover_description_inner').text
    
    return news_title, news_p

    
    home_url = "https://www.jpl.nasa.gov"
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(home_url)
    html = browser.html
    image_page = bs(html,'html.parser')
   
    featured_image = image_page.find('img',class_='thumb')
    featured_image_url = home_url + featured_image['src']
    return featured_image_url
    
    # Mars Facts
    mars_fcts_url = "https://space-facts.com/mars/"
    mars_fcts = pd.read_html(mars_fcts_url)[2]
    mars_fcts.columns = ['Key','Value']
    
    mars_fcts_table_html = mars_fcts.to_html()
    return mars_fcts_table_html


    # Mars Hemisphere

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')   
    

    # Get the html containing the title and put into a list
    title_list = soup.find_all('div', class_='description')


    hemisphere_urls = []
    for title in title_list:
        
        browser.visit(url)
        browser.click_link_by_partial_text(title.a.h3.text)
    
         
        html = browser.html
        soup = bs(html, 'html.parser')
    
        img_url_list = soup.find('img', class_='wide-image')
        img_url = f"https://astrogeology.usgs.gov{img_url_list['src']}"
    
       
        post = {
                'title': title.a.h3.text,
                'img_url': img_url
                }
            
        hemisphere_urls.append(post)
    
    #dictionaries to hold data              

    mars_data = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "mars_fcts_table_html": mars_fcts_table_html,
    "hemisphere_urls": hemisphere_urls
    }
    print(mars_data)   
    return mars_data

