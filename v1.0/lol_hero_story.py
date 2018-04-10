# -*-coding = utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

def createHeroName():
    hero_name = []
    with open('/Users/light/PycharmProjects/spider/lol/name.txt', 'r') as f:
        for line in f.readlines():
            a = line[:-2]
            hero_name.append(a)
    return hero_name

def lol_hero_stoiry(hero_name):
    for i in hero_name:
        try:
            url = 'http://lol.qq.com/biz/hero/'+i+'.js'
            r = requests.get(url)
            r.encoding = 'utf-8'
            demo = r.text
            start = demo.find('lore')
            end = demo.find('blurb')
            demo = demo[start:end]
            demo = demo[7:-3]
            demo = demo.replace("<br>","")
            demo = demo.encode('utf-8').decode('unicode_escape')
            soup = BeautifulSoup(demo,'html.parser')
            os.system('touch /Users/light/PycharmProjects/spider/lol/hero_story/'+i+".txt")
            with open('/Users/light/PycharmProjects/spider/lol/hero_story/'+i+".txt",'w') as f:
                f.write(demo)
            print(demo)
        except:
            continue

def main():
    hero_name = createHeroName()
    lol_hero_stoiry(hero_name)

if __name__ =="__main__":
    main()