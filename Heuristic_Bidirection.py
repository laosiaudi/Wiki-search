#!/usr/bin/python
#-*-coding:utf-8-*-
import Queue
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import time
from sets import Set
class Heuristic_Bidirection:
    def __init__(self, Source, Destination, Datalines, Outlines, Inlines):
        self.Origin= Source
        self.Destination = Destination

        self.Datalines = Datalines
        self.Outlines = Outlines
        self.Inlines = Inlines
        self.start = time.clock()

        self.Data_Dictionary = {}
        self.Outlink_Dictionary = {}
        self.Inlink_Dictionary = {}
        List = []        
            
        for line in self.Datalines: 
            List = line.split(' ')
            List[-1] = List[-1][:-1]
            self.Data_Dictionary[List[0]] = List[1:]
        
        for line in self.Outlines:
            List = line.split(' ')
            List[-1] = List[-1][:-1]
            self.Outlink_Dictionary[List[0]] = List[1:]
        
        for line in self.Inlines:
            List = line.split(' ')
            List[-1] = List[-1][:-1]
            self.Inlink_Dictionary[List[0]] = List[1:]

    def Search(self):
        Flag = False

        FrontDictionary = {}
        BackDictionary = {}
        FrontSet = Set()
        BackSet = Set()
        frontset = set()
        backset = set()
        
        '''A queue consists of tuples(title, number of outlinks, path)'''
        queue_front = []
        try:
            queue_front.append((self.Origin,
                self.Data_Dictionary[self.Origin][1], self.Origin))
        except:
            print '没有该词\n'
            return (None, None, None, None)
            

        '''A set stroes the front node'''

        FrontSet.add(self.Origin)
        frontset.add((self.Origin,self.Data_Dictionary[self.Origin][1],self.Origin))
        
        
        '''A queue consists of tuples(title, number of inlinks, path)'''
        queue_back = []
        try:
            queue_back.append((self.Destination,
                self.Data_Dictionary[self.Destination][0], self.Destination))
        except:
            print '没有该词\n'
            return (None, None, None, None)

        '''A set stores the back node'''
        BackSet.add(self.Destination)
        backset.add((self.Destination,self.Data_Dictionary[self.Destination][1],self.Destination))
        
        Node_Count = 1
        searchedlist = []     
        
        while len(queue_front) != 0 and len(queue_back) != 0:
            FrontNode = queue_front.pop(0)
            searchedlist.append(FrontNode) 
        
            Out_of_front = self.Outlink_Dictionary[FrontNode[0]]
            for item in Out_of_front:
                OutValue = self.Data_Dictionary[item][1]
                FrontDictionary[item] = OutValue
        
            
            SortedByValue = sorted(FrontDictionary.iteritems(), key = lambda d:d[1], reverse = True)
            Length_1 = int(math.ceil(len(SortedByValue) / 2))
            FrontDictionary.clear()

            for i in range(Length_1):
                front_item = SortedByValue[i]
                if front_item[0] not in FrontSet:
                    FrontTuple = (front_item[0], front_item[1], FrontNode[2] +
                            '->' + front_item[0])
                    queue_front.append(FrontTuple)
                    Node_Count += 1
                    FrontSet.add(front_item[0])
                    frontset.add(FrontTuple)
                    

            if len(BackSet & FrontSet) != 0:
                Flag = True
                for temp in (BackSet & FrontSet):
                    for i in queue_front:
                        if i[0] == temp:
                            PATH_Front = i[2]
                            break
                    for i in queue_back:
                        if i[0] == temp:
                            PATH_Back = i[2]
                            break
                
                    StrPath = PATH_Front.split('->')
                    StrPath = StrPath[:-1]
                    StrPath = '->'.join(StrPath)
                    Finally_Path = StrPath  + '->' + PATH_Back

                    etime = time.clock() - self.start
                    setcommon = backset | frontset
                    return(Finally_Path, Node_Count, etime,
                            self.drawgraph(Finally_Path, setcommon))
        
            BackNode = queue_back.pop(0)
            searchedlist.append(BackNode) 
        
            In_of_back = self.Inlink_Dictionary[BackNode[0]]
            for item in In_of_back:
                Invalue = self.Data_Dictionary[item][0]
                BackDictionary[item] = Invalue
        
            SortedByValue = sorted(BackDictionary.iteritems(), key = lambda d:d[1], reverse = True)
            BackDictionary.clear()
            Length_2 = int(math.ceil(len(SortedByValue) / 2))
        
            for i in range(Length_2):
                back_item = SortedByValue[i]
                if back_item[0] not in BackSet:

                    BackTuple = (back_item[0], back_item[1], back_item[0] + '->' + BackNode[2])
                    queue_back.append(BackTuple)
                    Node_Count += 1
                    BackSet.add(back_item[0])
                    backset.add(BackTuple)
                    
        
            if len(BackSet & FrontSet) != 0:
                for temp in (BackSet & FrontSet):
                    for i in queue_front:
                        if i[0] == temp:
                            PATH_Front = i[2]
                            break
                    for i in queue_back:
                        if i[0] == temp:
                            PATH_Back = i[2]
                            break
                    StrPath = PATH_Front.split('->')
                    StrPath = StrPath[:-1]
                    StrPath = '->'.join(StrPath)
                    etime = time.clock() - self.start
                    Finally_Path = StrPath  + '->' + PATH_Back
                    setcommon = backset | frontset
                    return(Finally_Path, Node_Count, etime,
                            self.drawgraph(Finally_Path, setcommon))
                    break
        if Flag == False:
            return (None,None,None,None)

    def drawgraph(self,path,nodeset):
        color = {}

        graph = nx.Graph()
        nodelist = list(nodeset)
        for item in nodelist:
            graph.add_node(item[0].decode('utf-8'))
            if item[0] in path.split('->'):
                color[item[0].decode('utf-8')] = 'green'

        for item in nodelist:
            if item[2] == '':
                continue
            s = item[2].split('->')
            for i in range(0,len(s) - 1):
                graph.add_edge(s[i].decode('utf-8'),s[i+1].decode('utf-8'))

        values = [color.get(node,'red') for node in graph.nodes()]
        pos = nx.spring_layout(graph)

        if len(nodelist) > 500:
            nx.draw_networkx(graph, font_family = 'SimHei',node_size=50,node_color=values, font_size = 5)
        else:
            nx.draw_networkx(graph,font_family = 'SimHei', node_size=1000,node_color=values, font_size = 10)
        plt.savefig('HeBiSearch.png')
        plt.close()
        return None


