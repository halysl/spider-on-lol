import os
import sys

# 将下载的图片文件重命名
# 打开名字文件
with open('../lol-skin-info.json','r') as f:
    # 按行读取，依次命名
    for line in f.readlines():
        temp = line.strip()

        # 获得原文件名
        index1 = line.find("image_id")
        index2 = line.find("image_urls")
        image_id = temp[index1 + 12:index2 - 4]
        image_address = os.getcwd() + "/img/hero_skin_img/full/" + image_id
        
        # 创建新文件名
        index3 = line.find("image_names")
        rename = temp[index3 + 15:-2]
        rename = os.getcwd() + "/img/hero_skin_img/full/" + rename
        
        # 命名
        os.rename(image_address,rename)