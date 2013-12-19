#!/usr/bin/python
#-*-coding:utf-8-*-
import Queue
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from sets import Set
class BidirectionSearch:
    def __init__(self, Source, Destination, Datalines, Outlines, Inlines):
        self.start = time.clock()
        self.Origin= Source
        self.Destination = Destination

        self.Datalines = Datalines
        self.Outlines = Outlines
        self.Inlines = Inlines

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


    '''搜索函数'''
    def Search(self):
        '''对文件建立索引'''
        Flag = False
         
        FrontDictionary = {}
        BackDictionary = {}
        FrontSet = Set()
        BackSet = Set()
        frontset = set()
        backset = set()
        '''一个由元组组成的队列，其中元组里面的值包括：网页标题，路径'''
        queue_front = []
        try:
            queue_front.append((self.Origin, self.Data_Dictionary[self.Origin][1],
                self.Origin))
        except:
            print '没有该词\n'
            return (None, None, None, None)

        '''一个记录正向已搜索节点的标题的集合'''

        FrontSet.add(self.Origin)
        frontset.add((self.Origin,self.Data_Dictionary[self.Origin][1],self.Origin))
        '''一个由元组组成的队列，其中元组里面的值包括：网页标题，路径'''
        queue_back = []

        try:
            queue_back.append((self.Destination,
                self.Data_Dictionary[self.Destination][0], self.Destination))
        except:
            print '没有该词\n'
            return (None, None, None, None)

        '''一个记录逆向已搜索节点的标题的集合'''
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

            FrontDictionary.clear()
            Shortest_Path_Length = 0
            Shortest_Path = ''

            '''将队列头元素的外链的所有节点都假如该队列中'''
            for i in SortedByValue:
                if i[0] not in FrontSet:
                    FrontTuple = (i[0], i[1], FrontNode[2] + '->' + i[0])
                    queue_front.append(FrontTuple)
                    Node_Count += 1
                    FrontSet.add(i[0])
                    frontset.add(FrontTuple)
            Label_front = 0

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
                    Full_Path = StrPath + '->' + PATH_Back
                    if Label_front == 0:
                        Shortest_Path_Length = len(Full_Path.split('->'))
                        Shortest_Path = Full_Path
                    else:
                        if len(Full_Path.split('->')) < Shortest_Path_Length:
                            Shortest_Path_Length = len(Full_Path.split('->'))
                            Shortest_Path = Full_Path

                    Label_front += 1

                '''等你来完善'''
                etime = time.clock() - self.start
                setcommon = backset | frontset
                return (Shortest_Path, Node_Count,etime,self.drawgraph(Shortest_Path,setcommon))

            if Flag:
                break

            BackNode = queue_back.pop(0)
            searchedlist.append(BackNode) 
            In_of_back = self.Inlink_Dictionary[BackNode[0]]
            for item in In_of_back:
                Invalue = self.Data_Dictionary[item][0]
                BackDictionary[item] = Invalue
    
            SortedByValue = sorted(BackDictionary.iteritems(), key = lambda d:d[1], reverse = True)
            BackDictionary.clear()
    
            '''将队列头元素的外链的所有节点都假如该队列中'''
            for i in SortedByValue:
                if i[0] not in BackSet:
                    BackTuple = (i[0], i[1], i[0] + '->' + BackNode[2])
                    queue_back.append(BackTuple)
                    Node_Count += 1
                    BackSet.add(i[0])
                    backset.add(BackTuple)
            Label_back = 0

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
                    Full_Path = StrPath + '->' + PATH_Back
                    if Label_back == 0:
                        Shortest_Path = Full_Path
                        Shortest_Path_Length = len(Full_Path.split('->'))
                    else:
                        if len(Full_Path.split('->')) < Shortest_Path_Length:
                            Shortest_Path_Length = Full_Path
                            Shortest_Path = Full_Path

                    Label_back += 1

                '''等你来完善'''
                etime = time.clock() - self.start
                setcommon = frontset | backset
                return (Shortest_Path, Node_Count,etime,self.drawgraph(Shortest_Path,setcommon))

            if Flag:
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
            nx.draw_networkx(graph,font_family='SimHei', node_size=50,node_color=values, font_size = 5)
        else:
            nx.draw_networkx(graph,font_family = 'SimHei', node_size=1000,node_color=values, font_size = 10)
        plt.savefig('BiSearch.png')
        plt.close()
        return None

if __name__ == '__main__':
    DataTxt = file('data.txt','r')
    Outlink  = file('outlinks.txt','r')
    Inlink = file('inlinks.txt','r')
    DataLines = DataTxt.readlines()
    OutLines = Outlink.readlines()
    InLines = Inlink.readlines()

    DataTxt.close()
    Outlink.close()
    Inlink.close()
    A = BidirectionSearch('麻省理工学院', '武汉大学计算机学院', DataLines, OutLines, InLines)
    a,b,c,d = A.Search()
    print a
    
