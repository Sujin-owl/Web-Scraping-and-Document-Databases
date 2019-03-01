#!/usr/bin/env python
# coding: utf-8

# ### Import Dependencies

import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
# ### Define URL to scrape and inform the browser to visit the page
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

# ### Scrape content from the website (latest news title and paragraph text)

# Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# Using BS, we can execute standard functions to capture the page's content
    quotes = soup.find_all('li', class_='slide')
    news_title = quotes[0].h3.text
    news_p = quotes[0].a.text
# ### Define JPL URL to scrape and inform the browser to visit the page

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

### Find the largesize image URL 

# Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# ### Go to next page with FULL IMAGE link

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

# ### Go to large size image link 

    browser.click_link_by_partial_text('more info')

# ### Scrape the image url from the new website

    new_html = browser.html
    new_soup = BeautifulSoup(new_html, 'html.parser')
    image = new_soup.find('img', class_='main_image')
    image_url = image.get('src')

# ### Assign the url string to a variable called 'featured_image_url'

    featured_image_url = 'https://www.jpl.nasa.gov'+image_url

# ### Mars Weather
# Define the weather url and inform the browser to visit the page
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

# Using bs to capture the page's content
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
# Scrape the latest (first) news about the mars weather
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

# ### Mars Facts

    facts_url = 'http://space-facts.com/mars/'

# ### Scrape the table information from the defined url and save as pandas

    table = pd.read_html(facts_url)
    table[0]

    df = table[0]
    df.columns = ['Parameters', 'Facts']
    html_table = df.to_html()

# ### Mars Hemispheres

# ### Define the USGS url and inform the browser to visit the page
    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_url)

# Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
    hemis_html = browser.html
    soup = BeautifulSoup(hemis_html, 'html.parser')

# Using BS, we can execute standard functions to capture the page's content
    titles = soup.find_all('div', class_='item')
# define an empty dictionary to store the title and image_url data
    hemisphere_image_urls = []
# ### Iterate each title and scrape the title and image url string, store the data into the dictionary

    for title in titles:
    # scrape the hemisphere title
        image_title = title.h3.text
    # go to the title's link
        browser.click_link_by_partial_text(image_title)
        time.sleep(5)
    # scrape the high resolution hemisphere image url 
        full_html = browser.html
        full_soup = BeautifulSoup(full_html, 'html.parser')
        full_quote = full_soup.find('div',class_ = 'downloads')
        full_url = full_quote.a['href']
    # store the hemisphere title and image url string into the dictionary
        hemisphere_image_urls.append({"title": image_title, "image_url": full_url})
        browser.back()
    # return data
    mars_data = {"News_Title":news_title, "News_Paragraph":news_p, "Featured_Image_URL":featured_image_url,"Mars_Weather":mars_weather, "HTML_Table":html_table, "Hemisphere_Image_URLs":hemisphere_image_urls}
    return mars_data

