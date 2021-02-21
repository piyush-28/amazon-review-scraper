# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 22:56:37 2021

@author: Piyush
"""

import pandas as pd
import time
import traceback
from utils import clean_reviews, get_soup
from amazon_reviews_scraper import AmazonReviewsScraper



def save_to_csv(data, path):
    df = pd.DataFrame(data)
    try:
        df.to_csv(path)
    except:
        traceback.print_exc()
        print("Unable to save to CSV")
        
        
        

#def clean_reviews(dic):
#    new_dic = dic.copy()
#    new_dic['review_body'] = new_dic['review_body'].strip('\n').strip(' ')
#    return new_dic


def main(asin, path):
    scraper = AmazonReviewsScraper(asin)
    urls = scraper.urls
    
    L = list()
    for url in urls:
        print('Scraping Page: ', url)
        print('--------------------------------------------------------------------------------------')
        soup = get_soup(url)
        details = scraper.get_details(soup)
        L += details
        L = list(map(clean_reviews, L))
        print('Saving to CSV...')
        print('--------------------------------------------------------------------------------------')
        save_to_csv(L, path)
        time.sleep(1.5)
        
        
        

asin = input('Enter the asin number of the product: ')

csv_path = input('Enter the CSV Path: ')
main(asin, csv_path)




