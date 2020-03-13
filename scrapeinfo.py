from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime

def init_browser():
    executable_path = {"executable_path": "C:/temp/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    news_url = "https://mars.nasa.gov/news/"
    twit_url = "https://twitter.com/marswxreport?lang=en"
    fact_url = "https://space-facts.com/mars/"
    img_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(news_url)

    # Scrape page into soup
    news_html = browser.html
    soup = BeautifulSoup(news_html, "html.parser")

    headline = soup.find('div', attrs={'class':'content_title'}).text
    para_text = soup.find('div', attrs={'class':'article_teaser_body'}).text
        # Store in dictionary
    mars1 = {
            "headline": headline,
            "text": para_text,

        }
    browser.visit(twit_url)

    # Scrape page into soup
    mars_weather_html = browser.html
    soup = BeautifulSoup(mars_weather_html, "html.parser")

    mars_weather = soup.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
        

    table = pd.read_html(fact_url)
    tabledf = table[0]
    tabledf.columns = ['Variable','Value']
    tabledf.set_index('Variable', inplace=True)

    browser.visit(img_url)
    img_html = browser.html
    soup = BeautifulSoup(img_html, "html.parser")
    hemi = soup.find_all("h3")
    for sphere in hemi:
        browser.click_link_by_partial_text("Hemisphere")
        hemis = soup.find_all("div", class_="description")
    mars_dict={}
    hemisphereurls=[]
    for parts in hemis:
        link = result.find('a')
        href = link['href']
        title = link.find('h3').text
        togoto = "https://astrogeology.usgs.gov" + href
        browser.visit(togoto)
        imgloc_html = browser.html
        soup = bs(imgloc_html, 'html.parser')
        pic = soup.find("a", target="_blank")
        imgref = pic['href']
        hemisphereurls.append({"title":title,"img_url":imgref})


mars_info_dict = {"headline":headline,"text":text,"mars_weather":mars_weather,"facts_table":tabledf,"hemisphere_img":hemisphereurls}

browser.quit()

return mars_info_dict