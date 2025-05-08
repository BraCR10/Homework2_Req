# Limite/limite_inicio.py
import tkinter as tk
from tkinter import ttk, messagebox, font
import re
from Limite.limite_estudiante import LimiteEstudiante
from Limite.limite_soporte import LimiteSoporte
from PIL import Image, ImageTk

class LimiteInicio:
    def __init__(self, root=None):
        # Colores
        self.COLOR_PRIMARY = "#4a6fa5"  # Azul oscuro
        self.COLOR_SECONDARY = "#6d98e3"  # Azul medio
        self.COLOR_ACCENT = "#2d4a72"  # Azul más oscuro
        self.COLOR_BACKGROUND = "#f5f5f5"  # Gris muy claro
        self.COLOR_TEXT = "#333333"  # Casi negro
        
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.root.title("Sistema de Préstamos - TEC")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.root.configure(bg=self.COLOR_BACKGROUND)
        
        # Centrar la ventana
        self.center_window()
        
        # Crear estilos personalizados
        self.setup_styles()
        
        # Crear el marco principal
        self.main_frame = ttk.Frame(self.root, style="MainFrame.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título y logo
        self.header_frame = ttk.Frame(self.main_frame, style="MainFrame.TFrame")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo (placeholder)
        self.logo_label = ttk.Label(
            self.header_frame, 
            text="TEC", 
            font=("Arial", 36, "bold"),
            foreground=self.COLOR_PRIMARY,
            background=self.COLOR_BACKGROUND
        )
        self.logo_label.pack(side=tk.LEFT, padx=10)
        
        # Título principal
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Sistema de Préstamos de Equipos",
            font=("Arial", 24, "bold"),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        )
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # Contenedor para las opciones
        self.content_frame = ttk.Frame(self.main_frame, style="ContentFrame.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Dividir en dos columnas
        self.left_frame = ttk.Frame(self.content_frame, style="ContentFrame.TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.right_frame = ttk.Frame(self.content_frame, style="ContentFrame.TFrame")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Opción para estudiantes
        self.student_frame = ttk.Frame(self.left_frame, style="OptionFrame.TFrame")
        self.student_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.student_title = ttk.Label(
            self.student_frame, 
            text="Acceso para Estudiantes",
            font=("Arial", 18, "bold"),
            foreground=self.COLOR_PRIMARY,
            background=self.COLOR_BACKGROUND
        )
        self.student_title.pack(pady=(20, 10))
        
        self.student_description = ttk.Label(
            self.student_frame, 
            text="Solicita préstamos de equipos\ny consulta el estado de tus solicitudes",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND,
            justify=tk.CENTER
        )
        self.student_description.pack(pady=(0, 20))
        
        self.student_button = ttk.Button(
            self.student_frame, 
            text="Ingresar como Estudiante",
            command=self.open_student_panel,
            style="AccentButton.TButton"
        )
        self.student_button.pack(pady=10)
        
        # Opción para soporte técnico
        self.support_frame = ttk.Frame(self.right_frame, style="OptionFrame.TFrame")
        self.support_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.support_title = ttk.Label(
            self.support_frame, 
            text="Acceso para Soporte Técnico",
            font=("Arial", 18, "bold"),
            foreground=self.COLOR_PRIMARY,
            background=self.COLOR_BACKGROUND
        )
        self.support_title.pack(pady=(20, 10))
        
        self.support_description = ttk.Label(
            self.support_frame, 
            text="Gestiona solicitudes, préstamos\ny consulta estadísticas del sistema",
            font=("Arial", 12),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND,
            justify=tk.CENTER
        )
        self.support_description.pack(pady=(0, 20))
        
        self.support_button = ttk.Button(
            self.support_frame, 
            text="Ingresar como Soporte Técnico",
            command=self.open_support_panel,
            style="AccentButton.TButton"
        )
        self.support_button.pack(pady=10)
        
        # Footer con información
        self.footer_frame = ttk.Frame(self.main_frame, style="MainFrame.TFrame")
        self.footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.footer_label = ttk.Label(
            self.footer_frame, 
            text="© 2025 Instituto Tecnológico de Costa Rica - Sistema de Préstamos",
            font=("Arial", 10),
            foreground=self.COLOR_TEXT,
            background=self.COLOR_BACKGROUND
        )
        self.footer_label.pack(side=tk.LEFT)
        
        # Botón de salir
        self.exit_button = ttk.Button(
            self.footer_frame, 
            text="Salir",
            command=self.exit_application,
            style="DangerButton.TButton"
        )
        self.exit_button.pack(side=tk.RIGHT)
    
    def setup_styles(self):
        """Configura los estilos personalizados de los widgets"""
        self.style = ttk.Style()
        self.style.configure("MainFrame.TFrame", background=self.COLOR_BACKGROUND)
        self.style.configure("ContentFrame.TFrame", background=self.COLOR_BACKGROUND)
        self.style.configure("OptionFrame.TFrame", background=self.COLOR_BACKGROUND,
                             relief="groove", borderwidth=2)
        
        # Botones
        self.style.configure("AccentButton.TButton", 
                            font=("Arial", 12, "bold"),
                            background=self.COLOR_PRIMARY,
                            foreground="black")
        
        self.style.map("AccentButton.TButton",
                      background=[('active', self.COLOR_SECONDARY)],
                      foreground=[('active', 'black')])
        
        self.style.configure("DangerButton.TButton", 
                            font=("Arial", 10),
                            background="#d9534f",
                            foreground="black")
        
        self.style.map("DangerButton.TButton",
                      background=[('active', "#c9302c")],
                      foreground=[('active', 'black')])
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def open_student_panel(self):
        """Abre el panel de estudiantes"""
        self.root.withdraw()  # Ocultar ventana principal
        student_window = tk.Toplevel(self.root)
        student_window.protocol("WM_DELETE_WINDOW", lambda: self.close_panel(student_window))
        limite_estudiante = LimiteEstudiante(student_window)
    
    def open_support_panel(self):
        """Abre el panel de soporte técnico"""
        self.root.withdraw()  # Ocultar ventana principal
        support_window = tk.Toplevel(self.root)
        support_window.protocol("WM_DELETE_WINDOW", lambda: self.close_panel(support_window))
        limite_soporte = LimiteSoporte(support_window)
    
    def close_panel(self, panel_window):
        """Cierra un panel y muestra de nuevo la ventana principal"""
        panel_window.destroy()
        self.root.deiconify()  # Mostrar ventana principal de nuevo
    
    def exit_application(self):
        """Cierra la aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir de la aplicación?"):
            self.root.destroy()
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    # Para pruebas
    app = LimiteInicio()
    app.run()