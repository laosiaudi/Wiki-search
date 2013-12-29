#-*- coding:utf-8 -*-
# AUTHOR:   apple
# FILE:     main.py
# 2013 @laosiaudi All rights reserved
# CREATED:  2013-12-26 14:22:30
# MODIFIED: 2013-12-29 13:55:26

import os
import tornado.ioloop
import tornado.web
import pymongo
import tornado.httpserver
import json
import time
import random
from heuristic_search import *
from breadth import *
from Heuristic_Bidirection import *
from PageRank import *
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        vac = []
        num = len(datalines)
        for i in range(50):
            rnum = random.randint(0,num)
            vac.append(datalines[rnum].split(' ')[0])
        self.render('main.html',vac = vac)

class SearchHandler(tornado.web.RequestHandler):
    def post(self):
        source = self.get_argument("source",'')
        dest = self.get_argument("dest",'')
        sway = self.get_argument("sway",'')
        sway = sway.encode('utf-8')
        if sway == '1':
            try:
                bisearch = BidirectionSearch(source.encode('utf-8'),dest.encode('utf-8'),datalines,outlink,inlink)
                bipath,binode,bitime,bigraph = bisearch.Search()
                resultpath = '双向搜索路径为: ' + bipath
                resultnode = '双向搜索节点数为: ' + str(binode)
                resulttime = '双向搜索时间为: '+ str(bitime)
                resultimage = 'BiSearch.png'
                os.system('mv BiSearch.png ./static/')
                resultdiv = {"rp":resultpath,"rn":resultnode,"rt":resulttime,"ri":resultimage}
                rr =json.dumps(resultdiv)
                self.write(rr)
            except:
                self.write("<html><title>Wrong Page</title><body><h1>No such word!</h1>\
                        <a href='/'>再来一次<a>")
        if sway == '2':    
            try:
                hbisearch = Heuristic_Bidirection(source.encode('utf-8'),dest.encode('utf-8'),datalines,outlink,inlink)
                hbipath,hbinode,hbitime,hbigraph = hbisearch.Search()
                resultpath = '双向启发搜索路径为: ' + hbipath
                resultnode = '双向启发搜索节点数为: ' + str(hbinode)
                resulttime = '双向启发搜索时间为: '+ str(hbitime)
                resultimage = 'HeBiSearch.png'
                os.system('mv HeBiSearch.png ./static/')
                resultdiv = {"rp":resultpath,"rn":resultnode,"rt":resulttime,"ri":resultimage}
                rr =json.dumps(resultdiv)
                self.write(rr)
            except:
                self.write("<html><title>Wrong Page</title><body><h1>No such word!</h1>\
                        <a href='/'>再来一次<a>")
        if sway == '3':    
            try:
                hsearch = HeuSearch(source.encode('utf-8'),dest.encode('utf-8'),datalines,outlink,inlink)
                hpath,hnode,htime,hgraph = hsearch.Search()
                resultpath = '启发式搜索路径为: ' + hpath
                resultnode = '启发式搜索节点数为: ' + str(hnode)
                resulttime = '启发式搜索时间为: '+ str(htime)
                resultimage = 'HSearch.png'
                os.system('mv HSearch.png ./static/')
                resultdiv = {"rp":resultpath,"rn":resultnode,"rt":resulttime,"ri":resultimage}
                rr =json.dumps(resultdiv)
                self.write(rr)
            except:
                self.write("<html><title>Wrong Page</title><body><h1>No such word!</h1>\
                        <a href='/'>再来一次<a>")

        #f sway == '4':    
        #   try:
        #       msearch = Heuristic_Bidirection(source.encode('utf-8'),dest.encode('utf-8'),datalines,outlink,inlink)
        #       hbipath,hbinode,hbitime,hbigraph = hbisearch.Search()
        #   except:
        #       self.write("<html><title>Wrong Page</title><body><h1>No such word!</h1>\
        #               <a href='/'>再来一次<a>")
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/",MainHandler),
        (r"/search",SearchHandler)
        ]
        settings = {"static_path":os.path.join(os.path.dirname(__file__),"static"),
                "template_path":os.path.join(os.path.dirname(__file__),"templates"),
                "debug":True,
        }
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
    datatext = open('data.txt','r')
    outlinktext = open('outlinks.txt','r')
    inlinktext = open('inlinks.txt','r')
    datalines = datatext.readlines()
    outlink = outlinktext.readlines()
    inlink = inlinktext.readlines()
    HTTPSERVER = tornado.httpserver.HTTPServer(Application())
    HTTPSERVER.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


