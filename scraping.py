
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #initialize headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }

    #stop webdriver and return data
    browser.quit()
    return data

#define funcitons
def mars_news(browser):

    # scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # convert the browser html to a soup object and then quite the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling:
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    #Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    #use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        #scrape the table from the Mars Facts page using pd.read_html
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
            return None

    #assign columns and set the index
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    #conver the datafram into html format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    hemisphere_pages = []
    hemisphere_names = []
    hemispheres = {}
    hemisphere_list_dicts = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')
    images = img_soup.find_all('div', class_='item')

    #loop for title and hemisphere page url
    for image in images:
        h3 = image.find('h3').text
        #grab the title and list it
        hemisphere_names.append(h3)
        a = image.find('a')
        href = a['href']
        #grab the intermediary link and list it
        hemisphere_pages.append(f'https://www.marshemispheres.com/{href}')

    #loop for full image url
    for i in hemisphere_pages:
        browser.visit(i)
        html = browser.html
        soupy = soup(html, 'html.parser')

        #get the final image url
        extension = soupy.find('img', class_="wide-image").get('src')
        hemisphere_image_urls.append(f'https://www.marshemispheres.com/{extension}')

    for i in range(0,4):
        hemispheres = {}
        hemispheres['img_url'] = hemisphere_image_urls[i]
        hemispheres['title'] = hemisphere_names[i]
        hemisphere_list_dicts.append(hemispheres)


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_list_dicts

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())