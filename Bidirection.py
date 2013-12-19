#!/usr/bin/python
#-*-coding:utf-8-*-
import Queue
import random
from sets import Set

DataTxt = file('data.txt','r')
Outlink  = file('outlinks.txt','r')
Inlink = file('inlinks.txt','r')
DataLines = DataTxt.readlines()
OutLines = Outlink.readlines()
InLines = Inlink.readlines()
Data_Dictionary = {}
Outlink_Dictionary = {}
Inlink_Dictionary = {}
List = []        
    
for line in DataLines: 
    List = line.split(' ')
    List[-1] = List[-1][:-1]
    Data_Dictionary[List[0]] = List[1:]

for line in OutLines:
    List = line.split(' ')
    List[-1] = List[-1][:-1]
    Outlink_Dictionary[List[0]] = List[1:]

for line in InLines:
    List = line.split(' ')
    List[-1] = List[-1][:-1]
    Inlink_Dictionary[List[0]] = List[1:]

while (True):
    Origin= raw_input('The Origin: ')
    Destination = raw_input('The Destination: ')
    Flag = False

    FrontDictionary = {}
    BackDictionary = {}
    FrontSet = Set()
    BackSet = Set()
    
    #A queue consists of tuples(title, number of outlinks, path)
    queue_front = []
    queue_front.append((Origin, Data_Dictionary[Origin][1],
        Origin))

    #A set stroes the front node
    FrontSet.add(Origin)
    
   
    #A queue consists of tuples(title, number of inlinks, path)
    queue_back = []
    queue_back.append((Destination,
        Data_Dictionary[Destination][0], Destination))
    #A set stores the back node
    BackSet.add(Destination)
    
    Node_Count = 1
    
    while len(queue_front) != 0 and len(queue_back) != 0:
        FrontNode = queue_front.pop(0)
    
        Out_of_front = Outlink_Dictionary[FrontNode[0]]
        for item in Out_of_front:
            OutValue = Data_Dictionary[item][1]
            FrontDictionary[item] = OutValue
    
        SortedByValue = sorted(FrontDictionary.iteritems(), key = lambda d:d[1], reverse = True)

        FrontDictionary.clear()
        Shortest_Path_Length = 0
        Shortest_Path = ''

        for i in SortedByValue:
            if i[0] not in FrontSet:
                FrontTuple = (i[0], i[1], FrontNode[2] + '->' + i[0])
                queue_front.append(FrontTuple)
                Node_Count += 1
                FrontSet.add(i[0])
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

            print 'The node count is %d' %Node_Count
            print Shortest_Path

        if Flag:
            break

        BackNode = queue_back.pop(0)
    
        In_of_back = Inlink_Dictionary[BackNode[0]]
        for item in In_of_back:
            Invalue = Data_Dictionary[item][0]
            BackDictionary[item] = Invalue
    
        SortedByValue = sorted(BackDictionary.iteritems(), key = lambda d:d[1], reverse = True)
        BackDictionary.clear()
    
        for i in SortedByValue:
            if i[0] not in BackSet:
                BackTuple = (i[0], i[1], i[0] + '->' + BackNode[2])
                queue_back.append(BackTuple)
                Node_Count += 1
                BackSet.add(i[0])

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

            print 'The node count is %d' %Node_Count
            print Shortest_Path

        if Flag:
            break
    

    if Flag == False:
        print 'Not Found!\n'


