import pdfplumber  # 导入库
import jieba
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
import os

file_path = 'dict.txt'
jieba.load_userdict(file_path)
class MyPDF:
    def __init__(self):
        self.canvas = canvas.Canvas(self.filename)
        self.canvas.setFont('myfont', 12)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 遍历当前目录下的所有PDF文件
for pdf_file in os.listdir('.'):
    if pdf_file.endswith('.pdf'):
        with pdfplumber.open(pdf_file) as f:
            text = ''
            for page in f.pages:
                page_text = page.extract_text()
                if page_text:  # 确保提取的文本不是None
                    text += page_text + '\n'

            # 将提取的文本保存到txt文件中
            with open(f'{pdf_file[:-4]}_temp.txt', mode='w', encoding='utf-8') as txt_f:
                txt_f.write(text)

file = open('temp.txt', encoding='utf-8')
file = file.read()  # 读取txt文件
txtlist = jieba.lcut(file)
string = " ".join(txtlist)
stop_words = {}
counts = {}
for txt in txtlist:
    if len(txt) == 1:
        stop_words[txt] = stop_words.get(txt, 0) + 1
    else:
        counts[txt] = counts.get(txt, 0) + 1
items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)
y1 = []
labels = []
for i in range(1, 10):
    y1.append(items[i][1])
    labels.append(items[i][0])
# plt.figure(figsize=(8,4))
width = 0.3
x = np.arange(len(y1))
a = [i for i in range(0, 9)]
plt.xticks(a, labels, rotation=30)
plt.bar(x=x, height=y1, width=width)
plt.title('PDF文件中热词统计分析')
plt.savefig("热词统计分析.png")
plt.show(block=False)
print("-------热词统计分析完成！-------")
stoplist = []
item = list(stop_words.items())
for i in range(len(item)):
    txt, count = item[i]
    stoplist.append(txt)
# print(stoplist)
setlist = set(stoplist)
wcd = WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc', scale=15, stopwords=setlist)
wcd.generate(string)
wcd.to_image()
print("-------热词词云生成完成！-------")
wcd.to_file('词云.png')  # 导出图片

