#!/usr/bin/python

import xml.dom.minidom

import tkinter
#from ttk import Frame, Label, Entry, Button
#from tkinter import Tk, StringVar, BOTH, W, E
import tkinter.messagebox

from tkinter import Frame, Label, Entry, Button, StringVar, Tk, BOTH, W, E
#from tkinter import

import sys


def printf(format, *args):
    sys.stdout.write(format % args)


def fprintf(fp, format, *args):
    fp.write(format % args)


# get an XML element with specified name
def getElement(parent, name):
    nodeList = []
    if parent.childNodes:
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == name:
                    nodeList.append(node)
    return nodeList[0]


# get value of an XML element with specified name
def getElementValue(parent, name):
    if parent.childNodes:
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == name:
                    if node.hasChildNodes:
                        child = node.firstChild
                        return child.nodeValue
    return None


# set value of an XML element with specified name
def setElementValue(parent, name, value):
    if parent.childNodes:
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == name:
                    if node.hasChildNodes:
                        child = node.firstChild
                        child.nodeValue = value
    return None


class Application(Frame):

    def __init__(self, parent):
        # initialize frame
        Frame.__init__(self, parent)

        # set root as parent
        self.parent = parent

        # read and parse XML document
        DOMTree = xml.dom.minidom.parse("config.xml")

        # create attribute for XML document
        self.xmlDocument = DOMTree.documentElement

        # get value of "rdbms" element
        self.database = StringVar()
        self.database.set(getElementValue(self.xmlDocument, "rdbms"))

        # get value of "benckmark" element
        self.benchmark = StringVar()
        self.benchmark.set(getElementValue(self.xmlDocument, "bm"))

        # create attribute for "oracle" element
        self.xmlOracle = getElement(self.xmlDocument, "oracle")

        # create attribute for "service" element
        self.xmlService = getElement(self.xmlOracle, "service")

        # get value of "system_user" element
        self.systemUser = StringVar()
        self.systemUser.set(getElementValue(self.xmlService, "system_user"))

        # get value of "system_password" element
        self.systemPassword = StringVar()
        self.systemPassword.set(getElementValue(self.xmlService, "system_password"))

        # get value of "service_name" element
        self.serviceName = StringVar()
        self.serviceName.set(getElementValue(self.xmlService, "service_name"))

        # initialize UI
        self.initUI()

    def initUI(self):
        # set frame title
        self.parent.title("HammerDB")

        # pack frame
        self.pack(fill=BOTH, expand=1)

        # configure grid columns
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)

        # configure grid rows
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(6, pad=3)

        # database
        label1 = Label(self, text="Database: ")
        label1.grid(row=0, column=0, sticky=W)

        entry1 = Entry(self, width=30, textvariable=self.database)
        entry1.grid(row=0, column=1)

        # bench mark
        label2 = Label(self, text="Benckmark : ")
        label2.grid(row=1, column=0, sticky=W)

        entry2 = Entry(self, width=30, textvariable=self.benchmark)
        entry2.grid(row=1, column=1)

        # service name
        label3 = Label(self, text="Service Name : ")
        label3.grid(row=2, column=0, sticky=W)

        entry3 = Entry(self, width=30, textvariable=self.serviceName)
        entry3.grid(row=2, column=1)

        # system user
        label4 = Label(self, text="System User : ")
        label4.grid(row=3, column=0, sticky=W)

        entry4 = Entry(self, width=30, textvariable=self.systemUser)
        entry4.grid(row=3, column=1)

        # system user password
        label5 = Label(self, text="System User Password : ")
        label5.grid(row=4, column=0, sticky=W)

        entry5 = Entry(self, width=30, textvariable=self.systemPassword)
        entry5.grid(row=4, column=1)

        # blank line
        label6 = Label(self, text="")
        label6.grid(row=5, column=0, sticky=E + W)

        # create OK button
        button1 = Button(self, text="OK", command=self.onOK)
        button1.grid(row=6, column=0, sticky=E)

        # create Cancel button
        button2 = Button(self, text="Cancel", command=self.onCancel)
        button2.grid(row=6, column=1, sticky=E)

    def onOK(self):
        # set values in xml document
        setElementValue(self.xmlDocument, "rdbms", self.database.get())
        setElementValue(self.xmlDocument, "bm", self.benchmark.get())
        setElementValue(self.xmlService, "system_user", self.systemUser.get())
        setElementValue(self.xmlService, "system_password", self.systemPassword.get())
        setElementValue(self.xmlService, "service_name", self.serviceName.get())

        # open XML file
        f = open("config.xml", "w")

        # set xml header
        fprintf(f, '<?xml version="1.0" encoding="utf-8"?>\n')

        # write XML document to XML file
        self.xmlDocument.writexml(f)

        # close XML file
        f.close()

        # show confirmation message
        tkinter.messagebox.showerror("Message", "Configuration updated successfully")
#        messageBox.showerror("Message", "Configuration updated successfully")

        # exit program
        self.quit()

    def onCancel(self):
        # exit program
        self.quit()


def main():
    # initialize root object
    root = Tk()

    # set size of frame
    root.geometry("410x160+300+300")

    # call object
    app = Application(root)

    # enter main loop
    root.mainloop()


# if this is the main thread then call main() function
if __name__ == '__main__':
    main()