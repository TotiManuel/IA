import tkinter as tk
from tkinter import messagebox
from Control.Control import Control

class Visual:
    def __init__(self):
        self.messageBox = messagebox
        self.control = Control()
    
    def verificarInicio(self, respuesta):
        if respuesta == True:
            print("si")
        else:
            print("No")

    def opcionBoton(self, eleccion):
        if eleccion == "camara":
            self.messageBox.showwarning("Camara.","Se iniciara la camara.")
            self.control.iniciarCamara()
        elif eleccion == "reconocimiento":
            self.messageBox.showwarning("Camara.","Se iniciara la camara y hara un reconocimiento facial.")
            self.control.iniciarReconocimiento()
        elif eleccion == "reconocimientovoz":
            self.messageBox.showwarning("Reconocimiento.","Se iniciara el reconocimiento de voz.")
            self.control.iniciarReconVoz()
    
    def nuevo_archivo(self):
        messagebox.showinfo("Nuevo", "Crear un nuevo archivo.")
    
    def abrir_archivo(self):
        messagebox.showinfo("Abrir", "Abrir un archivo existente.")
    
    def salir(self):
        self.root.quit()
    
    def pegar(self):
        messagebox.showinfo("Pegar", "Pegar contenido.")
    
    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Aplicación de ejemplo con menú en Tkinter.")

    def inicio(self):
        #self.messageBox.showwarning("ADVERTENCIA: Acceso no autorizado.","No tienes acceso para utilizar este dispositivo por favor dejalo, usamos reconocimieto facial para identificarte.")
        #respuesta = self.messageBox.askyesno("Continuar?", "Si continuas tus datos seran usado para lo que creamos convenientes para que devuelvas el dispositivo")
        #self.verificarInicio(respuesta)
        
        #region ConfiguracionVentana
        self.root = tk.Tk()
        self.root.title("JMM")
        self.root.geometry("500x500")
        #endregion
    
        #region menu

        # Crear un menú en la parte superior
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Crear el menú "Archivo"
        archivo_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.salir)
        
        # Crear el menú "Edición"
        editar_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Funciones", menu=editar_menu)
        editar_menu.add_command(label="Abrir Camara", command=lambda:self.opcionBoton("camara"))
        editar_menu.add_command(label="Reconocimiento Facial", command=lambda:self.opcionBoton("reconocimiento"))
        editar_menu.add_command(label="Reconocimiento De Voz", command=lambda:self.opcionBoton("reconocimientovoz"))
        
        # Crear el menú "Ayuda"
        ayuda_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.acerca_de)

        #endregion

        self.botonCamara = tk.Button(self.root, text="Iniciar Camara", command=lambda:self.opcionBoton("camara"))
        self.botonCamara.pack(pady=1)
        self.botonFacial = tk.Button(self.root, text="Reconocimiento Facial", command=lambda:self.opcionBoton("reconocimiento"))
        self.botonFacial.pack(pady=1)
        self.botonVoz = tk.Button(self.root, text="Reconocimiento de Voz", command=lambda:self.opcionBoton("reconocimientovoz"))
        self.botonVoz.pack(pady=1)
        self.botonMail = tk.Button(self.root, text="Enviar Mail")
        self.botonMail.pack(pady=1)
        self.botonSalir = tk.Button(self.root, text="Salir", command=lambda:self.root.destroy())
        self.botonSalir.pack(pady=1)
        
        self.root.mainloop()