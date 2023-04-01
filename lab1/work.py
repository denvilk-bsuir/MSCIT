from typing import List
import re

UNUSED = '±'

RESERVED = [
    'for', 
    'while', 
    'switch', 
    'case', 
    'if', 
    'do',
    'and', 
    'or', 
    'xor', 
    'try', 
    'new', 
    'new[]', 
    'delete', 
    'delete[]', 
    'catch',
    'break', 
    'return', 
    'continue', 
    'goto',
    # 'cout', 'cin'
    '>>=', '<<=', '>=', '<=', '<<', '>>', '+=', '-=', '==', '!=', '->',
         '*=', '/=', '%=', '&=', '|=', '^=', '&&', '||', '++', '--', '::',
         '+', '-', '/', '*', '=', '%', '&', '|', '^', '>', '<', '!',
         '~', '?', ':', '(', ')', '{', '}', '[', ']', ',', ';', '...',
]


def text_without_defines(text: List):
    return list(map(lambda x: x.strip(), filter(lambda x: not x.startswith("#") and x.strip(), text)))

def str_without_single_comment(s: str):
    single = r'(//([\w+ ]*))\s*(\n)*'
    return re.split(single, s)[0]

def text_without_single(text: List):
    return list(map(str_without_single_comment, text))

def text_without_comments(text: str):
    i = -1
    while (i:=text.find('/*'))!=-1:
        j = text.find('*/')
        text = text[:i]+text[j+2:]
    return text

def find_all_strings(text:str):
    i = -1
    l = []
    while (i:=text.find('"'))!=-1:
        j = text.find('"', i+1)
        l.append(text[i+1:j])
        text=text[:i]+UNUSED+text[j+1:]
    return (l, text)

def find_all_chars(text:str):
    i = -1
    l = []
    while (i:=text.find("'"))!=-1:
        j = text.find("'", i+1)
        l.append(text[i+1:j])
        text=text[:i]+UNUSED+text[j+1:]
    return (l, text)

def find_all_numbers(text:str):
    NUMBERS_REG = r"([^\w])+(\d+(\.\d*)?)"
    l=[]
    while (res:=re.search(NUMBERS_REG, text)):
        l.append(res.group(2))
        text=text[:res.start(2)]+UNUSED+text[res.end(2):]

    return (l, text)

def find_all_operators(text:str):
    REG = r'([\w+]+)\s*\(.*\)'
    print(re.findall(REG, text))