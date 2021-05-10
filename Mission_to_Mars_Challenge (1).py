#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[4]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[5]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[6]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[7]:


slide_elem.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
#img_soup


# In[13]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[16]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[17]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[34]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[35]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere_pages = []
hemisphere_names = []
hemisphere_list_dicts = []
hemispheres = {}
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
    print(h3)
   
    a = image.find('a')
    href = a['href']
    #print(href)
    hemisphere_pages.append(f'https://www.marshemispheres.com/{href}')

print(hemisphere_pages)



   


# In[36]:


#click thumbnail
for i in hemisphere_pages:
    #test = "https://www.marshemispheres.com/cerberus.html"
    browser.visit(i)
    html = browser.html
    soupy = soup(html, 'html.parser')

    #get the image url
    extension = soupy.find('img', class_="wide-image").get('src')
    print(extension)
    hemisphere_image_urls.append(f'https://www.marshemispheres.com/{extension}')
    

print(hemisphere_image_urls)

#add the title and url to the hemisphere_info dict


# In[38]:


for i in range(0,4):
    hemispheres['img_url'] = hemisphere_image_urls[i]
    hemispheres['title'] = hemisphere_names[i]
    hemisphere_list_dicts.append(hemispheres)

print(hemisphere_list_dicts)


# In[29]:


hemisphere_dict = {hemisphere_names[i]: hemisphere_image_urls[i] for i in range(len(hemisphere_names))}
#hemisphere_dict


# In[30]:


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_dict)


# In[31]:


# 5. Quit the browser
browser.quit()


# In[ ]:




