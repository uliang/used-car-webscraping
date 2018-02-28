#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:46:53 2018

@author: uliang
"""
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
# import re

#%% Helper functions
def custom_text_seive(x):
    return all([x != split_string
                for split_string
                in ['', 'Available', 'Add to shortlist', 'Tags:']])

#%% Navigation and get listings
browser = webdriver.Chrome()
browser.get('http://www.sgcarmart.com/used_cars/listing.php')
sift = SoupStrainer('div', id='contentblank')
html = BeautifulSoup(browser.page_source, "html.parser", parse_only=sift)
listings = html.find_all('table', {'cellspacing':'0', 'cellpadding':'0',
                                   'width':'100%',
                                   'style': 'table-layout: fixed;'})

#%% Data processing
_data = [listing.get_text().split('\n') for listing in listings]
data = [map(lambda x:x.strip(), _dat) for _dat in _data]
data = [list(filter(custom_text_seive, dat)) for dat in data]

#TODO Further data processing and merge into np.array
#%% Search for next page button and click.

while True:
    # TODO: Get listings
    # TODO: Data processing
    # TODO: Append to master list
    no_link_number = html.find('span', class_='pageNoLink').text
    next_link_number = no_link_number.next_sibling.next_sibling.text

    ## Condition for clicking next
    if int(no_link_number)+1== next_link_number:
        go_to_next = browser.find_element_by_partial_link_text('Next')
        go_to_next.click()
    # break out of loop
    else:
        break


