import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()         
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.quitbutton = tk.Button(command=self.quit, text="Bye!", anchor=tk.CENTER)
        self.quitbutton.grid()

app = Application()                       

app.master.title('Sample application')    

app.mainloop()


