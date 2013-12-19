#-*- coding:utf-8 -*-
# AUTHOR:   apple
# FILE:     search.py
# 2013 @laosiaudi All rights reserved
# CREATED:  2013-12-13 16:37:48
# MODIFIED: 2013-12-20 03:10:24
from __future__ import division
from collections import deque
import time
import math
import random
import networkx as nx
import matplotlib.pyplot as plt
class HeuSearch():
    def __init__(self, sourceword, dest, datalist, outlist, inlist):
        self.sourceword = sourceword
        self.dest = dest
        self.contentdata = datalist
        self.contentin = inlist
        self.contentout = outlist
        self.numofinlinks = {}
        self.numofoutlinks = {}
        self.visit = {}
        self.insert = {}
        self.links = {}
        self.linkss = {}
        self.cat = {}
        self.wordlist = []
        self.set2 = set()
        self.set4 = set()
        self.initialize()

    def initialize(self):
        """
        initialize,reading files including inlinks and outlinks,and categories
        """
        #file1 = open('data.txt','r')
        #content = file1.readlines()
        for line in self.contentdata:
            component = line[:-1].split(' ')
            self.visit[component[0]] = 0
            self.numofinlinks[component[0]] = int(component[1])
            self.numofoutlinks[component[0]] = int(component[2])
            self.wordlist.append(component[0])
            self.insert[component[0]] = 0
        #file1.close()
        #file2 = open('inlinks.txt','r')
        #content = file2.readlines()
        for line in self.contentin:
            component = line.split(' ')
            keyword = component[0]
            list = []
            for item in component:
                if item[-1] == '\n':
                    item = item[:-1]
                if item == component[0]:
                    continue
                else:
                    list.append(item)
            self.links[keyword] = list
        #file2.close()
        #file3 = open('outlinks.txt','r')
        #content = file3.readlines()
        for line in self.contentout:
            component = line.split(' ')
            keyword = component[0]
            list = []
            for item in component:
                if item[-1] == '\n':
                    item = item[:-1]
                if item == component[0]:
                    continue
                else:
                    list.append(item)
            self.linkss[keyword] = list

    def value(self,word):
       try:
           set1 = set(self.linkss[word])
           set3 = set1 & self.set2
           size = len(set3)
       except:
           size = 0
       try:
           set5 = set(self.links[word])
           size_ = len(set5&self.set4)
       except:
           size_ = 0
       if not self.numofinlinks.has_key(word):
           self.numofinlinks[word] = 0
       if not self.numofinlinks.has_key(self.dest):
           self.numofinlinks[self.dest] = 0
       if not self.numofoutlinks.has_key(word):
           self.numofoutlinks[word] = 0
       if not self.numofoutlinks.has_key(self.dest):
           self.numofoutlinks[word] = 0
       #return size/(self.numofoutlinks[word] + self.numofinlinks[self.dest] - size) + size_/(self.numofoutlinks[self.dest] + self.numofinlinks[word] -
       #        size_)
       return size + size_
    def Search(self):
        start = time.clock()
        self.insert[self.sourceword] = 1
        self.set2 = set(self.links[self.dest])
        self.set4 = set(self.linkss[self.dest])
        """搜索从这里开始---------------------------------------------------------------------"""
        source = node(self.sourceword, '', self.value(self.sourceword)) 
        temp = source
        queue= []
        queue.append(source)
        flag = False
        index = 0
        q = []
        while True:
            temp = queue.pop(0)
            q.append(temp) 
            #print temp.key
            if self.visit[temp.key] == 0:
                self.visit[temp.key] = 1
            else:
                continue
            if temp.key == '维基共享资源' or temp.key == '国际标准书号':
                continue
            index += 1
            if temp.key == self.dest:
                break;
            if not self.linkss.has_key(temp.key):
                continue
            """这里可以获得一个节点的出链---------------------------------------------------"""
            linklist = self.linkss[temp.key]
            for word in linklist:
                if word == self.dest:
                    temp = node(word, temp.path, self.value(word) )
                    q.append(temp)
                    flag = True
                    break
                if self.visit[word] == 0:
                    if self.insert[word] == 0:
                        subnode = node(word, temp.path, self.value(word))
                        queue.append(subnode)
                        self.insert[word] = 1
            if flag == True:
                break
            queue = sorted(queue, key=lambda item:item.keyvalue, reverse=True)
        etime = time.clock() -start 
        return (temp.path[2:], index, etime, self.drawgraph(temp.path,q))
    def drawgraph(self,path,nodelist):
        color = {}
        graph = nx.Graph()
        for item in nodelist:
            graph.add_node(item.key.decode('utf-8'))
            if item.key in path.split('->'):
                color[item.key.decode('utf-8')] = 'green'

        for item in nodelist:
            if item.path == '':
                continue
            s = item.path.split('->')
            for i in range(0,len(s) - 1):
                if i == 0:
                    continue
                graph.add_edge(s[i].decode('utf-8'),s[i+1].decode('utf-8'))
        values = [color.get(node,'red') for node in graph.nodes() ]
        pos = nx.spring_layout(graph)
        if len(nodelist) > 500:
            nx.draw_networkx(graph,font_family='SimHei', node_size=50,node_color=values, font_size = 5)
        else:
            nx.draw_networkx(graph,font_family='SimHei', node_size=1000,node_color=values, font_size = 10)
        plt.savefig('HSearch.png')
        plt.close()
        return None

            

"""
node 为每个节点的类，其中key为关键词，path为当前路径，keyvalue为估价值
"""
class node():
    def __init__(self, key, path,keyvalue):
        self.key = key
        self.path = path + '->' + key
        self.keyvalue = keyvalue

if __name__ == '__main__':
    source = raw_input('source is: \n')
    dest = raw_input('dest is :\n')
    print source
    print dest
    #try:
    hsearch = HeuSearch(source,dest)
    path,num,etime,graph = hsearch.search()
    print path + '   ' + str(num) + ' nodes ' + '  use ' + str(etime) + 's'

