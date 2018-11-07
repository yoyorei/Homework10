from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    scrapedata = {}

# NASA Mars News
    url1="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url1)
    html1 = browser.html
    soup1 = BeautifulSoup(html1,"html.parser")
    results = soup1.find("li",class_="slide")

    for result in results:
        news_title = result.find("div", class_="content_title").a.text
        news_p = result.find("div", class_="article_teaser_body").text

# News title of the latest news
    scrapedata["news_title"] = news_title
# News paragraph text of the latest news
    scrapedata["news_p"] = news_p


# JPL Mars Space Images - Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, "html.parser")

    featured_image_url = "https://www.jpl.nasa.gov"+soup2.body.find("img", class_="fancybox-image")["src"]
    
# Mars Space Featured Image
    scrapedata["featured_image_url"] = featured_image_url


# Mars Weather
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, "html.parser")

    mars_weather = soup3.find("div",class_="js-tweet-text-container").p.text

# Mars Weather Data
    scrapedata["mars_weather"] = mars_weather


# Mars Facts
    url4 = "https://space-facts.com/mars/"
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ["description","value"]
    #df.set_index("description",inplace = True)
    html_table = df.to_html(index=False)

# Mars Facts Table
    scrapedata["html_table"] = html_table


# Mars Hemispheres
    hemispheres = ["cerberus","schiaparelli","syrtis_major","valles_marineris"]
    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        url5 = f"https://astrogeology.usgs.gov/search/map/Mars/Viking/{hemisphere}_enhanced"
        browser.visit(url5)
        html5 = browser.html
        soup5 = BeautifulSoup(html5,"html.parser")
        hemisphere_image_url = {}
        title = soup5.find("h2", class_="title").text
        img_url = soup5.find("img", class_="wide-image")["src"]
        hemisphere_image_url["title"] = title
        hemisphere_image_url["img_url"] = "https://astrogeology.usgs.gov"+img_url
        hemisphere_image_urls.append(hemisphere_image_url)

# Mars Hemispheres Image and urls
    scrapedata["hemisphere_image_urls"] = hemisphere_image_urls

    return scrapedata

