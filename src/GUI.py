#!/usr/bin/python
#-*-coding:utf-8-*-
from Tkinter import *
from PageRank import *
from heuristic_search import *
from breadth import *
import os
from mountainclimb_search import *
from Heuristic_Bidirection import *

import tkMessageBox
import Image
class App:
    def __init__(self, master):
        # try:
        #     os.system('rm *.png')
        # except:
        #     pass
        self.index = 0
        DataTxt = file('data.txt','r')
        Outlink  = file('outlinks.txt','r')
        Inlink = file('inlinks.txt','r')
        self.DataLines = DataTxt.readlines()
        self.OutLines = Outlink.readlines()
        self.InLines = Inlink.readlines()

        DataTxt.close()
        Outlink.close()
        Inlink.close()

        frame_1 = Frame(master, height = 50, width = 450)
        frame_1.pack(side = TOP)

        frame_2 = Frame(master, height = 450, width = 450)
        frame_2.pack(side = TOP)

        self.OptionBox = Listbox(frame_1, selectmode = SINGLE, height = '10'
                , width = '12', selectbackground = 'green')
        self.OptionBox.insert(1, '启发式迭代深度搜索')
        self.OptionBox.insert(2, '双向广度搜索')
        self.OptionBox.insert(3, '启发式搜索')
        self.OptionBox.insert(4, '双向启发式搜索')
        self.OptionBox.pack(side = LEFT)
        


        self.button = Button(frame_1, text = "Quit", command = frame_1.quit, activebackground = 'red', width = '10',height =
                '5')
        self.button.pack(side = LEFT)

        self.Find = Button(frame_1, text = "Searching", command = self.Search,
                activebackground = 'green', width = '10', height = '5')
        self.Find.pack(side = LEFT)

        self.Show = Button(frame_1, text = 'ShowGraph', command = self.ShowGraph,
                activebackground = 'green', width = '10', height = '5')
        self.Show.pack(side = LEFT)
        

        L1 = Label(frame_2, text = 'Origin：')
        L1.pack(side = LEFT)
        self.Source = Entry(frame_2, bd = 5)
        self.Source.pack(side = LEFT)


        L2 = Label(frame_2, text = "Destination：")
        L2.pack(side = LEFT)
        self.Destination = Entry(frame_2, bd = 5)
        self.Destination.pack(side = LEFT)
        
        self.TextContent = Text(frame_2, height = '20', width = '450')
        self.TextContent.pack(side = LEFT)
        self.TextContent.delete('1.0', '40.0')

    def Search(self):
        try:
            Str1 = self.Source.get().encode('utf8')
            Str2 = self.Destination.get().encode('utf8')
        except:
            tkMessageBox.showinfo('Error', '请输入完整的查询条件')

        if Str1 == '' or Str2 == '':
            tkMessageBox.showinfo('Error', '请输入完整的查询条件')
            return 
        try:
            Number = self.OptionBox.curselection()[0]
            if Number == '1':
                try:
                    Bi_Search = BidirectionSearch(Str1, Str2, self.DataLines,self.OutLines, self.InLines)
                    self.Bi_PATH, self.Bi_Node, self.Bi_Time, self.Bi_Graph= Bi_Search.Search()

                    Str_Bi_Node = str(self.Bi_Node)
                    Str_Bi_Time = str(self.Bi_Time)

                    self.TextContent.insert(END,'双向搜索的路径为：\n')
                    self.TextContent.insert(END, self.Bi_PATH + '\n')
                    self.TextContent.insert(END,'所用时间为: ' + Str_Bi_Time +
                     ' 搜索过得节点数为: ' + Str_Bi_Node  + '\n\n')

                except:
                    tkMessageBox.showinfo('Error', '双向搜索失败')
                     
            elif Number == '2':
                try:
                    He_Search = HeuSearch(Str1, Str2, self.DataLines, self.OutLines,self.InLines)
                    self.He_Path, self.He_Node ,self.He_Time, self.He_Graph= He_Search.Search()
                    Str_He_Node = str(self.He_Node)
                    Str_He_Time = str(self.He_Time)
                    self.TextContent.insert(END,'启发式搜索的路径为：\n')
                    self.TextContent.insert(END, self.He_Path + '\n')
                    self.TextContent.insert(END,'所用时间为: ' + Str_He_Time +
                        '搜索过得节点数为: ' + Str_He_Node + '\n\n')

                except:
                    tkMessageBox.showinfo('Error', '启发式搜索失败')

                
            elif Number == '0':
                try:
                    Mc_Search = MC_search(Str1, Str2, self.DataLines, self.OutLines,self.InLines)
                    self.Mc_Path, self.Mc_Node, self.Mc_Time, self.Mc_Graph = Mc_Search.Search()
                    Str_Mc_Node = str(self.Mc_Node)
                    Str_Mc_Time = str(self.Mc_Time)
                    self.TextContent.insert(END,'爬山式搜索的路径为：\n')
                    self.TextContent.insert(END, self.Mc_Path+ '\n')
                    self.TextContent.insert(END,'所用时间为: ' + Str_Mc_Time +
                            ' 搜索过得节点数为: ' + Str_Mc_Node + '\n\n')

                except:
                    tkMessageBox.showinfo('Error', '爬山法搜索失败')
            elif Number == '3':
                try:
                    He_BiSearch = Heuristic_Bidirection(Str1, Str2, self.DataLines, self.OutLines, self.InLines)
                    self.HeBi_path, self.HeBi_Node, self.HeBi_Time, self.HeBi_Graph = He_BiSearch.Search()
                    Str_HeBi_Node = str(self.HeBi_Node)
                    Str_HeBi_Time = str(self.HeBi_Time)
                    self.TextContent.insert(END,'双向启发式的路径为：\n')
                    self.TextContent.insert(END, self.HeBi_path + '\n')
                    self.TextContent.insert(END,'所用时间为: ' + Str_HeBi_Time+
                        '  搜索过得节点数为: ' + Str_HeBi_Node+ '\n\n')

                except:
                    tkMessageBox.showinfo('Error', '双向启发式搜索失败')

        except:
            tkMessageBox.showinfo('Error', '请选择搜索类型')

        
    def ShowGraph(self):
        try:
            Number = self.OptionBox.curselection()[0]
            if Number == '1':
                try:
                    Bi_Image = Image.open('BiSearch.png')
                    Bi_Image.show()
                except:
                    tkMessageBox.showinfo('Error', '该图不存在')


            elif Number == '0':
                try:
                    Mc_Image = Image.open('Mo_Search.png') 
                    Mc_Image.show()
                except:
                    tkMessageBox.showinfo('Error', '该图不存在')

                
            elif Number == '2':
                try:
                    He_Image = Image.open('HSearch.png')
                    He_Image.show()
                except:
                    tkMessageBox.showinfo('Error', '该图不存在')
            elif Number == '3':
                try:
                    HeBi_Image = Image.open('HeBiSearch.png')
                    HeBi_Image.show()
                except:
                    tkMessageBox.showinfo('Error', '该图不存在')

        except:
            tkMessageBox.showinfo('Error', '请选择要显示图的搜索类型')

if __name__ == '__main__' :
    root = Tk()
    root.title('WiKi_Link_Search')
    root.geometry('800x500+550+550')
    app = App(root)
    root.mainloop()


