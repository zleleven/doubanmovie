#coding:utf-8
import codecs
import urllib.request
from bs4 import BeautifulSoup as bs

def crawldouban():
    requrl = 'https://movie.douban.com/top250'
    resp = request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    movie_list = soup.find_all('div', class_='item')

    
