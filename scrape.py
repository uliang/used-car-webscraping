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
import re

#%% Helper functions
SEARCH_POSTED = lambda s: re.search('Posted', s) is not None

def strip_text(x):
    return all([x != split_string
                for split_string
                in [',', 'Available', 'Add to shortlist', 'Tags:']])

def get_posted_date(dat):
    mask = [SEARCH_POSTED(s) for s in dat]
    posted_index = mask.index(True)
    return dat[posted_index]
    

#%% Main application loop
@click.command()
@click.option('--headless/--no-headless', default=True, help='Whether to show browsing'+
              ' window or not')
@click.option('--max_page', default=1, help='Max number of pages to scrape starting' +
              ' from the most recent listings. Default is 1.'+
              ' Pass -1 to scrape all listings.')
def main(headless, max_page): 
    MAX_COUNT = max_page

    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    if headless: options.add_argument("headless")
    
    print("Accessing website\n")

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
        data = [list(filter(strip_text, listing.stripped_strings)) for listing 
                in listings]
        
        fields = ["make", "list price", "depreciation", "date registered",
                  "eng cap", "mileage","veh type", "date posted"]    
        
        data_array = np.array([dat[:7]+[get_posted_date(dat)] for dat in data])
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
            finally:
                counter += 1
                spin.next()  
        else:
            break
        
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