import requests
from PIL import Image
from io import BytesIO
import time

def lol_skin_image():
    for i in range(1,123):
        url_ori = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big'
        for j in range(20):
            url = url_ori + str(i)
            if(j<10):
                url = url + "00" + str(j) + ".jpg"
            else:
                url = url +'0' + str(j) + ".jpg"
            r = requests.get(url)
            if(r.status_code == 200):
                img =Image.open(BytesIO(r.content))
                img.save('/Users/light/PycharmProjects/spider/lol/pic/skin/'+str(i)+'/'+str(j)+".jpg")
                print(i,j)
        time.sleep(0.1)

def main():
    lol_skin_image()

if __name__ == "__main__":
    main()