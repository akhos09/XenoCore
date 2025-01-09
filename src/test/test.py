import customtkinter as ctk
import tkinter as tk

class XenoDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("XenoDashboard")
        self.root.geometry("800x600")

        # Configurar el tema de CustomTkinter
        ctk.set_appearance_mode("light") # Modo oscuro
          # Tema azul

        # Crear un menú superior clásico con el fondo del tema
        self.crear_menu()

        # Crear un panel de pestañas
        self.crear_panel_pestanas()

    def crear_menu(self):
        # Crear un menú con tk.Menu y personalizar colores
        menubar = tk.Menu(self.root, bg="#2b2b2b", fg="white", activebackground="white", activeforeground="white")

        # Menú "Archivo"
        file_menu = tk.Menu(menubar, tearoff=0, bg="#2b2b2b", fg="white", activebackground="#3b3b3b", activeforeground="white")
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Menú "Ayuda"
        help_menu = tk.Menu(menubar, tearoff=0, bg="#2b2b2b", fg="white", activebackground="#3b3b3b", activeforeground="white")
        help_menu.add_command(label="Acerca de")
        menubar.add_cascade(label="Ayuda", menu=help_menu)

        # Configurar el menú en la ventana principal
        self.root.config(menu=menubar)

    def crear_panel_pestanas(self):
        # Crear un panel de pestañas con CustomTkinter
        panel_pestanas = ctk.CTkTabview(self.root)
        panel_pestanas.pack(expand=True, fill="both", padx=10, pady=10)

        # Pestaña de Vagrant
        pestana_vagrant = panel_pestanas.add("Vagrant")
        self.crear_contenido_vagrant(pestana_vagrant)

        # Pestaña de Microservicios
        pestana_microservicios = panel_pestanas.add("Microservicios")
        self.crear_contenido_microservicios(pestana_microservicios)

        # Pestaña de Virtualización
        pestana_virtualizacion = panel_pestanas.add("Virtualización")
        self.crear_contenido_virtualizacion(pestana_virtualizacion)

    def crear_contenido_vagrant(self, frame):
        label_vagrant = ctk.CTkLabel(frame, text="Gestión de Máquinas Virtuales con Vagrant", font=("Arial", 14))
        label_vagrant.pack(pady=10)

        boton_crear_vm = ctk.CTkButton(frame, text="Crear VM", command=self.crear_vm)
        boton_crear_vm.pack(pady=5)

        boton_iniciar_vm = ctk.CTkButton(frame, text="Iniciar VM", command=self.iniciar_vm)
        boton_iniciar_vm.pack(pady=5)

    def crear_contenido_microservicios(self, frame):
        label_microservicios = ctk.CTkLabel(frame, text="Instalación de Microservicios", font=("Arial", 14))
        label_microservicios.pack(pady=10)

        boton_instalar_microservicio = ctk.CTkButton(frame, text="Instalar Microservicio", command=self.instalar_microservicio)
        boton_instalar_microservicio.pack(pady=5)

    def crear_contenido_virtualizacion(self, frame):
        label_virtualizacion = ctk.CTkLabel(frame, text="Herramientas de Virtualización", font=("Arial", 14))
        label_virtualizacion.pack(pady=10)

        boton_crear_red_virtual = ctk.CTkButton(frame, text="Crear Red Virtual", command=self.crear_red_virtual)
        boton_crear_red_virtual.pack(pady=5)

    def crear_vm(self):
        print("Creando una máquina virtual con Vagrant...")

    def iniciar_vm(self):
        print("Iniciando una máquina virtual con Vagrant...")

    def instalar_microservicio(self):
        print("Instalando un microservicio...")

    def crear_red_virtual(self):
        print("Creando una red virtual...")

if __name__ == '__main__':
    root = ctk.CTk()
    app = XenoDashboard(root)
    root.mainloop()