# Limite/limite_estudiante.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
from Control.controlador_solicitud import ControladorSolicitud
from Control.controlador_estudiante import ControladorEstudiante
from Persistencia.equipo_dao import EquipoDAO
from Entity.Solicitud import Solicitud
from Entity.Estudiante import Estudiante
import os

class LimiteEstudiante:
    def __init__(self, root=None):
        # Colores
        self.COLOR_PRIMARY = "#4a6fa5"  # Azul oscuro
        self.COLOR_SECONDARY = "#6d98e3"  # Azul medio
        self.COLOR_ACCENT = "#2d4a72"  # Azul más oscuro
        self.COLOR_BACKGROUND = "#f5f5f5"  # Gris muy claro
        self.COLOR_TEXT = "#333333"  # Casi negro
        
        self.controlador_solicitud = ControladorSolicitud()
        self.controlador_estudiante = ControladorEstudiante()
        self.equipo_dao = EquipoDAO()
        
        if root is None:
            self.root = tk.Tk()
            self.root.title("Sistema de Préstamos - Estudiante")
            self.root.geometry("900x650")
            self.root.minsize(800, 600)
            self.should_close_root = True
        else:
            self.root = root
            self.root.title("Sistema de Préstamos - Estudiante")
            self.root.geometry("900x650")
            self.root.minsize(800, 600)
            self.should_close_root = False
            
        self.root.configure(bg=self.COLOR_BACKGROUND)
        
        # Configurar estilos
        self.setup_styles()
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, style="MainFrame.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título y barra superior
        self.header_frame = ttk.Frame(self.main_frame, style="MainFrame.TFrame")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Portal del Estudiante",
            font=("Arial", 24, "bold"),
            foreground=self.COLOR_PRIMARY,
            background=self.COLOR_BACKGROUND
        )
        self.title_label.pack(side=tk.LEFT)
        
        self.back_button = ttk.Button(
            self.header_frame, 
            text="Volver",
            command=self.volver_menu_principal,
            style="NormalButton.TButton"
        )
        self.back_button.pack(side=tk.RIGHT)
        
        # Contenido - Notebook para las pestañas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Solicitud de Préstamo
        self.solicitud_frame = ttk.Frame(self.notebook, style="ContentFrame.TFrame")
        self.notebook.add(self.solicitud_frame, text="Solicitar Préstamo")
        
        # Pestaña de Consulta de Solicitudes
        self.consulta_frame = ttk.Frame(self.notebook, style="ContentFrame.TFrame")
        self.notebook.add(self.consulta_frame, text="Consultar Solicitudes")
        
        # Configurar pestaña de Solicitud de Préstamo
        self.setup_solicitud_frame()
        
        # Configurar pestaña de Consulta de Solicitudes
        self.setup_consulta_frame()
    
    def setup_styles(self):
        """Configura los estilos personalizados de los widgets"""
        self.style = ttk.Style()
        self.style.configure("MainFrame.TFrame", background=self.COLOR_BACKGROUND)
        self.style.configure("ContentFrame.TFrame", background=self.COLOR_BACKGROUND)
        
        # Configuración para Treeview (tabla)
        self.style.configure("Treeview", 
                            background=self.COLOR_BACKGROUND,
                            foreground=self.COLOR_TEXT,
                            rowheight=25,
                            fieldbackground=self.COLOR_BACKGROUND)
        
        self.style.map('Treeview', 
                     background=[('selected', self.COLOR_SECONDARY)])
        
        # Botones
        self.style.configure("AccentButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_PRIMARY,
                            foreground="black")
        
        self.style.map("AccentButton.TButton",
                      background=[('active', self.COLOR_SECONDARY)],
                      foreground=[('active', 'black')])
        
        self.style.configure("NormalButton.TButton", 
                            font=("Arial", 11),
                            background="#e0e0e0",
                            foreground="black")
        
        self.style.map("NormalButton.TButton",
                      background=[('active', "#c0c0c0")],
                      foreground=[('active', 'black')])
    
    def setup_solicitud_frame(self):
        """Configura la pestaña de solicitud de préstamo"""
        # Formulario para identificación
        self.form_frame = ttk.Frame(self.solicitud_frame, style="ContentFrame.TFrame")
        self.form_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Título
        ttk.Label(
            self.form_frame, 
            text="Solicitud de Préstamo de Equipo",
            font=("Arial", 16, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(pady=(0, 15))
        
        # Mensaje de advertencia sobre el plazo de préstamo
        ttk.Label(
            self.form_frame,
            text="Todos los préstamos son por un plazo de 7 días",
            font=("Arial", 11, "bold"),
            foreground="#F44336",  # Rojo
            background=self.COLOR_BACKGROUND
        ).pack(pady=(0, 5))
        
        # Campos del formulario
        self.form_fields_frame = ttk.Frame(self.form_frame, style="ContentFrame.TFrame")
        self.form_fields_frame.pack(fill=tk.X, padx=50)
        
        # DNI
        ttk.Label(
            self.form_fields_frame, 
            text="DNI:",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.dni_var = tk.StringVar()
        self.dni_entry = ttk.Entry(self.form_fields_frame, textvariable=self.dni_var, width=30)
        self.dni_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Botón de verificación
        self.verificar_button = ttk.Button(
            self.form_fields_frame, 
            text="Verificar",
            command=self.verificar_estudiante,
            style="NormalButton.TButton"
        )
        self.verificar_button.grid(row=0, column=2, padx=10, pady=5)
        
        # Marcos adicionales que se mostrarán después de verificar
        self.info_estudiante_frame = ttk.Frame(self.form_frame, style="ContentFrame.TFrame")
        
        # Equipos disponibles
        self.equipos_frame = ttk.LabelFrame(
            self.solicitud_frame, 
            text="Equipos Disponibles",
            style="ContentFrame.TFrame"
        )
        self.equipos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(20, 10))
        
        # Lista de equipos disponibles con columna de checkbox unicode
        self.equipos_treeview = ttk.Treeview(
            self.equipos_frame,
            columns=("check", "id", "tipo", "marca", "modelo"),
            show="headings",
            selectmode="none"
        )
        self.equipos_treeview.heading("check", text="✔")
        self.equipos_treeview.heading("id", text="ID")
        self.equipos_treeview.heading("tipo", text="Tipo")
        self.equipos_treeview.heading("marca", text="Marca")
        self.equipos_treeview.heading("modelo", text="Modelo")
        self.equipos_treeview.column("check", width=40, anchor="center")
        self.equipos_treeview.column("id", width=50, anchor="center")
        self.equipos_treeview.column("tipo", width=150)
        self.equipos_treeview.column("marca", width=150)
        self.equipos_treeview.column("modelo", width=200)
        
        # Scrollbar para la lista de equipos
        equipos_scrollbar = ttk.Scrollbar(
            self.equipos_frame, 
            orient=tk.VERTICAL, 
            command=self.equipos_treeview.yview
        )
        self.equipos_treeview.configure(yscrollcommand=equipos_scrollbar.set)
        
        self.equipos_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        equipos_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Checkbox seleccionar todo
        self.seleccionar_todo_var = tk.BooleanVar()
        self.seleccionar_todo_checkbox = ttk.Checkbutton(
            self.equipos_frame,
            text="Seleccionar todo",
            variable=self.seleccionar_todo_var,
            command=self.toggle_seleccionar_todo
        )
        self.seleccionar_todo_checkbox.pack(side=tk.TOP, pady=(0, 5))
        
        # Ocultar inicialmente las secciones hasta verificar estudiante
        self.equipos_frame.pack_forget()
    
    def setup_consulta_frame(self):
        """Configura la pestaña de consulta de solicitudes"""
        # Formulario para identificación
        self.consulta_form_frame = ttk.Frame(self.consulta_frame, style="ContentFrame.TFrame")
        self.consulta_form_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Título
        ttk.Label(
            self.consulta_form_frame, 
            text="Consulta de Solicitudes",
            font=("Arial", 16, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(pady=(0, 15))
        
        # Campos del formulario de consulta
        self.consulta_fields_frame = ttk.Frame(self.consulta_form_frame, style="ContentFrame.TFrame")
        self.consulta_fields_frame.pack(fill=tk.X, padx=50)
        
        # DNI
        ttk.Label(
            self.consulta_fields_frame, 
            text="DNI:",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.consulta_dni_var = tk.StringVar()
        self.consulta_dni_entry = ttk.Entry(self.consulta_fields_frame, textvariable=self.consulta_dni_var, width=30)
        self.consulta_dni_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Botón de consulta
        self.consultar_button = ttk.Button(
            self.consulta_fields_frame, 
            text="Consultar",
            command=self.consultar_solicitudes,
            style="NormalButton.TButton"
        )
        self.consultar_button.grid(row=0, column=2, padx=10, pady=5)
        
        # Resultados de la consulta
        self.resultados_frame = ttk.LabelFrame(
            self.consulta_frame, 
            text="Mis Solicitudes",
            style="ContentFrame.TFrame"
        )
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(20, 10))
        
        # Lista de solicitudes
        self.solicitudes_treeview = ttk.Treeview(
            self.resultados_frame,
            columns=("numero", "fecha", "estado", "equipos"),
            show="headings",
            selectmode="browse"
        )
        
        self.solicitudes_treeview.heading("numero", text="Número")
        self.solicitudes_treeview.heading("fecha", text="Fecha")
        self.solicitudes_treeview.heading("estado", text="Estado")
        self.solicitudes_treeview.heading("equipos", text="Equipos")
        
        self.solicitudes_treeview.column("numero", width=100, anchor="center")
        self.solicitudes_treeview.column("fecha", width=150, anchor="center")
        self.solicitudes_treeview.column("estado", width=100, anchor="center")
        self.solicitudes_treeview.column("equipos", width=300)
        
        # Scrollbar para la lista de solicitudes
        solicitudes_scrollbar = ttk.Scrollbar(
            self.resultados_frame, 
            orient=tk.VERTICAL, 
            command=self.solicitudes_treeview.yview
        )
        self.solicitudes_treeview.configure(yscrollcommand=solicitudes_scrollbar.set)
        
        self.solicitudes_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        solicitudes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Ocultar inicialmente hasta hacer la consulta
        self.resultados_frame.pack_forget()
    
    def verificar_estudiante(self):
        """Verifica si el estudiante existe y muestra opciones adicionales"""
        dni = self.dni_var.get().strip()
        
        if not dni:
            messagebox.showerror("Error", "Por favor, ingrese un DNI válido")
            return
        
        # Validar formato del DNI (para este ejemplo: números y letras, 8-10 caracteres)
        if not re.match(r'^[0-9A-Za-z]{5,15}$', dni):
            messagebox.showerror("Error", "El DNI debe tener entre 5 y 15 caracteres alfanuméricos")
            return
        
        # Verificar si el estudiante existe
        estudiante = self.controlador_estudiante.obtener_estudiante_por_dni(dni)
        
        if estudiante:
            # Verificar morosidad
            if self.controlador_estudiante.consultar_morosidad(dni):
                messagebox.showwarning(
                    "Morosidad Detectada", 
                    "No puede realizar solicitudes porque tiene préstamos vencidos."
                )
                return
            
            # Mostrar información del estudiante
            self.mostrar_info_estudiante(estudiante)
        else:
            # Mostrar formulario de registro
            self.mostrar_formulario_registro()
    
    def mostrar_info_estudiante(self, estudiante):
        """Muestra la información del estudiante existente"""
        for widget in self.info_estudiante_frame.winfo_children():
            widget.destroy()
        ttk.Label(
            self.info_estudiante_frame, 
            text=f"Bienvenido/a, {estudiante.nombre}",
            font=("Arial", 14, "bold"),
            foreground=self.COLOR_PRIMARY,
            background=self.COLOR_BACKGROUND
        ).pack(pady=(10, 5))
        ttk.Label(
            self.info_estudiante_frame, 
            text=f"Correo: {estudiante.correo}",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(pady=2)
        self.info_estudiante_frame.pack(fill=tk.X, pady=10)
        self.solicitar_button = ttk.Button(
            self.info_estudiante_frame, 
            text="Solicitar Préstamo",
            command=self.solicitar_prestamo,
            style="AccentButton.TButton"
        )
        self.solicitar_button.pack(pady=(10, 5))
        self.seleccionar_todo_var.set(False)
        self.cargar_equipos_disponibles()
        self.equipos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(20, 10))
    
    def mostrar_formulario_registro(self):
        """Muestra el formulario para registrar nuevo estudiante"""
        for widget in self.info_estudiante_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.info_estudiante_frame, 
            text="Registrar Nuevo Estudiante",
            font=("Arial", 14, "bold"),
            foreground=self.COLOR_PRIMARY,
            background=self.COLOR_BACKGROUND
        ).pack(pady=(10, 15))
        
        # Formulario
        form_frame = ttk.Frame(self.info_estudiante_frame, style="ContentFrame.TFrame")
        form_frame.pack(fill=tk.X, padx=50)
        
        # Nombre
        ttk.Label(
            form_frame, 
            text="Nombre completo:",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(form_frame, textvariable=self.nombre_var, width=30)
        self.nombre_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Correo
        ttk.Label(
            form_frame, 
            text="Correo electrónico:",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.correo_var = tk.StringVar()
        self.correo_entry = ttk.Entry(form_frame, textvariable=self.correo_var, width=30)
        self.correo_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Botón de registro
        self.registro_button = ttk.Button(
            self.info_estudiante_frame, 
            text="Registrar y Continuar",
            command=self.registrar_estudiante,
            style="AccentButton.TButton"
        )
        self.registro_button.pack(pady=15)
        
        self.info_estudiante_frame.pack(fill=tk.X, pady=10)
    
    def registrar_estudiante(self):
        """Registra un nuevo estudiante en el sistema"""
        dni = self.dni_var.get().strip()
        nombre = self.nombre_var.get().strip()
        correo = self.correo_var.get().strip()
        
        # Validar campos
        if not nombre:
            messagebox.showerror("Error", "Por favor ingrese su nombre completo")
            return
        
        if not correo:
            messagebox.showerror("Error", "Por favor ingrese su correo electrónico")
            return
        
        # Validar formato del correo
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
            messagebox.showerror("Error", "Por favor ingrese un correo electrónico válido")
            return
        
        # Crear y registrar el estudiante
        nuevo_estudiante = Estudiante(None, dni, correo, nombre)
        estudiante = self.controlador_estudiante.registrar_estudiante(nuevo_estudiante)
        
        if estudiante:
            messagebox.showinfo("Registro Exitoso", f"¡{nombre} ha sido registrado exitosamente!")
            # Mostrar información y continuar
            self.mostrar_info_estudiante(estudiante)
        else:
            messagebox.showerror("Error", "No se pudo registrar el estudiante. Intente de nuevo.")
    
    def cargar_equipos_disponibles(self):
        """Carga la lista de equipos disponibles en el treeview con checkboxes unicode"""
        # Limpiar treeview
        for item in self.equipos_treeview.get_children():
            self.equipos_treeview.delete(item)
        self.checkbox_states = {}
        # Obtener equipos disponibles
        equipos_disponibles = self.equipo_dao.obtener_disponibles()
        if not equipos_disponibles:
            messagebox.showinfo("Sin Equipos", "No hay equipos disponibles en este momento.")
            return
        # Llenar treeview con checkboxes unicode
        for equipo in equipos_disponibles:
            iid = equipo.id
            self.equipos_treeview.insert(
                "",
                "end",
                iid=iid,
                values=("☐", equipo.id, equipo.tipo, equipo.marca, equipo.modelo)
            )
            self.checkbox_states[iid] = False
        # Asociar evento de click
        self.equipos_treeview.bind("<Button-1>", self.on_checkbox_click)
    
    def on_checkbox_click(self, event):
        """Maneja el click en la columna de checkbox unicode"""
        region = self.equipos_treeview.identify("region", event.x, event.y)
        if region == "cell":
            col = self.equipos_treeview.identify_column(event.x)
            if col == "#1":  # Columna de checkbox
                row = self.equipos_treeview.identify_row(event.y)
                if row:
                    self.checkbox_states[row] = not self.checkbox_states[row]
                    self.equipos_treeview.set(row, "check", "☑" if self.checkbox_states[row] else "☐")
                    # Actualizar seleccionar todo
                    all_checked = all(self.checkbox_states.values())
                    self.seleccionar_todo_var.set(all_checked)
    
    def toggle_seleccionar_todo(self):
        """Selecciona o deselecciona todos los equipos en el treeview"""
        check = self.seleccionar_todo_var.get()
        for iid in self.checkbox_states:
            self.checkbox_states[iid] = check
            self.equipos_treeview.item(iid, image=self.checkbox_checked if check else self.checkbox_unchecked)
    
    def solicitar_prestamo(self):
        """Procesa la solicitud de préstamo solo con los equipos marcados"""
        # Obtener solo los equipos marcados
        ids_equipos = [iid for iid, checked in self.checkbox_states.items() if checked]
        if not ids_equipos:
            messagebox.showerror("Error", "Por favor seleccione al menos un equipo")
            return
        dni_estudiante = self.dni_var.get().strip()
        solicitud, mensaje = self.controlador_solicitud.hacer_solicitud(dni_estudiante, ids_equipos)
        if solicitud:
            messagebox.showinfo(
                "Solicitud Exitosa", 
                f"{mensaje}\n\nNúmero de seguimiento: {solicitud.numero_seguimiento}"
            )
            self.cargar_equipos_disponibles()
            result = messagebox.askyesno(
                "Continuar", 
                "¿Desea realizar otra solicitud?"
            )
            if not result:
                self.notebook.select(1)
                self.consulta_dni_var.set(dni_estudiante)
                self.consultar_solicitudes()
        else:
            messagebox.showerror("Error", f"No se pudo crear la solicitud: {mensaje}")
    
    def consultar_solicitudes(self):
        """Consulta las solicitudes de un estudiante"""
        dni = self.consulta_dni_var.get().strip()
        
        if not dni:
            messagebox.showerror("Error", "Por favor, ingrese un DNI válido")
            return
        
        # Validar formato del DNI
        if not re.match(r'^[0-9A-Za-z]{5,15}$', dni):
            messagebox.showerror("Error", "El DNI debe tener entre 5 y 15 caracteres alfanuméricos")
            return
        
        # Verificar si el estudiante existe
        estudiante = self.controlador_estudiante.obtener_estudiante_por_dni(dni)
        
        if not estudiante:
            messagebox.showerror("Error", "No se encontró ningún estudiante con ese DNI")
            return
        
        # Obtener las solicitudes del estudiante
        solicitudes = self.controlador_solicitud.solicitud_dao.obtener_por_estudiante(estudiante.id)
        
        # Limpiar treeview
        for item in self.solicitudes_treeview.get_children():
            self.solicitudes_treeview.delete(item)
        
        if not solicitudes:
            messagebox.showinfo("Sin Solicitudes", "No tienes solicitudes registradas")
            return
        
        # Llenar treeview
        for solicitud in solicitudes:
            # Formatear lista de equipos
            equipos_str = ", ".join([f"{e.tipo} {e.marca}" for e in solicitud.equipos_solicitados])
            
            self.solicitudes_treeview.insert(
                "", 
                "end", 
                values=(
                    solicitud.numero_seguimiento,
                    solicitud.fecha_solicitud.strftime('%d/%m/%Y'),
                    solicitud.estado.value,
                    equipos_str
                )
            )
        
        # Mostrar sección de resultados
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(20, 10))
    
    def volver_menu_principal(self):
        """Cierra la ventana y muestra la principal si es necesario (igual que la X)"""
        # Si la ventana principal está oculta, mostrarla
        if hasattr(self.root, 'master') and self.root.master is not None:
            try:
                self.root.master.deiconify()
            except Exception:
                pass
        self.root.destroy()
    
    def run(self):
        """Ejecuta la interfaz gráfica"""
        self.root.mainloop()

if __name__ == "__main__":
    # Para pruebas
    app = LimiteEstudiante()
    app.run()