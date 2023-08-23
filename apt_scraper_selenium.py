# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:39:55 2020

@author: bdaet
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re


#initializing the webdriver
options = webdriver.ChromeOptions()
    
#set path to driver
driver = webdriver.Chrome(options = options)
driver.set_window_size(1120, 1000)
    
url = 'https://www.apartments.com/oakland-ca/'

#number of pages to scrape, looks like there are 25 listings per page
num_pages = 28

#max delay for WebDriverWait function
max_delay = 5
        
df = pd.DataFrame()

#looping through specified number of pages
for j in range(num_pages):
    print('Page Number: {}'.format('' + str(j+1)))
    
    if j > 0:
        driver.get(url+'/'+str(j+1)+'/')
    else:
        driver.get(url)
    
    
    #going through each apartment listing on page
    num_placards = len(driver.find_elements_by_class_name('placardTitle'))
    for i in range(num_placards):
        print('Progess: {}'.format('' + str(i+1) + '/' + str(num_placards)))
        
        #wait for web page to load before getting list of placardTitle elements
        WebDriverWait(driver, max_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'placardTitle')))        
        apt_buttons = driver.find_elements_by_class_name('placardTitle')
        
        
        apt_buttons[i].click()

        #wait for web page to load before scraping
        WebDriverWait(driver, max_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'rentalGridRow')))
        
        listings_dict = ({'Title' : [],
                        'Address' : [],
                        'Bedrooms' : [],
                        'Bathrooms' : [],
                        'Rent' : [],
                        'Square Footage': [],
                        'Availability': [],
                        'Amenities': []})
        
        #getting elements for entire property
        title = driver.find_element_by_class_name('propertyName').text
        address = driver.find_element_by_class_name('propertyAddress').text
        
        amenities = driver.find_element_by_class_name('amenitiesSection')
        amenity_rows = amenities.find_elements_by_css_selector('li')
        amenity_data = []
        for row in amenity_rows:
            amenity = re.sub(u'•', '', re.sub('<[^<]+?>', '', row.get_attribute('innerHTML')))
            amenity_data.append(amenity)
        amenity_string = ', '.join(amenity_data)

        #getting elements for each apartment
        rows = driver.find_elements_by_class_name('rentalGridRow')
        for row in rows:
            try:
                if row.find_element_by_class_name('rent').text == u'':
                    continue
                listings_dict['Bedrooms'].append(row.find_element_by_class_name('beds').text)
                listings_dict['Bathrooms'].append(row.find_element_by_class_name('baths').text)
                listings_dict['Rent'].append(row.find_element_by_class_name('rent').text)
                listings_dict['Square Footage'].append(row.find_element_by_class_name('sqft').text)
                listings_dict['Availability'].append(row.find_element_by_class_name('available').text)
                listings_dict['Title'].append(title)
                listings_dict['Address'].append(address)
                listings_dict['Amenities'].append(amenity_string)
            except NoSuchElementException:
                continue
        
        #converting dictionary to dataframe
        listing_df = pd.DataFrame(listings_dict)
        
        #adding data from this listing to larger dataframe with data for all listings
        df = pd.concat([df, listing_df], axis = 0, sort = False)
        
        
        driver.back()   #to go back to main page
        
        
#resetting index for dataframe
df.reset_index(drop = True, inplace = True)

df.to_csv('oakland_apartment_data.csv', index = False)
