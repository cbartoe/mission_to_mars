# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

#convert the df to html
df.to_html()



# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
#______________________________________________________________________#


url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere_pages = []
hemisphere_names = []
hemisphere_dict = {}

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')
images = img_soup.find_all('div', class_='item')
#print(images)
# hemisphere_image_urls = [image.get('a') for image in images]
# hemisphere_image_urls

for image in images:
    h3 = image.find('h3').text
    hemisphere_names.append(h3)
    a = image.find('a')
    href = a['href']
    hemisphere_pages.append(f'https://www.marshemispheres.com/{href}')

print(hemisphere_pages)

#click thumbnail
for i in hemisphere_pages:
    #test = "https://www.marshemispheres.com/cerberus.html"
    browser.visit(i)
    html = browser.html
    soupy = soup(html, 'html.parser')

    #get the image url
    extension = soupy.find('img', class_="wide-image").get('src')
    hemisphere_image_urls.append(f'https://www.marshemispheres.com/{extension}')

for i in range(0,4):
    hemispheres['img_url'] = hemisphere_image_urls[i]
    hemispheres['title'] = hemisphere_names[i]
    hemisphere_list_dicts.append(hemispheres)

#add the title and url to the hemisphere_info dict
hemisphere_dict = {hemisphere_names[i]: hemisphere_image_urls[i] for i in range(len(hemisphere_names))}

# 5. Quit the browser
browser.quit()



