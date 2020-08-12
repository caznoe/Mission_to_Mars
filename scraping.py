# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# Initialize the browser, create a data dictionary, end the webdriver.
def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)
   
   news_title, news_paragraph = mars_news(browser)
   # Run all scraping functions and store results.
   data = {"news_title": news_title, "news_paragraph": news_paragraph, "featured_image": featured_image(browser), "facts": mars_facts(), "hemispheres": hemispheres(browser), "c_hemisphere": c_hemisphere(browser), "s_hemisphere": s_hemisphere(browser), "vm_hemisphere": vm_hemisphere(browser), "sm_hemisphere": sm_hemisphere(browser), "last_modified": dt.datetime.now()}
   # Stop webdriver and return data
   browser.quit()
   return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a Beautifulsoup object
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

def hemispheres(browser):

    c_hem_img_url = c_hemisphere(browser)
    s_hem_img_url = s_hemisphere(browser)
    sm_hem_img_url = sm_hemisphere(browser)
    vm_hem_img_url = vm_hemisphere(browser)
    
    hemispheres = [{"Cerberus Hemisphere": c_hem_img_url}, {"Schiaparelli Hemisphere": s_hem_img_url}, {"Syrtis Major Hemisphere" : sm_hem_img_url}, {"Valles Marineris Hemisphere" : vm_hem_img_url}]
    return hemispheres
    

def c_hemisphere(browser):

    #Visit URL
    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_unenhanced.tif/full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        c_img_url = img_soup.select_one('body img').get("src")

    except AttributeError:
        return None

    return c_img_url

def s_hemisphere(browser):

    #Visit URL
    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_unenhanced.tif/full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        s_img_url = img_soup.select_one('body img').get('src')

    except AttributeError:
        return None

    return s_img_url

def sm_hemisphere(browser):

    #Visit URL
    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_unenhanced.tif/full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        sm_img_url = img_soup.select_one('body img').get('src')

    except AttributeError:
        return None

    return sm_img_url

def vm_hemisphere(browser):

    #Visit URL
    url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_unenhanced.tif/full.jpg'
    browser.visit(url)

    #Parse the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        vm_img_url = img_soup.select_one('body img').get('src')

    except AttributeError:
        return None

    return vm_img_url

# ## Mars Facts
def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    return df.to_html()

browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
