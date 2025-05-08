# Limite/limite_soporte.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
from Control.controlador_solicitud import ControladorSolicitud
from Control.controlador_prestamo import ControladorPrestamo
from Control.controlador_estudiante import ControladorEstudiante
from Entity.enumeraciones import EstadoSolicitud, EstadoPrestamo
from Persistencia.solicitud_dao import SolicitudDAO

class LimiteSoporte:
    def __init__(self, root=None):
        # Colores
        self.COLOR_PRIMARY = "#4a6fa5"  # Azul oscuro
        self.COLOR_SECONDARY = "#6d98e3"  # Azul medio
        self.COLOR_ACCENT = "#2d4a72"  # Azul más oscuro
        self.COLOR_BACKGROUND = "#f5f5f5"  # Gris muy claro
        self.COLOR_TEXT = "#333333"  # Casi negro
        self.COLOR_SUCCESS = "#4CAF50"  # Verde
        self.COLOR_WARNING = "#FFC107"  # Amarillo
        self.COLOR_DANGER = "#F44336"  # Rojo
        
        self.controlador_solicitud = ControladorSolicitud()
        self.controlador_prestamo = ControladorPrestamo()
        self.controlador_estudiante = ControladorEstudiante()
        self.solicitud_dao = SolicitudDAO()
        
        if root is None:
            self.root = tk.Tk()
            self.root.title("Sistema de Préstamos - Soporte Técnico")
            self.root.geometry("1000x700")
            self.root.minsize(900, 650)
            self.should_close_root = True
        else:
            self.root = root
            self.root.title("Sistema de Préstamos - Soporte Técnico")
            self.root.geometry("1000x700")
            self.root.minsize(900, 650)
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
            text="Panel de Soporte Técnico",
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
        
        # Menú principal de soporte
        self.menu_frame = ttk.Frame(self.main_frame, style="ContentFrame.TFrame")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        self.menu_buttons = []
        opciones = [
            ("Aprobar solicitud de préstamo", self.mostrar_aprobar_solicitud),
            ("Registrar devolución de equipo", self.mostrar_registrar_devolucion),
            ("Consultar estudiantes morosos", self.mostrar_morosos),
            ("Consultar estudiantes con N préstamos", self.mostrar_n_prestamos)
        ]
        for i, (texto, comando) in enumerate(opciones):
            btn = ttk.Button(
                self.menu_frame,
                text=texto,
                command=comando,
                style="AccentButton.TButton"
            )
            btn.pack(fill=tk.X, pady=10, padx=200)
            self.menu_buttons.append(btn)
        
        # Frame de contenido dinámico
        self.content_frame = ttk.Frame(self.main_frame, style="ContentFrame.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cargar datos iniciales
        self.cargar_solicitudes_pendientes()
    
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
        
        # Botones normales
        self.style.configure("NormalButton.TButton", 
                            font=("Arial", 11),
                            background="#e0e0e0")
        
        self.style.map("NormalButton.TButton",
                      background=[('active', "#c0c0c0")])
        
        # Botones de acción principal
        self.style.configure("AccentButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_PRIMARY,
                            foreground="white")
        
        self.style.map("AccentButton.TButton",
                      background=[('active', self.COLOR_SECONDARY)],
                      foreground=[('active', 'white')])
        
        # Botón de éxito (verde)
        self.style.configure("SuccessButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_SUCCESS,
                            foreground="white")
        
        self.style.map("SuccessButton.TButton",
                      background=[('active', "#2E7D32")],
                      foreground=[('active', 'white')])
        
        # Botón de advertencia (amarillo)
        self.style.configure("WarningButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_WARNING)
        
        self.style.map("WarningButton.TButton",
                      background=[('active', "#FFA000")])
        
        # Botón de peligro (rojo)
        self.style.configure("DangerButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_DANGER,
                            foreground="white")
        
        self.style.map("DangerButton.TButton",
                      background=[('active', "#D32F2F")],
                      foreground=[('active', 'white')])
    
    def limpiar_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_aprobar_solicitud(self):
        self.limpiar_content_frame()
        # Aquí va la lógica para mostrar solicitudes pendientes y aprobar/rechazar
        ttk.Label(self.content_frame, text="Aquí se mostrarán las solicitudes pendientes para aprobar/rechazar.", font=("Arial", 14)).pack(pady=20)
    
    def mostrar_registrar_devolucion(self):
        self.limpiar_content_frame()
        # Aquí va la lógica para registrar devolución
        ttk.Label(self.content_frame, text="Aquí se podrá registrar la devolución de un equipo.", font=("Arial", 14)).pack(pady=20)
    
    def mostrar_morosos(self):
        self.limpiar_content_frame()
        # Aquí va la lógica para mostrar estudiantes morosos
        ttk.Label(self.content_frame, text="Aquí se mostrarán los estudiantes morosos.", font=("Arial", 14)).pack(pady=20)
    
    def mostrar_n_prestamos(self):
        self.limpiar_content_frame()
        # Aquí va la lógica para consultar estudiantes con N préstamos
        ttk.Label(self.content_frame, text="Aquí se podrá consultar estudiantes con N préstamos.", font=("Arial", 14)).pack(pady=20)
    
    def cargar_solicitudes_pendientes(self):
        # Implementa la lógica para cargar solicitudes pendientes
        pass
    
    def volver_menu_principal(self):
        # Cierra la ventana de soporte y muestra el menú principal si existe
        if hasattr(self.root, 'master') and self.root.master is not None:
            try:
                self.root.master.deiconify()
            except Exception:
                pass
        self.root.destroy()

    def setup_solicitudes_frame(self):
        """Configura la pestaña de solicitudes pendientes"""
        # Panel superior con controles
        self.solicitudes_control_frame = ttk.Frame(self.solicitudes_frame, style="ContentFrame.TFrame")
        self.solicitudes_control_frame.pack(fill=tk.X, pady=(0, 10), padx=10)
        
        # Botón de actualizar
        self.actualizar_solicitudes_btn = ttk.Button(
            self.solicitudes_control_frame,
            text="Actualizar Lista",
            command=self.cargar_solicitudes_pendientes,
            style="NormalButton.TButton"
        )
        self.actualizar_solicitudes_btn.pack(side=tk.RIGHT, padx=5)
        
        # Título
        ttk.Label(
            self.solicitudes_control_frame,
            text="Solicitudes Pendientes de Aprobación",
            font=("Arial", 16, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(side=tk.LEFT, padx=5)
        
        # Lista de solicitudes pendientes
        self.solicitudes_list_frame = ttk.Frame(self.solicitudes_frame, style="ContentFrame.TFrame")
        self.solicitudes_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear treeview para solicitudes
        self.solicitudes_treeview = ttk.Treeview(
            self.solicitudes_list_frame,
            columns=("id", "seguimiento", "estudiante", "dni", "fecha", "equipos"),
            show="headings",
            selectmode="browse"
        )
        
        # Definir encabezados
        self.solicitudes_treeview.heading("id", text="ID")
        self.solicitudes_treeview.heading("seguimiento", text="N° Seguimiento")
        self.solicitudes_treeview.heading("estudiante", text="Estudiante")
        self.solicitudes_treeview.heading("dni", text="DNI")
        self.solicitudes_treeview.heading("fecha", text="Fecha")
        self.solicitudes_treeview.heading("equipos", text="Equipos")
        
        # Configurar anchos de columnas
        self.solicitudes_treeview.column("id", width=50, anchor="center")
        self.solicitudes_treeview.column("seguimiento", width=100, anchor="center")
        self.solicitudes_treeview.column("estudiante", width=150)
        self.solicitudes_treeview.column("dni", width=100, anchor="center")
        self.solicitudes_treeview.column("fecha", width=100, anchor="center")
        self.solicitudes_treeview.column("equipos", width=300)
        
        # Scrollbar
        solicitudes_scrollbar = ttk.Scrollbar(
            self.solicitudes_list_frame,
            orient=tk.VERTICAL,
            command=self.solicitudes_treeview.yview
        )
        self.solicitudes_treeview.configure(yscrollcommand=solicitudes_scrollbar.set)
        
        # Empaquetar elementos
        self.solicitudes_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        solicitudes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar evento de selección
        self.solicitudes_treeview.bind("<<TreeviewSelect>>", self.mostrar_detalles_solicitud)
        
        # Panel inferior para detalles y acciones
        self.solicitudes_details_frame = ttk.LabelFrame(
            self.solicitudes_frame,
            text="Detalles de la Solicitud",
            style="ContentFrame.TFrame"
        )
        self.solicitudes_details_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # Contenido de detalles
        self.detalles_solicitud_text = scrolledtext.ScrolledText(
            self.solicitudes_details_frame,
            wrap=tk.WORD,
            width=50,
            height=6,
            font=("Arial", 11)
        )
        self.detalles_solicitud_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detalles_solicitud_text.config(state=tk.DISABLED)
        
        # Botones de acción
        self.solicitudes_actions_frame = ttk.Frame(self.solicitudes_frame, style="ContentFrame.TFrame")
        self.solicitudes_actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.aprobar_solicitud_btn = ttk.Button(
            self.solicitudes_actions_frame,
            text="Aprobar Solicitud",
            command=self.aprobar_solicitud,
            style="SuccessButton.TButton"
        )
        self.aprobar_solicitud_btn.pack(side=tk.RIGHT, padx=5)
        
        self.rechazar_solicitud_btn = ttk.Button(
            self.solicitudes_actions_frame,
            text="Rechazar Solicitud",
            command=self.rechazar_solicitud,
            style="DangerButton.TButton"
        )
        self.rechazar_solicitud_btn.pack(side=tk.RIGHT, padx=5)
        
        # Deshabilitar botones inicialmente
        self.aprobar_solicitud_btn.config(state=tk.DISABLED)
        self.rechazar_solicitud_btn.config(state=tk.DISABLED)
    
    def setup_devoluciones_frame(self):
        """Configura la pestaña de devoluciones"""
        # Marco para formulario de búsqueda
        self.devolucion_search_frame = ttk.Frame(self.devoluciones_frame, style="ContentFrame.TFrame")
        self.devolucion_search_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Título
        ttk.Label(
            self.devolucion_search_frame,
            text="Registrar Devolución de Préstamo",
            font=("Arial", 16, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(pady=(0, 15))
        
        # Formulario de búsqueda
        self.devolucion_form_frame = ttk.Frame(self.devolucion_search_frame, style="ContentFrame.TFrame")
        self.devolucion_form_frame.pack(fill=tk.X, padx=20)
        
        ttk.Label(
            self.devolucion_form_frame,
            text="ID de Préstamo:",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.id_prestamo_var = tk.StringVar()
        self.id_prestamo_entry = ttk.Entry(
            self.devolucion_form_frame,
            textvariable=self.id_prestamo_var,
            width=20
        )
        self.id_prestamo_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.buscar_prestamo_btn = ttk.Button(
            self.devolucion_form_frame,
            text="Buscar",
            command=self.buscar_prestamo,
            style="NormalButton.TButton"
        )
        self.buscar_prestamo_btn.grid(row=0, column=2, sticky=tk.W, pady=5, padx=15)
        
        # Marco para detalles del préstamo
        self.devolucion_details_frame = ttk.LabelFrame(
            self.devoluciones_frame,
            text="Detalles del Préstamo",
            style="ContentFrame.TFrame"
        )
        self.devolucion_details_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Texto para detalles
        self.detalles_prestamo_text = scrolledtext.ScrolledText(
            self.devolucion_details_frame,
            wrap=tk.WORD,
            width=50,
            height=10,
            font=("Arial", 11)
        )
        self.detalles_prestamo_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detalles_prestamo_text.config(state=tk.DISABLED)
        
        # Marco para acciones
        self.devolucion_actions_frame = ttk.Frame(self.devoluciones_frame, style="ContentFrame.TFrame")
        self.devolucion_actions_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.confirmar_devolucion_btn = ttk.Button(
            self.devolucion_actions_frame,
            text="Confirmar Devolución",
            command=self.confirmar_devolucion,
            style="SuccessButton.TButton"
        )
        self.confirmar_devolucion_btn.pack(side=tk.RIGHT, padx=5)
        
        # Deshabilitar botón inicialmente
        self.confirmar_devolucion_btn.config(state=tk.DISABLED)
    
    def setup_morosos_frame(self):
        """Configura la pestaña de estudiantes morosos"""
        # Panel superior con controles
        self.morosos_control_frame = ttk.Frame(self.morosos_frame, style="ContentFrame.TFrame")
        self.morosos_control_frame.pack(fill=tk.X, pady=(0, 10), padx=10)
        
        # Botón de actualizar
        self.actualizar_morosos_btn = ttk.Button(
            self.morosos_control_frame,
            text="Actualizar Lista",
            command=self.cargar_estudiantes_morosos,
            style="NormalButton.TButton"
        )
        self.actualizar_morosos_btn.pack(side=tk.RIGHT, padx=5)
        
        # Título
        ttk.Label(
            self.morosos_control_frame,
            text="Estudiantes con Morosidad",
            font=("Arial", 16, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(side=tk.LEFT, padx=5)
        
        # Lista de estudiantes morosos
        self.morosos_list_frame = ttk.Frame(self.morosos_frame, style="ContentFrame.TFrame")
        self.morosos_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear treeview para morosos
        self.morosos_treeview = ttk.Treeview(
            self.morosos_list_frame,
            columns=("id", "nombre", "dni", "correo"),
            show="headings",
            selectmode="browse"
        )
        
        # Definir encabezados
        self.morosos_treeview.heading("id", text="ID")
        self.morosos_treeview.heading("nombre", text="Nombre")
        self.morosos_treeview.heading("dni", text="DNI")
        self.morosos_treeview.heading("correo", text="Correo")
        
        # Configurar anchos de columnas
        self.morosos_treeview.column("id", width=50, anchor="center")
        self.morosos_treeview.column("nombre", width=200)
        self.morosos_treeview.column("dni", width=100, anchor="center")
        self.morosos_treeview.column("correo", width=250)
        
        # Scrollbar
        morosos_scrollbar = ttk.Scrollbar(
            self.morosos_list_frame,
            orient=tk.VERTICAL,
            command=self.morosos_treeview.yview
        )
        self.morosos_treeview.configure(yscrollcommand=morosos_scrollbar.set)
        
        # Empaquetar elementos
        self.morosos_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        morosos_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar evento de selección
        self.morosos_treeview.bind("<<TreeviewSelect>>", self.mostrar_detalles_moroso)
        
        # Panel inferior para detalles de préstamos vencidos
        self.morosos_details_frame = ttk.LabelFrame(
            self.morosos_frame,
            text="Préstamos Vencidos",
            style="ContentFrame.TFrame"
        )
        self.morosos_details_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # Contenido de detalles
        self.detalles_moroso_text = scrolledtext.ScrolledText(
            self.morosos_details_frame,
            wrap=tk.WORD,
            width=50,
            height=8,
            font=("Arial", 11)
        )
        self.detalles_moroso_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detalles_moroso_text.config(state=tk.DISABLED)
    
    def setup_estadisticas_frame(self):
        """Configura la pestaña de estadísticas"""
        # Título
        ttk.Label(
            self.estadisticas_frame,
            text="Estadísticas del Sistema",
            font=("Arial", 16, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        ).pack(pady=(10, 20), padx=10, anchor=tk.W)
        
        # Panel para estadísticas generales
        self.general_stats_frame = ttk.LabelFrame(
            self.estadisticas_frame,
            text="Estadísticas Generales",
            style="ContentFrame.TFrame"
        )
        self.general_stats_frame.pack(fill=tk.X, padx=10, pady=5, ipady=5)
        
        # Estadísticas en dos columnas
        self.stats_cols_frame = ttk.Frame(self.general_stats_frame, style="ContentFrame.TFrame")
        self.stats_cols_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)
        
        # Columna izquierda
        self.stats_left_frame = ttk.Frame(self.stats_cols_frame, style="ContentFrame.TFrame")
        self.stats_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Columna derecha
        self.stats_right_frame = ttk.Frame(self.stats_cols_frame, style="ContentFrame.TFrame")
        self.stats_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Estudiantes con más préstamos
        self.top_estudiantes_frame = ttk.LabelFrame(
            self.estadisticas_frame,
            text="Top Estudiantes con más Préstamos",
            style="ContentFrame.TFrame"
        )
        self.top_estudiantes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear treeview para top estudiantes
        self.top_estudiantes_treeview = ttk.Treeview(
            self.top_estudiantes_frame,
            columns=("nombre", "dni", "correo", "cantidad"),
            show="headings",
            selectmode="browse"
        )
        
        #