#coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from time import sleep
import logging
import urllib.request
import ssl

#登录
def login(url, username, password):
	brower.get(url)
	brower.find_element_by_css_selector('[class="nav-login"]').click()
	name = brower.find_element_by_id('email')
	name.clear()
	name.send_keys(username)
	pwd = brower.find_element_by_id('password')
	pwd.clear()
	pwd.send_keys(password)

	pic_src = brower.find_element_by_id('captcha_image').get_attribute('src')
	#调用方法获取验证码
	cap_value = get_yzm(pic_src)
	yan_zheng_ma = brower.find_element_by_id('captcha_field')
	yan_zheng_ma.clear()
	yan_zheng_ma.send_keys(cap_value)
	brower.find_element_by_css_selector('[class="btn-submit"]').click()
	print("登录成功")

def get_yzm(src):
	print ("正在保存验证码")
	print (src)
	context = ssl._create_unverified_context()
	captchapicfile = "/Users/eleven/Pictures/captcha.png";
	#urllib.request.urlretrieve(src, filename=captchapicfile)
	print ("请打开图片输入验证码：")
	captcha_value = input()
	return captcha_value

def search(movie_name):
	inp_query = brower.find_element_by_id('inp-query')
	inp_query.clear()
	inp_query.send_keys(movie_name)
	btn_search = brower.find_element_by_css_selector('[type="submit"]')
	btn_search.click()
	#print (brower.page_source)
	sleep(10)
	#brower.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/a').click()
	brower.get('https://movie.douban.com/subject/26985127/?from=showing')
	print("进入详情页")

def into_comments():
	#print (brower.page_source)
	sleep(5)
	#brower.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span/a').click()
	brower.get('https://movie.douban.com/subject/26985127/comments?status=P')
	print ("进入短评列表")

def get_comments():
	wait.until(lambda brower : brower.find_element_by_css_selector('[class="next"]'))
	sleep(1)
	print (brower.page_source)
	for i in range(1,21):
		comment = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/p'.format(str(i))).text
		#comment_name = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a'.format(str(i))).text
		#votes = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div2/h3/span[1]/span'.format(str(i))).text

		data = {
			'comment' : comment
			#'comment_name' : comment_name,
			#'votes' : votes
		}

		comments.insert_one(data)
		print ('*'*100)
		print (data)
		print ('成功写入数据库')

def next_page():
	next = brower.find_element_by_css_selector('[class="next"]')
	try:
		next.click()
	except:
		logging.info("全部完成")




URL='https://movie.douban.com/'
username='lzeleven@126.com'
password='zl5263642'
movie='一出好戏'

client = MongoClient('localhost',27017)
next_our = client['next_our']
comments = next_our['comments']

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
brower = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(brower, 10)
#brower = webdriver.PhantomJS(executable_path="/Users/eleven/Documents/phantomjs/bin/phantomjs")

if __name__ == '__main__':
	
	login(URL, username, password)
	search(movie)
	into_comments()
	for page in range(24):
		get_comments()
		next_page()