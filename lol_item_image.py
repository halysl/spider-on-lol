import requests
from io import BytesIO
from PIL import Image
import time
def lol_item_img():
    for i in range(2000,4000):
        url = 'http://ossweb-img.qq.com/images/lol/img/item/'+str(i)+".png"
        r = requests.get(url)
        if(r.status_code == 200):
            img = Image.open(BytesIO(r.content))
            img.save('/Users/light/PycharmProjects/spider/lol/pic/item/'+str(i)+".png")
            print(i)
        time.sleep(0.1)

def main():
    lol_item_img()

if __name__=="__main__":
    main()