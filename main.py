# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 22:56:37 2021

@author: Piyush
"""

import pandas as pd
from bs4 import BeautifulSoup
import time
from requests_module import Request







def get_details(url):
    L = list()
    resp = Request.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    
    reviews = soup.select('div[id*=customer_review]')
    for review in reviews:
        D = {
        'username' : None, 
        'profile_link': None,
        'rating' : None,
        'review_title': None, 
        'review_body': None
        }
        
        try:
            D['username'] = review.select('span[class=a-profile-name]')[0].text
            
        except:
            D['username'] = None
            
        try:
            D['profile_link'] = 'https://amazon.com' + review.select('div[data-hook=genome-widget]')[0].a['href']
        except:
            D['profile_link'] = None
            
        try:
            D['rating'] = review.select_one('i[data-hook=review-star-rating]').text.rstrip('out of 5 stars')
        except:
            try:
                D['rating'] = review.select_one('i[data-hook=cmps-review-star-rating]').text.rstrip('out of 5 stars')
            except:
                D['rating'] = None
            
        
        try:
            D['review_title'] = review.select_one('a[data-hook=review-title]').text.strip('\n')
        except:
            try:
                D['review_title'] = review.select_one('span[data-hook=review-title]').text.strip('\n')
            except:
                D['review_title'] = None
            
        try:
            D['review_body'] = review.select_one('span[data-hook=review-body]').text
            
        except:
            D['review_body'] = None
        L.append(D)
        
        
    return L



def generate_urls(parent_url, start_page, end_page):
    L = list()
    if '&pageNumber=' in parent_url:
        parent_url.strip('')
    
    for i in range(start_page, end_page + 1):
        url = parent_url + '&pageNumber=' + str(i)
        L.append(url)
        
    return L



def save_to_csv(data, path):
    df = pd.DataFrame(data)
    try:
        df.to_csv(path)
    except:
        print("Unable to save to CSV")
        
        
        

def clean_reviews(dic):
    new_dic = dic.copy()
    new_dic['review_body'] = new_dic['review_body'].strip('\n').strip(' ')
    return new_dic


def main(url, start_page, end_page, path):
    urls = generate_urls(url, start_page, end_page)
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

