import os
import re
import codecs
from typing import Dict, Union, List, Any

def using(items: List[str]) -> Dict[Any, int]:
    if not items:
        return {}
    res = {}
    for item in items:
        res[item] = res.get(item, 0) + 1
    return res

def find_literals(text: List[str]) -> Dict[Union[str, int, float, bool], int]:
    STR_LITERAL_REGEX = r'(StringLiteral([0-9:<>a-z\s\'\[\]]+)(\"(?P<constant>.+)\"))|((?P<type_number>(\w)+)Literal(Expr)*([0-9:<>a-z\s\'\[\]]+)\s((?P<constant_number>([0-9\.(e\+)]+)|(false|true))))'
    ans = []
    for line in text:
        res = re.search(STR_LITERAL_REGEX, line)
        if res:
            s = res.group("constant")
            i = res.group("constant_number")
            if i: 
                match (res.group("type_number")):
                    case "Integer":
                        ans.append(int(i))
                    case "Floating":
                        ans.append(float(i))
                    case "CXXBool":
                        ans.append(i)
                    case _:
                        ans.append(i)
            if s:
                b2 = codecs.escape_decode(s)[0]
                ans.append(b2.decode("utf8"))

    return using(ans)

def find_operators(text: List[str]) -> Dict[str, int]:
    OPERATOR_REG = r'\b(?!Decl|Compound)(?P<operator>\w*)Stmt\b'
    ans = []
    for line in text:
        res = re.search(OPERATOR_REG, line)
        if res:
            op = res.group("operator").lower()
            ans.append(op)
    return using(ans)

def find_operands(text: List[str]) -> Dict[str, int]:
    OPER_REG = r"DeclRefExpr(.)+Var\s'(?P<name>\w+)'"
    ans = []
    for line in text:
        res = re.search(OPER_REG, line)
        if res:
            ans.append(res.group("name"))
    
    return using(ans)

def find_call_funcs(text: List[str]) -> Dict[str, int]:
    REG = r"DeclRefExpr(.+)lvalue\s(Function|CXXMethod)\s'(?P<name>[\w<>+-]+)'"
    ans = []
    for line in text:
        res = re.search(REG, line)
        if res:
            ans.append(res.group("name"))
    return using(ans)

def find_all_operators(text: List[str]) -> Dict[str, int]:
    REG = r"(BinaryOperator\s(.)+\s('bool')\s'(?P<bin_operator>.+)')|(UnaryOperator\s(.+)fix\s'(?P<un_operator>.+)')|(CompoundAssignOperator(.+)lvalue\s'(?P<name>.+)'\sComputeLHST)"
    ans = []
    for line in text:
        res = re.search(REG, line)
        if res:
            i = res.group('un_operator')
            s = res.group('bin_operator')
            f = res.group('name')
            if i: ans.append(i)
            if s: ans.append(s)
            if f: ans.append(f)
    
    return using(ans)

def str_without_single_comment(s: str):
    single = r'(//([.]*))\s*(\n)*'
    return re.split(single, s)[0]

def text_without_single(text: List):
    return list(map(str_without_single_comment, text))

def text_without_comments(text: str):
    i = -1
    while (i:=text.find('/*'))!=-1:
        j = text.find('*/')
        text = text[:i]+text[j+2:]
    return text

def count_signs(filename):
    text = None
    with open(f"{filename}", 'r') as f:
        text = text_without_single(f.readlines())
        text = ''.join(text)
    text = text_without_comments(text)
    ans = re.findall(r'(?P<operator>[,;\[\{\]\}])', text)
    return using(ans)

filename='test.cpp'
os.system("clang++ -Xclang -ast-dump -fsyntax-only test.cpp > parse_res.txt")
# filename='csc.cpp'
# os.system("clang++ -Xclang -ast-dump -fsyntax-only /Users/vvelikovich/Downloads/csc.cpp > parse_res.txt")

text = None

with open("parse_res.txt","r") as f:
    text = f.readlines()

i=0
while (i<len(text) and text[i].find(f'{filename}')==-1):
    i+=1

if i!=len(text):
    text = text[i:]

for i, line in enumerate(text):
    text[i] = re.sub(r'(\[[0-9;]+m)|(\s0x([0-9a-z]{9}))', "" ,line.replace('', ""))
    
with open("parse_res_clear.txt","w") as f:
    print(*text, sep='', file=f)

print(find_literals(text))
print(find_operators(text))
print(find_operands(text))
print(find_call_funcs(text))
print(find_all_operators(text))
print(count_signs(filename))
