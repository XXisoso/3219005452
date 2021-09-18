import profile
import jieba.posseg as pseg
import jieba
import jieba.analyse
import codecs
import math
import time


files = ['orig.txt','orig_0.8_add.txt','orig_0.8_del.txt',
         'orig_0.8_dis_1.txt','orig_0.8_dis_10.txt','orig_0.8_dis_15.txt']
text = [codecs.open(file,'r','utf8').read() for file in files] #读取文章

start = time.time();
#统计词汇出现的次数
from collections import Counter
def count(text,n=20):
    line = jieba.cut(text)
    line = [each.strip() for each in line] #去除空格
    counter = Counter(line)
    for words in counter.most_common(n):
        print('%-10s\t%d' % (words[0],words[1]))
    print('\n')

for i in range(len(text)):
    print("%s 词汇出现个数统计\n" %files[i])
    count(text[i])

#关键字提取
jieba.analyse.set_stop_words('stopwords.txt')
def print_topic(text):
    tags = jieba.analyse.extract_tags(text,topK=20,withWeight=True) #提取主题词
    print("%10s\t%s" %('关键词','权重'))
    for t, y in tags:
        print("%-10s\t%d" %(t,y*10000))
    print('')

for i in range(len(text)):
    print("%s 关键字提取\n")
    print_topic(text[i])

#相似度判断
def cut_word(text):
    res = jieba.analyse.extract_tags(text ,60,withWeight=True)
    return res

def TF_IDF(res1 = None,res2 = None):
    v1 = []
    v2 = []
    tf1 = {i[0]: i[1] for i in res1}
    tf2 = {i[0]: i[1] for i in res2}
    res = set(list(tf1.keys()) + list(tf2.keys()))

    for word in res:
        if word in tf1:
            v1.append(tf1[word])
        else:
            v1.append(0)
            if word in tf2:
                v2.append(tf2[word])
            else:
                v2.append(0)
    return v1,v2

def fenzi(v1,v2):
    return sum(a*b for a, b in zip(v1,v2))

def fenmu(v):
    return math.sqrt(sum(a*b for a,b in zip(v,v)))

def zhixing(v1,v2):
    return fenzi(v1,v2)/(fenmu(v1)*fenmu(v2))

def xiangsidu(text1,text2):
    v = TF_IDF(res1 = cut_word(text1), res2 = cut_word(text2))
    xiangshidujieguo=zhixing(v1=v[0],v2=v[1])
    return xiangshidujieguo
f = open("answer.txt",'w')
for i,j in [(0,1),(0,2),(0,3),(0,4),(0,5),]:
    print(' %s 和 %s 的相似度: %.2f'%(files[i],files[j],xiangsidu(text[i],text[j])+0.5),file = f)
end = time.time()
print("运行时间为："+str(end-start))
