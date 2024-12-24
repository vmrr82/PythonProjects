import tkinter as tk
from tkinter import ttk
from openpyxl import load_workbook
import subprocess
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.archivo= load_workbook('archivo.xlsx')
        self.hoja = self.archivo['Hoja1']
        self.numero = self.hoja['AB4'].value

    def escribir_numero(self):
        # Corrección: agregamos la variable `numero` como un atributo de la clase
        self.numero += 1
        self.hoja['AB4'] =self.numero
        self.archivo.save(f'In-54_{self.numero}.xlsx')
      
    def num_inicial(self):
        ventana_inicial = tk.Tk()
        frm = ttk.Frame(ventana_inicial, padding=10)
        
        label_num = tk.Label(frm, text="Introduce el número inicial, por favor.")
        label_num.grid(column=0, row=0)
        
        num_var = tk.IntVar()
        
        entry_num = ttk.Entry(frm, textvariable=num_var)
        entry_num.grid(row=1, column=0, padx=10)
    
        def guardar_num():
                result_num = ttk.Label(frm, text=f"Número guardado ({entry_num.get()}).")
                result_num.grid(row=3, column=0)
                self.numero = int(entry_num.get())
                self.hoja['AB4'] =self.numero
                self.archivo.save('ejemplo.xlsx')
        
        button_num = ttk.Button(frm, text='Guardar', command=guardar_num)
        button_num.grid(row=2, column=0)
        
        
        
        frm.pack()
        
        ventana_inicial.title('Número inicial')
        ventana_inicial.geometry("300x150")
        ventana_inicial.resizable(False,False)
        ventana_inicial.mainloop()
 

    def convertir(self):
        nombre_archivo_excel = f'In-54_{self.numero}.xlsx'
        ruta_completa = os.path.abspath(nombre_archivo_excel)
    
        # Crear el comando para imprimir el archivo
        comando = f'scalc --headless --convert-to pdf --outdir {os.path.dirname(ruta_completa)} {ruta_completa}'
    
        # Ejecutar el comando en una nueva sesión de terminal
        subprocess.run(comando, shell=True)

    def create_widgets(self):
        numero_generado = tk.StringVar()
        label_numero = tk.Label(self, textvariable=numero_generado)
        label_numero

        # Corrección: agregamos el argumento "self" a la función command
        boton_inicial = tk.Button(self, text="Número Inicial", command=self.num_inicial, width=12)
        boton_inicial.grid(row=1, column=0,pady=5)
        boton_generar = tk.Button(self, text="Generar", command=self.escribir_numero, width=12)
        boton_generar.grid(row=2, column=0,pady=5)

        boton_convertir = tk.Button(self, text="Convertir PDF", command=self.convertir, width=12)
        boton_convertir.grid(row=3, column=0,pady=5)

        boton_salir = tk.Button(self, text="Salir", command=self.master.quit, width=12)
        boton_salir.grid(row=4, column=0,pady=5)

# Creamos la ventana principal
ventana = tk.Tk()
ventana.geometry("300x150")
ventana.resizable(False,False)
ventana.title("Generador IN-54")

# Creamos una instancia de la clase Application y la ejecutamos
app = Application(master=ventana)
app.mainloop()
