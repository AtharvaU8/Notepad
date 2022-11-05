from tkinter  import messagebox
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename , asksaveasfilename
import os
import datetime
from tkinter import filedialog,simpledialog

try:
    def select_all():
        textarea.tag_add("sel", "1.0","end") 

    def check():
        if str(textarea.get(1.0,END)).isspace():
            return False
        else:
            return True

    def newfile(event=None):
        global file
        notepad.title('Untitled - Notepad')
        if file == None and check():
            mb = messagebox.askyesnocancel("Notepad", "Do you want to save changes to Untitled")
            print(mb)
            if mb:
                file = None
                file = asksaveasfilename(initialfile="Untitled.txt",defaultextension=".txt",
                                        filetypes=[("All Files","*.*"),
                                            ("Text Documents","*.txt")])
                if file == '':
                    file = None
                else:
                    o = open(file,'w')
                    o.write(textarea.get(1.0,END))
                    o.close()
                    notepad.title(os.path.basename(file) + '- Notepad' )
            elif mb == None:
                pass
            else:
                file = None
                textarea.delete(1.0,END)
        else:
            file = None
            textarea.delete(1.0,END)

    def openfile(event=None):
        global file
        file = askopenfilename(defaultextension=".txt",
                                        filetypes=[("All Files","*.*"),
                                            ("Text Documents","*.txt")])

        if file == '':
            file = None
        else:
            notepad.title(os.path.basename(file) + '- Notepad')
            textarea.delete(1.0,END)
            o = open(file, 'r')
            textarea.insert(1.0, o.read())
            o.close()

    def savefile(event=None):
        global file
        if file == None:
            file = asksaveasfilename(initialfile="Untitled.txt",defaultextension=".txt",
                                        filetypes=[("All Files","*.*"),
                                            ("Text Documents","*.txt")])
            if file == '':
                file = None
            else:
                o = open(file,'w')
                o.write(textarea.get(1.0,END))
                o.close()

                notepad.title(os.path.basename(file) + '- Notepad' )
        else:
            o = open(file,'w')
            o.write(textarea.get(1.0,END))
            o.close()

    def saveas(event=None):
        global file

        file = asksaveasfilename(initialfile="Untitled.txt",defaultextension=".txt",
                                        filetypes=[("All Files","*.*"),
                                            ("Text Documents","*.txt")])
        if file == '':
            file = None
        else:
            o = open(file,'w')
            o.write(textarea.get(1.0,END))
            o.close()

            notepad.title(os.path.basename(file) + '- Notepad' )

    def quit():
        if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
            notepad.destroy()

    
    def find(event=None):     #edit menu Find option
        textarea.tag_remove("Found",'1.0', END)
        find = simpledialog.askstring("Find", "Find what:")
        if find:
            idx = '1.0'     #idx stands for index
        while 1:
            idx = textarea.search(find, idx, nocase = 1, stopindex = END)
            if not idx:
                break
            lastidx = '%s+%dc' %(idx, len(find))
            textarea.tag_add('Found', idx, lastidx)
            idx = lastidx
        textarea.tag_config('Found', foreground = 'white', background = 'blue')
        textarea.bind("<1>", click)

    def undo():
        textarea.event_generate("<<Undo>>")

    def delete(event=None): 
        textarea.event_generate("<<Clear>>")

    def click(event):     #handling click event
        textarea.tag_config('Found',background='white',foreground='black')

    def time_date(event=None):
        time = datetime.datetime.now().strftime('%H:%M:%S')
        time+=" "
        now = datetime.datetime.now().strftime("%d-%m-%y")
        textarea.insert(INSERT,time)
        textarea.insert(END,now)

    def copy():
        textarea.event_generate("<<Copy>>")

    def cut():
        textarea.event_generate("<<Cut>>")

    def paste():
        textarea.event_generate("<<Paste>>")
        
    def help():
        showinfo("Notepad", "Notepad by Atharva")

    notepad = Tk()
    notepad.title('Untitled - Notepad')
    notepad.geometry('1000x500')
    notepad.wm_iconbitmap('notepad.ico')
    textarea = Text(notepad, font='consolas 11')
    textarea.pack(expand=True,fill=BOTH)
    file = None

    # menubar 
    menubar = Menu(notepad)

    # filemenu starts
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label = 'New                          Ctrl+N', command =newfile)
    notepad.bind('<Control-n>', newfile)
    filemenu.add_command(label = 'Open                        Ctrl+O', command =openfile)
    notepad.bind('<Control-o>', openfile)
    filemenu.add_command(label = 'Save                          Ctrl+S', command =savefile)
    notepad.bind('<Control-s>', savefile)
    filemenu.add_command(label = 'Save As          Ctrl+Shift+S', command =saveas)
    notepad.bind('<Control-S>', saveas)
    filemenu.add_separator()
    filemenu.add_command(label = 'Exit', command =quit)    
    menubar.add_cascade(label = 'File', menu = filemenu)
    # filemenu ends

    # editmenu starts
    editmenu = Menu(menubar, tearoff=0)
        
    editmenu.add_command(label = 'Undo                       Ctrl+Z', command =undo)
    editmenu.add_separator()
    editmenu.add_command(label = 'Cut                          Ctrl+X', command =cut)
    editmenu.add_command(label = 'Copy                       Ctrl+C', command =copy)
    editmenu.add_command(label = 'Paste                       Ctrl+V', command =paste)
    editmenu.add_command(label='Delete                           Del', command = delete)
    notepad.bind('Del', delete)                              
    editmenu.add_separator()                                 
    editmenu.add_command(label = 'Find                         Ctrl+F', command =find)
    notepad.bind('<Control-f>', find)
    editmenu.add_separator()
    editmenu.add_command(label = 'Select All                Ctrl+A', command =select_all)
    editmenu.add_command(label = 'Time/Date                     F5', command =time_date)
    notepad.bind('<F5>', time_date)
    menubar.add_cascade(label = 'Edit', menu = editmenu)
    # editmenu ends

    # helpmenu starts
    helpmenu = Menu(menubar, tearoff=0)

    helpmenu.add_command(label = 'About Notepad', command =help)
    menubar.add_cascade(label = 'Help', menu = helpmenu)
    # helpmenu ends
    notepad.config(menu=menubar)

    scrollbar = Scrollbar(textarea)
    scrollbar.pack(side=RIGHT,fill=Y)
    scrollbar.config(command=textarea.yview)
    textarea.config(yscrollcommand=scrollbar.set) 

    notepad.mainloop()
    
except Exception as e:
    e