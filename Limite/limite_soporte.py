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
            ("Consultar estudiantes con N préstamos", self.mostrar_n_prestamos),
            ("Ver historial de solicitudes", self.mostrar_historial_solicitudes)
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
                            background="#e0e0e0",
                            foreground="black")
        
        self.style.map("NormalButton.TButton",
                      background=[('active', "#c0c0c0")],
                      foreground=[('active', 'black')])
        
        # Botones de acción principal
        self.style.configure("AccentButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_PRIMARY,
                            foreground="black")
        
        self.style.map("AccentButton.TButton",
                      background=[('active', self.COLOR_SECONDARY)],
                      foreground=[('active', 'black')])
        
        # Botón de éxito (verde)
        self.style.configure("SuccessButton.TButton", 
                            font=("Arial", 12),
                            background=self.COLOR_SUCCESS,
                            foreground="black")
        
        self.style.map("SuccessButton.TButton",
                      background=[('active', "#2E7D32")],
                      foreground=[('active', 'black')])
        
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
                            foreground="black")
        
        self.style.map("DangerButton.TButton",
                      background=[('active', "#D32F2F")],
                      foreground=[('active', 'black')])
    
    def limpiar_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_aprobar_solicitud(self):
        self.limpiar_content_frame()
        
        # Botones de acción
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(pady=10)
        aprobar_btn = ttk.Button(action_frame, text="Aprobar", style="SuccessButton.TButton", state=tk.DISABLED)
        rechazar_btn = ttk.Button(action_frame, text="Rechazar", style="DangerButton.TButton", state=tk.DISABLED)
        aprobar_btn.pack(side=tk.LEFT, padx=10)
        rechazar_btn.pack(side=tk.LEFT, padx=10)
        # Título
        ttk.Label(self.content_frame, text="Solicitudes pendientes de aprobación", font=("Arial", 16, "bold")).pack(pady=(10, 10))
        # Treeview para solicitudes
        columns = ("seguimiento", "estudiante", "dni", "fecha", "equipos")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("seguimiento", text="N° Seguimiento")
        tree.heading("estudiante", text="Estudiante")
        tree.heading("dni", text="DNI")
        tree.heading("fecha", text="Fecha")
        tree.heading("equipos", text="Equipos")
        tree.column("seguimiento", width=120, anchor="center")
        tree.column("estudiante", width=180)
        tree.column("dni", width=100, anchor="center")
        tree.column("fecha", width=120, anchor="center")
        tree.column("equipos", width=300)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Cargar solicitudes pendientes
        solicitudes = [s for s in self.controlador_solicitud.solicitud_dao.obtener_todas() if s.estado.value == "Pendiente"]
        for s in solicitudes:
            equipos_str = ", ".join([f"{e.tipo} {e.marca}" for e in s.equipos_solicitados])
            tree.insert("", "end", iid=s.numero_seguimiento, values=(s.numero_seguimiento, s.estudiante.nombre, s.estudiante.dni, s.fecha_solicitud.strftime('%d/%m/%Y'), equipos_str))
    
        # Funciones de aprobar/rechazar
        def aprobar():
            selected = tree.selection()
            if not selected:
                return
            num = tree.item(selected[0], "values")[0]
            ok, msg = self.controlador_solicitud.aprobar_solicitud(num)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.mostrar_aprobar_solicitud()
            else:
                messagebox.showerror("Error", msg)
        def rechazar():
            selected = tree.selection()
            if not selected:
                return
            num = tree.item(selected[0], "values")[0]
            ok, msg = self.controlador_solicitud.cambiar_estado(num, EstadoSolicitud.RECHAZADO)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.mostrar_aprobar_solicitud()
            else:
                messagebox.showerror("Error", msg)
        aprobar_btn.config(command=aprobar)
        rechazar_btn.config(command=rechazar)
        # Habilitar botones al seleccionar
        def on_select(event):
            selected = tree.selection()
            if selected:
                aprobar_btn.config(state=tk.NORMAL)
                rechazar_btn.config(state=tk.NORMAL)
            else:
                aprobar_btn.config(state=tk.DISABLED)
                rechazar_btn.config(state=tk.DISABLED)
        tree.bind("<<TreeviewSelect>>", on_select)
        
    
    def mostrar_registrar_devolucion(self):
        self.limpiar_content_frame()
        ttk.Label(self.content_frame, text="Registrar devolución de equipo", font=("Arial", 16, "bold")).pack(pady=(10, 10))
        buscar_frame = ttk.Frame(self.content_frame)
        buscar_frame.pack(pady=10)
        ttk.Label(buscar_frame, text="N° de seguimiento:", font=("Arial", 12)).pack(side=tk.LEFT)
        seguimiento_var = tk.StringVar()
        entry = ttk.Entry(buscar_frame, textvariable=seguimiento_var, width=20)
        entry.pack(side=tk.LEFT, padx=5)
        resultado_frame = ttk.Frame(self.content_frame)
        resultado_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        detalles_label = ttk.Label(resultado_frame, text="", font=("Arial", 12))
        detalles_label.pack(pady=10)
        devolver_btn = ttk.Button(resultado_frame, text="Registrar devolución", style="SuccessButton.TButton", state=tk.DISABLED)
        devolver_btn.pack(pady=5)
        def buscar():
            num = seguimiento_var.get().strip()
            solicitud = self.controlador_solicitud.solicitud_dao.obtener_por_numero_seguimiento(num)
            if not solicitud:
                detalles_label.config(text="No se encontró ninguna solicitud con ese número.")
                devolver_btn.config(state=tk.DISABLED)
                return
            equipos_str = ", ".join([f"{e.tipo} {e.marca}" for e in solicitud.equipos_solicitados])
            detalles = f"Estudiante: {solicitud.estudiante.nombre}\nDNI: {solicitud.estudiante.dni}\nFecha: {solicitud.fecha_solicitud.strftime('%d/%m/%Y')}\nEquipos: {equipos_str}\nEstado: {solicitud.estado.value}"
            detalles_label.config(text=detalles)
            if solicitud.estado.value == "Aprobado":
                devolver_btn.config(state=tk.NORMAL)
            else:
                devolver_btn.config(state=tk.DISABLED)
        def registrar_devolucion():
            num = seguimiento_var.get().strip()
            solicitud = self.controlador_solicitud.solicitud_dao.obtener_por_numero_seguimiento(num)
            if not solicitud:
                messagebox.showerror("Error", "No se encontró la solicitud.")
                return
            prestamos = self.controlador_prestamo.prestamo_dao.obtener_por_estudiante(solicitud.estudiante.id)
            prestamo = next((p for p in prestamos if p.solicitud.numero_seguimiento == int(num)), None)
            if not prestamo:
                # Si la solicitud está aprobada, crear el préstamo automáticamente
                if solicitud.estado.value == "Aprobado":
                    prestamo, msg = self.controlador_prestamo.crear_prestamo(solicitud)
                    if not prestamo:
                        messagebox.showerror("Error", msg)
                        return
                else:
                    messagebox.showerror("Error", "No se encontró el préstamo asociado.")
                    return
            ok, msg = self.controlador_prestamo.confirma_devolucion(prestamo.id)
            if ok:
                messagebox.showinfo("Éxito", msg)
                detalles_label.config(text="")
                devolver_btn.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", msg)
        buscar_btn = ttk.Button(buscar_frame, text="Buscar", command=buscar, style="AccentButton.TButton")
        buscar_btn.pack(side=tk.LEFT, padx=5)
        devolver_btn.config(command=registrar_devolucion)
    
    def mostrar_morosos(self):
        self.limpiar_content_frame()
        ttk.Label(self.content_frame, text="Estudiantes morosos", font=("Arial", 16, "bold")).pack(pady=(10, 10))
        columns = ("nombre", "dni", "correo", "fecha_vencimiento")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("nombre", text="Nombre")
        tree.heading("dni", text="DNI")
        tree.heading("correo", text="Correo")
        tree.heading("fecha_vencimiento", text="Fecha de vencimiento")
        tree.column("nombre", width=180)
        tree.column("dni", width=100, anchor="center")
        tree.column("correo", width=200)
        tree.column("fecha_vencimiento", width=150, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Cargar morosos
        morosos = self.controlador_prestamo.consultar_morosidades()
        for est in morosos:
            prestamos = self.controlador_prestamo.obtener_prestamos_vencidos_por_estudiante(est.id)
            if prestamos:
                fecha_venc = prestamos[0].fecha_vencimiento.strftime('%d/%m/%Y')
            else:
                fecha_venc = "-"
            tree.insert("", "end", iid=est.dni, values=(est.nombre, est.dni, est.correo, fecha_venc))
        # Mostrar detalles al seleccionar
        detalles_label = ttk.Label(self.content_frame, text="", font=("Arial", 12))
        detalles_label.pack(pady=10)
        def on_select(event):
            selected = tree.selection()
            if not selected:
                detalles_label.config(text="")
                return
            dni = tree.item(selected[0], "values")[1]
            estudiante = self.controlador_estudiante.obtener_estudiante_por_dni(dni)
            prestamos = self.controlador_prestamo.obtener_prestamos_vencidos_por_estudiante(estudiante.id)
            detalles = f"Préstamos vencidos: {len(prestamos)}\n"
            for p in prestamos:
                detalles += f"- Solicitud #{p.solicitud.numero_seguimiento} | Equipo(s): {', '.join([e.tipo for e in p.solicitud.equipos_solicitados])} | Vencimiento: {p.fecha_vencimiento.strftime('%d/%m/%Y')}\n"
            detalles_label.config(text=detalles)
        tree.bind("<<TreeviewSelect>>", on_select)
    
    def mostrar_n_prestamos(self):
        self.limpiar_content_frame()
        ttk.Label(self.content_frame, text="Consultar estudiantes con N préstamos", font=("Arial", 16, "bold")).pack(pady=(10, 10))
        buscar_frame = ttk.Frame(self.content_frame)
        buscar_frame.pack(pady=10)
        ttk.Label(buscar_frame, text="N (mínimo de préstamos):", font=("Arial", 12)).pack(side=tk.LEFT)
        n_var = tk.StringVar()
        entry = ttk.Entry(buscar_frame, textvariable=n_var, width=10)
        entry.pack(side=tk.LEFT, padx=5)
        resultado_frame = ttk.Frame(self.content_frame)
        resultado_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        columns = ("nombre", "dni", "correo", "cantidad")
        tree = ttk.Treeview(resultado_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("nombre", text="Nombre")
        tree.heading("dni", text="DNI")
        tree.heading("correo", text="Correo")
        tree.heading("cantidad", text="Cantidad")
        tree.column("nombre", width=180)
        tree.column("dni", width=100, anchor="center")
        tree.column("correo", width=200)
        tree.column("cantidad", width=100, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(resultado_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        def buscar():
            n = n_var.get().strip()
            if not n.isdigit() or int(n) < 1:
                messagebox.showerror("Error", "Ingrese un número válido mayor a 0")
                return
            n = int(n)
            tree.delete(*tree.get_children())
            estudiantes = self.controlador_estudiante.obtener_todos_estudiantes()
            for est in estudiantes:
                prestamos = self.controlador_prestamo.prestamo_dao.obtener_por_estudiante(est.id)
                if len(prestamos) >= n:
                    tree.insert("", "end", iid=est.dni, values=(est.nombre, est.dni, est.correo, len(prestamos)))
        buscar_btn = ttk.Button(buscar_frame, text="Buscar", command=buscar, style="AccentButton.TButton")
        buscar_btn.pack(side=tk.LEFT, padx=5)
    
    def mostrar_historial_solicitudes(self):
        self.limpiar_content_frame()
        ttk.Label(self.content_frame, text="Historial de todas las solicitudes", font=("Arial", 16, "bold")).pack(pady=(10, 10))
        columns = ("seguimiento", "estudiante", "dni", "fecha", "estado", "equipos")
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("seguimiento", text="N° Seguimiento")
        tree.heading("estudiante", text="Estudiante")
        tree.heading("dni", text="DNI")
        tree.heading("fecha", text="Fecha")
        tree.heading("estado", text="Estado")
        tree.heading("equipos", text="Equipos")
        tree.column("seguimiento", width=120, anchor="center")
        tree.column("estudiante", width=180)
        tree.column("dni", width=100, anchor="center")
        tree.column("fecha", width=120, anchor="center")
        tree.column("estado", width=100, anchor="center")
        tree.column("equipos", width=300)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        solicitudes = self.controlador_solicitud.solicitud_dao.obtener_todas()
        solicitudes = sorted(solicitudes, key=lambda s: s.fecha_solicitud, reverse=True)
        for s in solicitudes:
            equipos_str = ", ".join([f"{e.tipo} {e.marca}" for e in s.equipos_solicitados])
            tree.insert("", "end", iid=s.numero_seguimiento, values=(s.numero_seguimiento, s.estudiante.nombre, s.estudiante.dni, s.fecha_solicitud.strftime('%d/%m/%Y'), s.estado.value, equipos_str))
    
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