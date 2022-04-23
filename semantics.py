from anytree.importer import JsonImporter
from anytree import RenderTree, Node, AsciiStyle, PreOrderIter

import re


# def idSymbolTable(lines, ids, scopes):
#     id_table=[[]]
#     scope=0
#     for i in range(len(lines)):
#         line=lines[i].split()
#         for k in range(len(line)):
            

importer = JsonImporter()
in_file = open("ast.json", "r")
ast=importer.read(in_file)
# ast=json.load(in_file)
in_file.close()
with open('code.txt') as f:
    input= " ".join(line.strip() for line in f) 

for pre, fill, node in RenderTree(ast):
    print("%s%s" % (pre, node.name))
f = open("symbol_table.txt", "r")
symbol_table={}
buffer = f.read()
symbol_lines = re.split(r"\n", buffer)  # Splits into lines
for m in range(len(symbol_lines)):
    tokens=symbol_lines[m].split()
    if tokens and not symbol_table[tokens[0]]:
        symbol_table[tokens[0]]=[(tokens[2],tokens[len(tokens)-1])]#overwrites repeated values
    elif tokens and symbol_table[tokens[0]]:
        symbol_table[tokens[0]].append((tokens[2],tokens[len(tokens)-1]))
f.close()



def search_scope(id,scope_list):
    found=False
    for i in range(len(scope_list)):
        for k in range(len(scope_list[i])):
            if id in scope_list[i]:
                return True
    return found
def parse(input, ast):
    
    return
def nodeName(node):
    last_name= node.name[node.name.rfind('/')-1:]
    return last_name
def typecheck(line,ast, symbol_table):
    scope_table=[]
    scope=0
    tokens=line.split()
    ast_post=[node.name for node in PreOrderIter(ast)]
    # for i in range(len(tokens)):
    for i in range(len(ast_post)):

            

    return scope_table
