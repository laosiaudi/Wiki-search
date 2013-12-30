#
#coding:utf-8
import sys 
import networkx as nx
import matplotlib.pyplot as plt
import time
class MC_search():
    def __init__(self,sourceword, dest, datalist,outlist,inlist):
        self.ord_database = []
        self.inlinks = {}
        self.outlinks = {}
        self.step =1
        self.has_been = []
        self.graph = nx.Graph()
        self.path = []
        self.start = sourceword
        self.dest = dest
        for line in datalist:
            word_database = line[:-1].split(' ')
        for line in inlist:
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
            self.inlinks[keyword] = list
        for line in outlist:
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
            self.outlinks[keyword] = list



    def interlist(self,a,b):
        s = set(b)
        return len([item for item in a if item in s])

    def weight(self,a,b):
        if self.outlinks.has_key(a) and self.inlinks.has_key(b):
            lin =  self.interlist(self.outlinks[a],self.inlinks[b])
        else:
            lin = 0
        if self.inlinks.has_key(a) and self.outlinks.has_key(b):
            lout = self.interlist(self.inlinks[a],self.outlinks[b])
        else:
            lout = 0
        return lin+lout

    def select_num(self,d):
        if len(d)<=10 :
            return len(d)
        if len(d) <= 100 and len(d)>=10:
            return len(d)/10
        return 10


    def dfs(self,cur,depth,end,d):
        self.step += 1
        #print "hello"
        self.has_been.append(cur)
        if depth>d or self.step>50000 :
            return False
        if self.outlinks.has_key(cur) and end in self.outlinks[cur]:
            self.path.append(end)
            self.graph.add_node(end.decode('utf-8'))
            self.graph.add_edge(cur.decode('utf-8'),end.decode('utf-8'))
            self.has_been.append(end)
            return True
        if self.outlinks.has_key(cur)==False:
            return False
        dict = {}
        for link in self.outlinks[cur]:
            dict[link] = self.weight(link,end)
        sorted_dict = sorted(dict ,key = dict.get ,reverse = True)
        for w in range(0,self.select_num(sorted_dict)):
            if not sorted_dict[w] in self.path and not sorted_dict[w] in self.has_been :
                self.graph.add_node(sorted_dict[w].decode('utf-8'))
                self.graph.add_edge(sorted_dict[w].decode('utf-8'),cur.decode('utf-8'))
                self.path.append(sorted_dict[w])
                if self.dfs(sorted_dict[w],depth+1,end,d) == True:
                    return True
                self.path.remove(sorted_dict[w])
        return False

    def Search(self):
        self.path = []
        self.has_been = []
        self.path.append(self.start)
        self.step = 1
        self.graph.add_node(self.start.decode('utf-8'))
        t = time.clock()
       
        if self.dfs(self.start,0,self.dest,15) ==True:
            t = time.clock()-t
            path_str = ""
            for i in range(0,len(self.path)):
                if i == 0:
                    path_str += self.path[i]
                else:
                    path_str += "->"+self.path[i]
            self.Draw()    
            return (path_str,self.step,t,self.graph)
        else:
            return (None, None, None, None)

    def Draw(self):
        color = {}
        for item in self.has_been:
            if   item in self.path:
                color[item.decode('utf-8')] = 'green'
            else:
                color[item.decode('utf-8')] = 'red'
        values = [color.get(node,'red') for node in self.graph.nodes() ]
        if len(self.has_been) > 500:
            nx.draw_networkx(self.graph,font_family = 'SimHei',node_size=50,node_color=values, font_size = 5)
        else:
            nx.draw_networkx(self.graph,font_family = 'SimHei',node_size=1000,node_color=values, font_size = 10)
        plt.savefig('Mo_Search.png')
        plt.close()



#if __name__ =="__main__":
#    load_data()
    #input
#    start = raw_input("please input start point: ").decode('utf-8')
#    end = raw_input("please input end point: ").decode('utf-8')
    #random
    #datafile = open('testcase.txt','r')
    #line = datafile.readline().split(' ')
    #start = line[0].decode('utf-8')
    #end = line[1][:-1].decode('utf-8')
    
#    if not start in word_database or not end in word_database:
#        print "words not found"
#        sys.exit()
#    print "searching......."
#    G = nx.Graph()
#    G.add_node(start)
    
#    test.path.append(start)
    #print weight(start,end)
#    if dfs(start,0,end,10) ==True:
#        for link in test.path :
#            print link,
#    else:
#        print "path not found"
#    print test.step
    #pos =nx.random_layout(G)
#    tree = nx.tree(G,test.path[0])
#    nx.draw(tree)
    #nx.draw(G,node_size =1000)
#    plt.show()


