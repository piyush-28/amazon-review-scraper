# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 22:56:37 2021

@author: Piyush
"""

import pandas as pd
import time
import traceback
from utils import clean_reviews
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


def main(asin):
    scraper = AmazonReviewsScraper(asin)
    
    L = list()
    for url in urls:
        print('Scraping Page: ', url)
        print('--------------------------------------------------------------------------------------')
        details = get_details(url)
        L += details
        L = list(map(clean_reviews, L))
        print('Saving to CSV...')
        print('--------------------------------------------------------------------------------------')
        save_to_csv(L, path)
        time.sleep(1.5)
        
        
        
test_url= 'https://www.amazon.com/Polaroid-Color-I-Type-Film-Photos/product-reviews/B084SDXVBD/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&filterByStar=positive'


url = input('Enter the url: ')
first_page_num = int(input('Enter the starting page for scraping: '))
last_page_num = int(input('Enter the last page for scraping: '))
csv_path = input('Enter the CSV Path: ')
main(url, first_page_num, last_page_num, csv_path)

