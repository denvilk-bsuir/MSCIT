import re
from typing import List
from work import *

# reading text
text = None
with open('./test.cpp','r') as f:
    text = f.readlines()

# def text_without_defines(text: List):
#     return list(map(lambda x: x.strip(), filter(lambda x: not x.startswith("#") and x.strip(), text)))

# def str_without_single_comment(s: str):
#     single = r'(//([\w+ ]*))\s*(\n)*'
#     return re.split(single, s)[0]

# def text_without_single(text: List):
#     return list(map(str_without_single_comment, text))


text = text_without_single(text)

s = ''.join(text_without_defines(text))
s = text_without_comments(s)
# print(s)
# with open('output.txt','w+') as f:
#     print(s, file=f)

# VARIABLE_REG = r'((const\s*)?(T|auto|bool|char|char8_t|char16_t|char32_t|double|float|int|(long\sdouble)|long\slong|long|short int| short long|short double|short|size_t|signed|string|unsigned|void))\s*((\w*)\s*(=)?\s*(\w*)?,?\s*?)*\s*;'
REG = r'([a-zA-z]+\[\]|;|\d+\.\d+|\w+|\"\w+\"|\(|\)|\{|\}|\[|\]|\+=+|-=+|\*=+|/=+|%=+|\++|-+|\*+|\/+|%+|!=+|<+|<=+|>+|>=+|=+|;|.|\&\&|\&|\|\|)|(.+)"'


strings, s = find_all_strings(s)
chars, s = find_all_chars(s)
numbers, s = find_all_numbers(s)

print('\n'*5)
print(numbers)
nums = {}
for i in numbers:
    if not i in nums.keys():
        nums[i]=1
    else:
        nums[i]+=1

for k,v in nums.items():
    print(f'{k}  : {v}')
with open('output.cpp','w+') as f:
    print(s, file=f)

r1 = re.findall(REG, s)
# print(r1)
d={}
for x,y in r1:
    if (x in d.keys()):
        d[x]+=1
    else:
        d[x]=1

# print(d)
for k,v in d.items():
    print(f'{k}: {v}')

find_all_operators(s)