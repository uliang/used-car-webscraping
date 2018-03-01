#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:46:53 2018

@author: uliang
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
import numpy as np
import pandas as pd
import time

#%% Helper functions
def strip_text(x):
    return all([x != split_string
                for split_string
                in ['', 'Available', 'Add to shortlist', 'Tags:']])

def main(): 
#%% Navigation and get listings
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://www.sgcarmart.com/used_cars/listing.php')
    sift = SoupStrainer('div', id='contentblank')
    #time.sleep(5)
    
    #%% Search for next page button and click.
    counter = 1
    while True:
        print("Reading page %d" % counter)
        start = time.time() 
        # Get listings
        html = BeautifulSoup(browser.page_source, "html.parser", parse_only=sift)
        listings = html.find_all('table', {'cellspacing':'0', 'cellpadding':'0',
                                           'width':'100%',
                                           'style': 'table-layout: fixed;'})
    
        # Data processing
        _data = [listing.get_text().split('\n') for listing in listings]
        _data = [map(str.strip, _dat) for _dat in _data]   
        data = [list(filter(strip_text, _dat)) for _dat in _data]
        
        fields = ["make", "list price", "depreciation", "date registered", "eng cap", "mileage", "date posted"]    
        
        data_array = np.array([dat[:6]+[dat[-2]] for dat in data])
        frame = pd.DataFrame(data_array, columns=fields)
        frame.to_csv("./data/%d.csv" % counter)
        
        no_link = html.find('span', class_='pageNoLink')
        no_link_number = no_link.text
        next_link_number = no_link.next_sibling.next_sibling.text
    
        ## Condition for clicking next
        if int(no_link_number)+1 == int(next_link_number) and counter < 3:
            go_to_next = browser.find_elements_by_partial_link_text("Next")
            print(go_to_next)
            try:
                go_to_next[1].click()
            except:
                go_to_next[0].click()
            finally:
                print("Unable to continue")
                break
        else:
            break
        
        counter += 1
        print("Time taken: %.4f s" % time.time()-start)
        
    browser.quit()
    print("Done")

#%%
# TODO: Append to master list

if __name__=="__main__": main()