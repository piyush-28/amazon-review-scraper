# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 12:30:15 2021

@author: Piyush
"""

from requests_module import Request
from bs4 import BeautifulSoup

def get_soup(url):
    
    resp = Request.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup



def clean_reviews(dic):
    new_dic = dic.copy()
    new_dic['review_body'] = new_dic['review_body'].strip('\n').strip(' ')
    return new_dic
