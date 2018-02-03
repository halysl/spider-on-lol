import string
li = []
with open('name.txt','r') as f:
    for line in f.readlines():
        a = line[:-2]
        li.append(a)
        print(a)

print(li)