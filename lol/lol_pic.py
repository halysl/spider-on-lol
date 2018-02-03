import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
from PIL import Image

def createdata():
    li = []
    with open('/Users/light/PycharmProjects/spider/lol/name.txt', 'r') as f:
        for line in f.readlines():
            a = line[:-2]
            li.append(a)
    return li

def getdata(li):
    for i in li:
        print(i)
        try:
            url = 'http://ossweb-img.qq.com/images/lol/img/champion/'+i+'.png'
            r = requests.get(url)
            image = Image.open(BytesIO(r.content))
            image.save('/Users/light/PycharmProjects/spider/lol/pic/'+i+'.png')
            print('/Users/light/PycharmProjects/spider/lol/pic/'+i)
        except:
            print(url)
            continue
    print("Done!")



def main():
    li = createdata()
    getdata(li)

if __name__ =="__main__":
    main()