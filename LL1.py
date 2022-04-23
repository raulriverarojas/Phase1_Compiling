from email import header
import re
import numpy as np
from turtle import right
from collections import deque
from tabulate import tabulate
from anytree import Node, RenderTree
from anytree.exporter import JsonExporter
from graphviz import Source, render
import json


def computeFirsts(prod, terminals, nonterminals):
    firsts = {}
    empty = u'\u03B5'
    change = True
    for i in range(len(prod)):
        rightside = prod[i][1]
        if prod[i][0] not in firsts:
            firsts[prod[i][0]] = []
        
        rightprods = rightside.split()
        if rightprods[0] in terminals:
            firsts[prod[i][0]].append(rightprods[0])
        elif rightprods[0] == empty:
            firsts[prod[i][0]].append(empty)

    while(change):
        change = False
        for i in range(len(prod)):
            rightside = prod[i][1]
            
            rightprods = rightside.split()
            if rightprods[0] in nonterminals:
                for x in range(len(firsts[rightprods[0]])):
                    if firsts[rightprods[0]][x] not in firsts[prod[i][0]]:
                        firsts[prod[i][0]].append(firsts[rightprods[0]][x])
                        change = True
    return firsts


def removeEpsilon(lst):
    # empty=u'\u03B5'
    # temp=lst
    # if empty in temp:
    #     temp.remove(empty)
    # return temp
    return list(set(lst) - set([u'\u03B5']))


def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


def computeFollow(prod, firsts, terminals, nonterminals, start):
    follow = {}
    change = True
    empty = u'\u03B5'
    for k in range(len(nonterminals)):
        follow[nonterminals[k]] = []
    follow[start].append("$")
    # for i in range(len(prod)):
    #     rightside=prod[i][1].split("|")
    #     for l in range(len(rightside)):
    #         rightprods=rightside[l].split()
    #         for j in range(len(rightprods)):
    #             if rightprods[j] in nonterminals:
    #                 for h in range(len(rightprods)-j):
    #                     if rightprods[j+h] in terminals:
    #                         follow[rightprods[j]].append(rightprods[j+h])
    for i in range(len(prod)):
        rightside = prod[i][1]
        
        rightprods = rightside.split()
        for j in range(len(rightprods)):
            if rightprods[j] in nonterminals:
                for h in range(1, len(rightprods)-j):
                    if rightprods[j+h] in nonterminals and set(follow[rightprods[j]]) != set(removeEpsilon(firsts[rightprods[j+h]])):
                        follow[rightprods[j]
                                   ] += removeEpsilon(firsts[rightprods[j+h]])
                            # follow[rightprods[j]]=follow[rightprods[j]]
                    elif rightprods[j+h] in terminals and rightprods[j+h] not in follow[rightprods[j]]:
                        follow[rightprods[j]].append(rightprods[j+h])
    # while(change):
    #     change=False
    #     for i in range(len(prod)):
    #         rightside=prod[i][1].split("|")
    #         for l in range(len(rightside)):
    #             rightprods=rightside[l].split()
    #             for j in range(len(rightprods)):
    #                 if rightprods[j] in nonterminals:
    #                     follow[rightprods[j]]=Union(follow[rightprods[j]], removeEpsilon(follow[prod[i][0]]))
    #                     #Geeks for geeks line
    #                     for h in range(1,len(rightprods)-j):
    #                         if rightprods[j+h] in nonterminals and set(follow[rightprods[j]])!=set(removeEpsilon(firsts[rightprods[j+h]])):
    #                             if empty in firsts[rightprods[j+h]] and set(follow[rightprods[j]])!=set(follow[prod[i][0]]):
    #                                 #follow[rightprods[j]]+=follow[prod[i][0]]
    #                                 #follow[rightprods[j]]=list(set(follow[rightprods[j]]).update(set(follow[prod[i][0]])))
    #                                 follow[rightprods[j]]=Union(follow[rightprods[j]], follow[prod[i][0]])
    #                             #follow[rightprods[j]]+=removeEpsilon(firsts[rightprods[j+h]])
    #                             #follow[rightprods[j]]=list(set(follow[rightprods[j]]).update(set(removeEpsilon(firsts[rightprods[j+h]]))))
    #                             #make function to remove epsilon from firsts before addition
    #                             follow[rightprods[j]]=Union(follow[rightprods[j]], removeEpsilon(firsts[rightprods[j+h]]))
    #                             change=True

    while(change):
        change = False
        for i in range(len(prod)):
            rightside = prod[i][1]
            
            rightprods = rightside.split()
            for j in range(len(rightprods)):

                if rightprods[j] in nonterminals:
                        # if set(follow[rightprods[j]])!=set(follow[prod[i][0]]):
                        #     follow[rightprods[j]]=Union(follow[rightprods[j]], removeEpsilon(follow[prod[i][0]]))
                        #     change=True
                    if j+1 == len(rightprods) and set(follow[rightprods[j]]) != set(Union(follow[rightprods[j]], follow[prod[i][0]])):
                        follow[rightprods[j]] = Union(
                                follow[rightprods[j]], follow[prod[i][0]])
                            # Geeks for geeks line
                        change = True
                    for h in range(1, len(rightprods)-j):
                        if rightprods[j+h] in nonterminals and empty in firsts[rightprods[j+h]] and set(follow[rightprods[j]]) != set(Union(follow[rightprods[j]], follow[prod[i][0]])):
                            follow[rightprods[j]] = Union(
                                    follow[rightprods[j]], follow[prod[i][0]])
                            change = True
    return follow


def computeLL1Table(prod, terminals, nonterminals, firsts, follow):

    empty = u'\u03B5'
    prod[0][1] += " $"
    table = [[[] for u in range(len(terminals))]
             for o in range(len(nonterminals))]
    for i in range(len(prod)):
        rightside = prod[i][1]
        
        rightprods = rightside.split()
        for j in range(len(rightprods)):
            if rightprods[j] in nonterminals:
                for h in removeEpsilon(firsts[rightprods[j]]):
                    if h in terminals:
                        table[nonterminals.index(prod[i][0])][terminals.index(
                                    h)].append(rightside)
                if empty in firsts[rightprods[j]]:
                    for z in follow[prod[i][0]]:
                        table[nonterminals.index(prod[i][0])][terminals.index(
                                    z)].append(rightside)
                
                break
            elif rightprods[j] in terminals or rightprods[j]==empty:
                if rightprods[j]==empty:
                    for z in follow[prod[i][0]]:
                        table[nonterminals.index(prod[i][0])][terminals.index(
                                    z)].append(rightside)
                else:
                    table[nonterminals.index(prod[i][0])][terminals.index(
                                    rightprods[j])].append(rightside)
                break

        #printTable(terminals, nonterminals,table)

    return table
def printTable(terminals, nonterminals, table):
    print("Table:")
    print("\t", end="")
    for u in range(len(table)):
        print(terminals[u]+",\t\t", end='')
    print()
    for o in range(len(table)):
        print(nonterminals[o]+'\t', end="")
        for m in table[o]:
            print(m, end="")
            if(len(m)<=0):
                print("\t", end="")
            print("\t", end="")
        print()
def nodeName(node):
    last_name= node.name[node.name.rfind('/')-1:]
    return last_name

    return 
def parser(table, line, terminals, nonterminals, start, symbol_table):
    stack = deque()
    input=deque()
    empty = u'\u03B5'
    root=Node("S")
    
    for p in start.split()[::-1]:
        stack.append(Node(p, parent=root))
        #stack.append(p)
    # for i in range(len(lines)):
    tokens=line.split()
    t=0
    while(len(stack)>=1):
        #while(tokens[t]!=stack[len(stack)-1] and stack[len(stack)-1]!=empty):
        while(tokens[t]!=nodeName(stack[len(stack)-1]) and nodeName(stack[len(stack)-1])!=empty):
                # for j in tokens[t].split():
            popped=stack[len(stack)-1]
            #push=table[nonterminals.index(stack.pop())][symbol_table[tokens[t]]]
            push=table[nonterminals.index(nodeName(stack.pop()))][terminals.index(tokens[t])]
            #push=table[nonterminals.index(stack.pop())][terminals.index(tokens[t])]
            for j in push[0].split()[::-1]:
                stack.append(Node(j, parent=popped))
                #stack.append(j)
        #if (stack[len(stack)-1]!=empty):
        if (nodeName(stack[len(stack)-1])!=empty):
            if (tokens[t]!=nodeName(stack[len(stack)-1])):
                Node(tokens[t],parent=stack[len(stack)-1])
            stack.pop()
            t+=1
        else:
            if (nodeName(stack[len(stack)-1])!=empty):
                Node(tokens[t],parent=stack[len(stack)-1])
            stack.pop()
    return root
            



        








#f = open("decaf_grammar_left_rec_rem_ed2.txt", "r", encoding='utf-8')
#f = open("test_grammar_2.txt", "r", encoding='utf-8')
f = open("grammar.txt", "r", encoding='utf-8')

buffer = f.read()
lines = re.split(r"\n", buffer)  # Splits into lines
f.close()

prod = []
nonterminals = []
terminals = []
start = ""
# termChar=r"\b[a-z]+|\{|\}|\[|\]|\,|\.|\;|\(|\)|\=|\-|\!|\+|\*|\/|\<|\>|\%|\<\<|\>\>|\<\=|\>\=|\=\=|\!\=|\&\&|\|\|"
termChar = r"\b[a-z]+|\$|\{|\}|\[|\]|\,|\.|\;|\(|\)|\=|\-|\!|\+|\*|\/|\<|\>|\%|\<\<|\>\>|\<\=|\>\=|\=\=|\!\=|\&\&|\|\|"

for s in range(len(lines)):
    prodinter = lines[s].split("::=")
    prod.append([prodinter[0].strip(), prodinter[1]])
    if not prod[s][0] in nonterminals:
        nonterminals.append(prod[s][0].strip())
    terminals += re.findall(termChar, prod[s][1])
start = prod[0][0]
terminals.insert(0, "$")

print("Prod:\t")
print(prod)
print("terminals:\t")
print(terminals)
print("nonterminals:\t")
print(nonterminals)


firsts = computeFirsts(prod, terminals, nonterminals)

print("Firsts:")
print(firsts)
follow = computeFollow(prod, firsts, terminals, nonterminals, start)
print("Follow")
print(follow)
table = computeLL1Table(prod, terminals, nonterminals, firsts, follow)
#printTable(terminals, nonterminals,table)
print("Table: ")
with open("table.txt", "a", encoding='utf-8') as o:
    o.write(tabulate(table,headers=terminals, showindex=nonterminals))

# f = open("code.txt", "r", encoding='utf-8')

# buffer = f.read()
# input = re.split(r"\n", buffer)  # Splits into lines
with open('code.txt') as f:
    input= " ".join(line.strip() for line in f) 
f = open("symbol_table.txt", "r")
symbol_table={}
buffer = f.read()
symbol_lines = re.split(r"\n", buffer)  # Splits into lines
for m in range(len(symbol_lines)):
    
    tokens=symbol_lines[m].split()
    if tokens:
        symbol_table[tokens[0]]=tokens[len(tokens)-1]
f.close()
input="id + id $"
ast=parser(table,input,terminals,nonterminals,prod[0][1], symbol_table)
#if parsed: print("Parsing input: {} Successfull".format(input))
for pre, fill, node in RenderTree(ast):
    print("%s%s" % (pre, node.name))

exporter = JsonExporter(indent=2, sort_keys=True)
out_file = open("ast.json", "w")
# data=exporter.export(ast)
# json.dump(data, out_file, indent = 2)
  



exporter.write(ast, out_file)
out_file.close()

# DotExporter(ast).to_dotfile("ast.dot")
# Source.from_file('ast.dot')
# render('dot','png','ast.dot')




