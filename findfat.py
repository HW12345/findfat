import tkinter
import tkinter.messagebox,tkinter.simpledialog
import os,os.path
import threading

rubbishExt=['.tmp','.bak','.old','.wbk','.xlk','._mp','.gid','.chk','.syd','.$$$','.@@@','.~*']

class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        
        
        menu = tkinter.Menu(self.root)

        
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="about...",command = self.MenuAbout)
        submenu.add_separator() 
        submenu.add_command(label="exit", command = self.MenuExit)
        menu.add_cascade(label="system", menu=submenu)
        
        
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="scan", command = self.MenuScanRubbish)
        submenu.add_command(label="delete", command = self.MenuDelRubbish)
        menu.add_cascade(label="clear", menu=submenu)

        
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="find big file", command = self.MenuScanBigFile)  
        submenu.add_separator()             
        submenu.add_command(label="find(using name)", command = self.MenuSearchFile)
        menu.add_cascade(label="find", menu=submenu)

        self.root.config(menu=menu)
        
        
        self.progress = tkinter.Label(self.root,anchor = tkinter.W,
            text = 'status',bitmap = 'hourglass',compound = 'left')
        self.progress.place(x=10,y=370,width = 480,height = 15)

        
        self.flist = tkinter.Text(self.root)
        self.flist.place(x=10,y = 10,width = 480,height = 350)
        
        
        self.vscroll = tkinter.Scrollbar(self.flist)
        self.vscroll.pack(side = 'right',fill = 'y')
        self.flist['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.flist.yview

    
    def MenuAbout(self):
        tkinter.messagebox.showinfo("Window findfat",
            "This is a findfat app\nby HW")

    
    def MenuExit(self):
        self.root.quit();

    
    def MenuScanRubbish(self):
        result = tkinter.messagebox.askquestion("Window findfat","countinue?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("Window findfat","start")
        
        self.drives =GetDrives()
        t=threading.Thread(target=self.ScanRubbish,args=(self.drives,))
        t.start()

    
    def MenuDelRubbish(self):
        result = tkinter.messagebox.askquestion("Window findfat","countinue?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("Window findfat","start")
        self.drives =GetDrives()
        t=threading.Thread(target=self.DeleteRubbish,args=(self.drives,))
        t.start()       
    
    
    def MenuScanBigFile(self):
        s = tkinter.simpledialog.askinteger('Window findfat','how big?  (M)')
        t=threading.Thread(target=self.ScanBigFile,args=(s,))
        t.start()   
    
    
    def MenuSearchFile(self):
        s = tkinter.simpledialog.askstring('Window findfat','type what you want to look for')
        t=threading.Thread(target=self.SearchFile,args=(s,))
        t.start()   
    
    
    def ScanRubbish(self,scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root,dirs,files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] == '':  
                            continue
                        try:
                            if rubbishExt.index(filesplit[1]) >=0:  
                                fname = os.path.join(os.path.abspath(root),fil)
                                filesize += os.path.getsize(fname)
                                if total % 15 == 0:
                                    self.flist.delete(0.0,tkinter.END)
                                
                                l = len(fname)
                                if l > 50:
                                    fname = name[:25] + '...' + fname[l-25:l]
                                self.flist.insert(tkinter.END,fname + '\n')
                                self.progress['text'] = fname
                                total += 1  
                        except ValueError:
                            pass
                except Exception as e:
                    print(e)
                    pass
        self.progress['text'] = "find %s rubbish, use %.2f M space" % (total,filesize/1024/1024)

    
    def DeleteRubbish(self,scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root,dirs,files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] == '':  
                            continue
                        try:
                            if rubbishExt.index(filesplit[1]) >=0: 
                                fname = os.path.join(os.path.abspath(root),fil)
                                filesize += os.path.getsize(fname)

                                try:
                                    os.remove(fname)    
                                    l = len(fname)
                                    if l > 50:
                                        fname = fname[:25] + '...' + fname[l-25:l]
                                    
                                    if total % 15 == 0:
                                        self.flist.delete(0.0,tkinter.END)

                                    self.flist.insert(tkinter.END,'Deleted '+ fname + '\n')
                                    self.progress['text'] = fname
                                    
                                    total += 1  
                                except:                
                                    pass                                
                        except ValueError:
                            pass
                except Exception as e:
                    print(e)
                    pass
        self.progress['text'] = "delete X%s rubbish，get %.2f M space" % (total,filesize/1024/1024)   
    
    
    def ScanBigFile(self,filesize):
        total = 0
        filesize = filesize * 1024 * 1024
        for drive in GetDrives():
            for root,dirs,files in os.walk(drive):
                for fil in files:
                    try:
                        fname = os.path.abspath(os.path.join(root,fil))                     
                        fsize = os.path.getsize(fname)

                        self.progress['text'] = fname  
                        if fsize >= filesize:                           
                            total += 1                      
                            self.flist.insert(tkinter.END, '%s，[%.2f M]\n' % (fname,fsize/1024/1024))                           
                    except:
                        pass
        self.progress['text'] = "find %s more than %s M file" % (total,filesize/1024/1024)
    
    
    def SearchFile(self,fname):
        total = 0
        fname = fname.upper()
        for drive in GetDrives():
            for root,dirs,files in os.walk(drive):
                for fil in files:
                    try:
                        fn = os.path.abspath(os.path.join(root,fil))    
                        l = len(fn)
                        if l > 50:
                            self.progress['text'] = fn[:25] + '...' + fn[l-25:l]    
                        else:
                            self.progress['text'] = fn          

                        if fil.upper().find(fname) >= 0 :                       
                            total += 1                      
                            self.flist.insert(tkinter.END, fn + '\n')                           
                    except:
                        pass
        self.progress['text'] = "find %s file" % (total)

    def MainLoop(self):
        self.root.title("Window findfat”")
        self.root.minsize(500,400)
        self.root.maxsize(500,400)
        self.root.mainloop()


def GetDrives():
    drives=[]
    for i in range(65,91):
        vol = chr(i) + ':/'
        if os.path.isdir(vol):
            drives.append(vol)
    return tuple(drives)


if __name__ == "__main__" :
    window = Window()
    window.MainLoop()
