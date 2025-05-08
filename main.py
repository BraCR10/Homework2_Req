# main.py
from Limite.limite_inicio import LimiteInicio
from Persistencia.inicializador import inicializar_base_datos
from Persistencia.mongo_base import MongoDB
import os
import sys
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox

def main():
    """Función principal que inicia la aplicación"""
    # Cargar las variables de entorno
    load_dotenv()
    
    # Verificar las variables de entorno requeridas
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        mostrar_error_entorno()
        return
    
    # Inicializar la base de datos
    try:
        inicializar_base_datos(cargar_datos_prueba=True)
    except Exception as e:
        mostrar_error_bd(str(e))
        return
    
    # Iniciar la interfaz gráfica
    root = tk.Tk()
    app = LimiteInicio(root)
    
    # Configurar el cierre para cerrar la conexión a MongoDB
    root.protocol("WM_DELETE_WINDOW", lambda: cerrar_aplicacion(root))
    
    # Iniciar el bucle de la aplicación
    app.run()

def mostrar_error_entorno():
    """Muestra un error relacionado con las variables de entorno"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    messagebox.showerror(
        "Error de Configuración",
        "Variable de entorno MONGO_URI no encontrada.\n\n"
        "Por favor, crea un archivo .env con las variables requeridas.\n"
        "Puedes basarte en el archivo .env.example"
    )
    
    root.destroy()

def mostrar_error_bd(mensaje):
    """Muestra un error relacionado con la base de datos"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    messagebox.showerror(
        "Error de Base de Datos",
        f"Error al inicializar la base de datos:\n\n{mensaje}"
    )
    
    root.destroy()

def cerrar_aplicacion(root):
    """Cierra la aplicación y la conexión a MongoDB"""
    if messagebox.askokcancel("Salir", "¿Está seguro que desea salir de la aplicación?"):
        # Cerrar la conexión a MongoDB
        try:
            mongo = MongoDB()
            mongo.close_connection()
        except:
            pass
        
        # Destruir la ventana principal
        root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    main()