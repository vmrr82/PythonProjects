from tkinter import *
from tkinter import ttk
from tkinter import messagebox



raiz = Tk()
raiz.title('RAT')
raiz.geometry("200x200")

myFrame = ttk.Frame(raiz,width=100,height=100,padding=(3,3,3,3))
myFrame.pack()

entradaConversor = ttk.Entry(myFrame)
entradaConversor.grid(column=0,row=0,columnspan=1)

labelConversor = ttk.Label(myFrame,text="Convertir a").grid(column=0,row=0)
valoresConversor = ['KM/H','M/S']

boxConversor = ttk.Combobox(myFrame,width=7,values=valoresConversor)


def checkConversor():
    if boxConversor.get() == 'KM/H':
        ttk.Label(myFrame,text=int(entradaConversor.get()) /3.6).grid(column=3,row=0)
    elif boxConversor.get() == 'M/S':
        ttk.Label(myFrame,text=int(entradaConversor.get()) * 3.6).grid(column=3,row=0)

boxConversor.grid(column=2,row=0)
botonConversor = ttk.Button(myFrame,text='Click',command=checkConversor)
botonConversor.grid(column=2,row=1)



raiz.mainloop()