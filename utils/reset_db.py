# reset_db.py
"""
Script para resetear la base de datos MongoDB.
Útil durante el desarrollo o para reiniciar el sistema.
"""

from Persistencia.mongo_base import MongoDB
from Persistencia.inicializador import inicializar_base_datos
from dotenv import load_dotenv
import sys

def resetear_base_datos(forzar=False):
    """Elimina todas las colecciones y vuelve a inicializar la base de datos"""
    # Cargar variables de entorno
    load_dotenv()
    
    # Instancia de MongoDB
    try:
        mongo = MongoDB()
    except Exception as e:
        print(f"No se pudo conectar a MongoDB: {e}")
        return
    
    try:
        # Colecciones a borrar
        colecciones = ["estudiantes", "equipos", "solicitudes", "prestamos", "contadores"]
        
        # Confirmación
        if not forzar:
            print("¡ADVERTENCIA! Esta operación eliminará todos los datos existentes.")
            confirmacion = input("¿Está seguro que desea continuar? (s/n): ")
            
            if confirmacion.lower() != 's':
                print("Operación cancelada.")
                return
        
        # Eliminar datos de cada colección
        for coleccion in colecciones:
            col = mongo.get_collection(coleccion)
            col.delete_many({})
            print(f"Colección '{coleccion}' vaciada.")
        
        # Inicializar datos de prueba
        inicializar_base_datos(cargar_datos_prueba=True)
        
        print("Base de datos restablecida exitosamente.")
    
    except Exception as e:
        print(f"Error al resetear la base de datos: {e}")
    
    finally:
        # Cerrar la conexión
        mongo.close_connection()

if __name__ == "__main__":
    forzar = False
    if len(sys.argv) > 1 and sys.argv[1] == "--forzar":
        forzar = True
    resetear_base_datos(forzar=forzar)
