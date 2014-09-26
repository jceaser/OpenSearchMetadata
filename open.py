from sys import stdin
from xml.dom import minidom
from Tkinter import *

#import tkFileDialog


class GUI(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid()
        self.ui = dict()
    
    def callback_go(self, tmp):
        entry = self.ui[tmp]["searchTerms"]
        template = self.ui[tmp]["template"]
        type = self.ui[tmp]["type"]
        url = template
        url = url.replace("{searchTerms}", str(self.ui[tmp]["searchTerms"].get()))
        url = url.replace("{count?}", str(self.ui[tmp]["count"].get()))
        url = url.replace("{startPage?}", str(self.ui[tmp]["startPage"].get()))
        url = url.replace("{geo:box?}", str(self.ui[tmp]["geoBox"].get()))
        url = url.replace("{time:start?}", str(self.ui[tmp]["timeStart"].get()))
        url = url.replace("{time:end?}", str(self.ui[tmp]["timeEnd"].get()))
        #print "before: %s\nafter: %s" % (template, url)
        print "%s %s" % (type, url)
        exit()
    
    def process(self):
        r=0
        w = Label(self, text="Options")
        
        xmldoc = minidom.parse("/tmp/osd.xml")
        urls = xmldoc.getElementsByTagName("Url")
        
        key = 0;
        ui= {}
        
        for u in urls:
            template = u.getAttribute("template")
            type = u.getAttribute("type")
            ul = Label(self, text=u.getAttribute("type"))
            ul.grid(row=r,column=0,columnspan=4)
            r += 1
            
            self.ui[key] = dict()
            
            params = u.getElementsByTagName("parameters:Parameter")
            for p in params:
                msg = required = repeat = minInclude = maxInclude = ""
                
                min = p.getAttribute("minimum")
                max = p.getAttribute("maximum")
                
                minInclude = p.getAttribute("minInclusive")
                maxInclude = p.getAttribute("maxInclusive")
                
                ####################
                # parameter label
                name = p.getAttribute("name")
                w = Label(self, text=name)
                w.grid(column=0, row=r)
                
                #print "adding '%s' of '%d'" % (name, key)
                
                ####################
                # input box
                self.ui[key]["template"] = template
                self.ui[key]["type"] = type

                if minInclude.isdigit() and maxInclude.isdigit():
                    self.ui[key][name] = Spinbox(self, textvariable=StringVar(), from_=minInclude, to=maxInclude, text=str(p.getAttribute("value")))
                elif minInclude.isdigit():
                    self.ui[key][name] = Spinbox(self, textvariable=StringVar(), from_=minInclude, to=1024, text=str(p.getAttribute("value")))
                else:
                    self.ui[key][name] = Entry(self, textvariable=StringVar(), text=str(p.getAttribute("value")))

                self.ui[key][name].grid(column=1, row=r)
                
                ####################
                # message label
                if (min==1 and max==1) or (min=="" and max==""):
                    msg += " required"
                    required = "yes"
                if max>0:
                    repeat = "yes"
                    #msg += " repeatable"
                
                if (minInclude<>"" or maxInclude<>""):
                    msgMin = "any" if minInclude == "" else minInclude
                    msgMax = "any" if maxInclude == "" else maxInclude
                    msg += "%s to %s" %(msgMin, msgMax)
                
                onote = Label(self, text=msg)
                onote.grid(column=2, row=r)
                r += 1
            go = Button(self, text="Go", command= lambda key=key: self.callback_go(key) )
            go.grid(column=0, row=r, columnspan=4)
            key += 1
            r+=1

root = Tk()
root.title("OSD Options")
gui = GUI(root)
gui.process()
root.mainloop()

