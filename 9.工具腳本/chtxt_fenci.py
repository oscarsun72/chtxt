#!/usr/bin/env python3
# images generator with wordcloud
# https://github.com/bgc2017/chtxt
# Usage: fenci.py <max_words> <source_txt_file> <target_png_file>
# fenci.py 150 詩經.txt shijing.png 

import jieba
import sys
from random import randint
import wordcloud
from matplotlib import colors

custom=2
margin=5
image_width=1024 
image_height=768
relative_scaling=0.02
jieba_cut_all=False

maxword=int(sys.argv[1])
source_txt_file=sys.argv[2]
target_png_file=sys.argv[3]

if custom == 1:
    # 正苏新诗柳楷-简体
    default_font="Font_liukaiJ.ttf"
elif custom == 2:
    # 康熙字典-繁体 
    default_font="Font_kangxi.ttf"
elif custom == 3:
    # MacOS 苹方字体
    default_font="/System/Library/fonts/PingFang.ttc"
else:
    default_font="I.Ming-7.01.ttf"
    
txt_file=source_txt_file
txt = open(txt_file, "r", encoding='utf-8').read()

# 分詞字典
#user_dict="/chinese_words_final.dict"
#jieba.load_userdict(user_dict)
jieba.set_dictionary('/chinese_words_final.dict')

# color map
color_list=["#FB2E91","#53D3BE","#B34BE5","#D95B5B","#737779","#5BBD72","#737779","#D84999","#F2C61F","#8D7DE5","#564E8A","#B34BE5","#232325","#01B4AD","#01B4AD","#DF7B53","#53D3BE","#5BBD72","#F2450C","#E08712","#6495ED","#FF1493","#57508A","#57508A","#564E8A","#F2450C","#3A82BF","#FF1493","#199422","#D95B5B","#8D7DE5","#F2C61F","#D84999","#3A82BF","#DF7B53","#E08712","#5BBD72","#232325","#6495ED","#5BBD72"]
colormap=colors.ListedColormap(color_list)

removes =["子曰","曰"]

words = jieba.lcut(txt,cut_all=jieba_cut_all)
words = [w for w in words if w not in removes]
txt_1 = " ".join(words)
#print(txt_1)

w = wordcloud.WordCloud(font_path=default_font, width=image_width, height=image_height, background_color="white",collocations=False,prefer_horizontal=1,relative_scaling=relative_scaling,max_words=maxword,margin=margin,repeat=False,mode="RGBA",colormap=colormap)
w.generate(txt_1)
w.to_file(target_png_file)
