"""
Created on Sun Feb 21 12:24:01 2021

@author: Piyush
"""
import math
# from requests_module import Request
# from bs4 import BeautifulSoup
from utils import get_soup

class AmazonReviewsScraper:
    origin_url = 'https://amazon.com'
    
    def __init__(self, asin):
        
        self.review_url = self.get_review_url_from_asin(asin)
        self.soup = get_soup(self.review_url)
        self.total_pages = self.get_total_pages_from_reviews_url()
        self.last_page = self.total_pages if self.total_pages <= 500 else 500
        self.urls = self.generate_urls(self.review_url, 1, self.last_page)
        
    
    def get_review_url_from_asin(self, asin):
        base_url = 'https://amazon.com/dp/'
        product_url = base_url + asin
        
        try:
            soup = get_soup(product_url)
            
        except:
            raise Exception('Invalid ASIN!')
            
        review_url = self.origin_url + soup.select_one('a[data-hook=see-all-reviews-link-foot]').attrs.get('href')
        return review_url
        
    
        
        
    def get_total_pages_from_reviews_url(self, ):
        soup = self.soup
        total_reviews_section = soup.select_one('div[data-hook=cr-filter-info-review-rating-count]')
        start =total_reviews_section.text.find('| ') + 2
        end = total_reviews_section.text.find('global reviews')
        total_reviews = total_reviews_section.text[start:end].strip(' ').replace(',', '')
        if not total_reviews.isdigit():
            raise Exception('There is some problem in calculating total pages...')
            
        total_pages = math.ceil(int(total_reviews)/ 10)
        return total_pages
    
    def generate_urls(self, review_url, start_page, end_page):
        urls = list()
        s = review_url + '&pageNumber='
        for i in range(start_page, end_page + 1):
            url = s+ str(i)
            urls.append(url)
            
        return urls


    def get_details(self, soup):
        L = list()        
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
                
            
            try:
                review_text = review.select_one(
                    'span[class*=review-date]').text
                
                temp = review_text.find(' on ')
                review_date = review_text[temp + 4:]
                D['review_date'] = review_date
                
            except:
                D['review_date'] = None
            L.append(D)
            
            
        return L

    
test_asin = 'B07R8GD47V'
