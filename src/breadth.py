#!/usr/bin/python
#-*-coding:utf-8-*-
from sets import Set
import Queue
import time
from Class import *
import networkx as nx
import matplotlib.pyplot as plt
global links
global keyset
class breadthSearch():
	def __init__(self,Begin,Destination,data,outlink,inlink):
		global links
		global keyset
		links = {}
		keyset = set()
		for line in outlink:
			component = line.split(' ')
			keyword = component[0]
			lists = []
			for item in component:
				if item[-1] == '\n':
					item = item[:-1]
				if item == component[0]:
					continue
				else:
					lists.append(item)
			keyset.add(keyword)
			links[keyword] = lists
		self.begin = Begin
		self.dest = Destination
	
	def Search(self):
		global links
		global keyset
		if not self.begin in keyset or not self.dest in keyset:
			return ("",0,0,False,nx.Graph())
		else:
			WordSet = Set()
			List = []
			q = []
			start = time.clock()
			BeginTerm = term(self.begin,self.begin)
			WordSet.add(self.begin)
			List.append(BeginTerm)
			Flag = False
			cou = 0

			while List.count != 0:
				cou = cou + 1
				if not List:
					break

				terms = List.pop(0)
				q.append(terms)
				p = terms.title
				if p not in keyset:
					continue
				Termlinks = links[p]
				if p == self.dest:
					Flag = True
					etime = time.clock() - start
					return (terms.path,cou,etime,Flag,self.drawgraph(result_path,q))
					break

				if self.dest in Termlinks:
					result_path = terms.path + '->' + self.dest
					Flag = True
					etime = time.clock() - start
					return (result_path,cou,etime,Flag,self.drawgraph(result_path,q))
					break
			
				for link in Termlinks:
					if link not in WordSet:
						Path = terms.path + '->' + link
						NewTerm = term(link,Path)
						List.append(NewTerm)
						WordSet.add(link)
		
			if Flag == False:
				result_path = ""
				cou = 0
				return (result_path,cou,0,Flag,nx.Graph())
	
	def drawgraph(self,path,nodelist):
		color = {}
		graph = nx.Graph()
		for item in nodelist:
			graph.add_node(item.title)
			if item.title in path.split('->'):
				color[item.title] = 'green'

		for item in nodelist:
			if item.path == '':
				continue
			s = item.path.split('->')
			for i in range(0,len(s) - 1):
				if i == 0:
					continue
				graph.add_edge(s[i],s[i+1])
		values = [color.get(node,'red') for node in graph.nodes()]
		pos = nx.spring_layout(graph)
		if len(nodelist) > 500:
			nx.draw_networdx(graph,node_size=50,node_color=values,font_size = 5)
		else:
			nx.draw_networkx(graph,node_size=1000,node_color=values,font_size = 10)
		
		plt.savefig('breadthSearch.png')
		plt.close()
		return None

if __name__ == '__main__':
	source = "微软"
	dest = "苹果"
	bsearch = breadthSearch(source,dest,[],[],[])
	path,num,etime,graph = bsearch.search()
	plt.show(graph)
