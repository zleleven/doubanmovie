#coding:utf-8
import warnings
warnings.filterwarnings("ignore")
import re
import ssl
import jieba	#分词包
import numpy	#numpy计算包
import codecs	#codecs提供open方法来指定打开文件的语言编码，它会在读取的时候自动转换成内部unicode
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup as bs

import matplotlib.pyplot as plt
#%matplotlib inline

import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0,5.0)
from wordcloud import WordCloud

#分析网页函数
def getNowPlayingMovie_list():
	context = ssl._create_unverified_context()
	resp = urllib.request.urlopen('https://movie.douban.com/cinema/nowplaying/hangzhou/', context=context)
	html_data = resp.read().decode('utf-8')

	soup = bs(html_data,'html.parser')
	nowplaying_movie = soup.find_all('div',id='nowplaying')
	nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')

	nowplaying_list = []
	for item in nowplaying_movie_list:
		nowplaying_dict = {}
		nowplaying_dict['id'] = item['data-subject']
		for tag_img_item in item.find_all('img'):
			nowplaying_dict['name'] = tag_img_item['alt']
			nowplaying_list.append(nowplaying_dict)
	return nowplaying_list

#爬去网页函数
def getCommentsById(movieId,pageNum):
	context = ssl._create_unverified_context()
	eachCommentList = []
	if pageNum > 0:
		start = (pageNum-1) * 20
	else:
		return False

	requrl = 'https://movie.douban.com/subject/'+ movieId + '/comments?start='+ str(start) +'&limit=20'
	print (requrl)

	resp = urllib.request.urlopen(requrl, context=context)
	html_data = resp.read().decode('utf-8')
	soup = bs(html_data, 'html.parser')
	comment_div_lists = soup.find_all('div',class_='comment')

	for item in comment_div_lists:
		if item.find_all('p')[0].string is not None:
			eachCommentList.append(item.find_all('p')[0].string)

	return eachCommentList;

def main():
	commentList=[]
	NowPlayingMovie_list = getNowPlayingMovie_list();
	#循环获取第一个电影的前10页的评论
	for i in range(3):
		num = i + 1
		commentList_temp = getCommentsById(NowPlayingMovie_list[0]['id'], num)
		commentList.append(commentList_temp)

	#将列表中的数据转换为字符串
	comments = ''
	for k in range(len(commentList)):
		comments = comments + (str(commentList[k]).strip())

	#使用正则表达式去除标点符号
	pattern = re.compile(r'[\u4e00-\u9fa5]+')
	filterdata = re.findall(pattern, comments)
	clean_comments = ''.join(filterdata)

	#使用结巴分词进行中文分词
	segment = jieba.lcut(clean_comments)
	words_df = pd.DataFrame({'segment':segment})

	#去掉停用词
	stopwords = pd.read_csv("./stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'],encoding='utf-8')
	words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

	#统计词频
	words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
	words_stat=words_stat.reset_index().sort_values(by=["计数"], ascending=False)

	#进行云词显示
	wordcloud=WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)
	word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
	word_frequence_list = []
	for key in word_frequence:
		temp = (key,word_frequence[key])
		word_frequence_list.append(temp)

	wordcloud=wordcloud.fit_words(dict(word_frequence_list))
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()
#主函数
main()
