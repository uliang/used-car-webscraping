#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:46:53 2018

@author: uliang
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup, SoupStrainer
from progress.spinner import Spinner
from datetime import timedelta
import numpy as np
import pandas as pd
import time
import click
import os

#%% Helper functions
def strip_text(x):
    return all([x != split_string
                for split_string
                in ['', 'Available', 'Add to shortlist', 'Tags:']])

#%% Main application loop
@click.command()
@click.option('--headless/--no-headless', default=False, help='Whether not to show browsing'+
              ' window or not')
@click.option('--max_page', default=1, help='Max number of pages to scrape starting' +
              ' from the most recent listings. Default is 1.'+
              ' Pass -1 to scrape all listings.')
def main(headless, max_page): 
    MAX_COUNT = max_page

    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    if headless: options.add_argument("headless")

    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://www.sgcarmart.com/used_cars/listing.php')
    sift = SoupStrainer('div', id='contentblank')
    spin = Spinner('Scraping...')
    
    counter, start = 1, time.time() 
    while True:
        
        # Get listings
        html = BeautifulSoup(browser.page_source, "html.parser", parse_only=sift)
        listings = html.find_all('table', {'cellspacing':'0', 'cellpadding':'0',
                                           'width':'100%',
                                           'style': 'table-layout: fixed;'})
        spin.next()
        # Data processing
        _data = [listing.get_text().split('\n') for listing in listings]
        _data = [map(str.strip, _dat) for _dat in _data]   
        data = [list(filter(strip_text, _dat)) for _dat in _data]
        
        fields = ["make", "list price", "depreciation", "date registered",
                  "eng cap", "mileage", "date posted"]    
        
        data_array = np.array([dat[:6]+[dat[-2]] for dat in data])
        frame = pd.DataFrame(data_array, columns=fields)
        frame.to_csv("./data/%d.csv" % counter)
        spin.next()
        ## Condition for clicking next
        no_link = html.find('span', class_='pageNoLink')
        next_link_number = no_link.next_sibling.next_sibling.text
    
        scrape_next_page = next_link_number.isalnum()
        if MAX_COUNT != -1: 
            scrape_next_page = scrape_next_page and counter < MAX_COUNT
            
        if scrape_next_page:
            
            # Search for next page button and click.
            go_to_next = browser.find_element_by_partial_link_text("Next")
            try:
                go_to_next.click()
            except:
                action = ActionChains(browser)
                action.pause(20)
                action.move_to_element(go_to_next)
                action.click(go_to_next)
                action.perform()
        else:
            break
        
        counter += 1
        spin.next()
        
    browser.quit()
    time_taken = str(timedelta(seconds = time.time()-start))
    print("Time taken: %s" % (time_taken))
    print("Done")
#%%
# TODO: Append to master list

if __name__=="__main__": 
    try:
        os.system('cls')
    except:
        os.system('clear')
    main()