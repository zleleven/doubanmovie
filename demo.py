#coding:utf-8
import matplotlib.pyplot as plt
import jieba
import codecs
from wordcloud import WordCloud

text_from_file_with_apath = open('test.txt').read()

wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
wl_space_split = " ".join(wordlist_after_jieba)

#wordcloud=WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)
my_wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80).generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()