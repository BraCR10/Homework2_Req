# main.py
from Limite.limite_soporte import LimiteSoporte
from Limite.limite_estudiante import LimiteEstudiante
from Persistencia.inicializador import inicializar_base_datos
from Persistencia.mongo_base import MongoDB
import os
from dotenv import load_dotenv

def main():
    # Cargar las variables de entorno
    load_dotenv()
    
    # Verificar las variables de entorno requeridas
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("Error: Variable de entorno MONGO_URI no encontrada")
        print("Por favor, crea un archivo .env con las variables requeridas")
        print("Puedes basarte en el archivo .env.example")
        return
    
    # Inicializar la base de datos
    try:
        inicializar_base_datos(cargar_datos_prueba=True)
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return
    
    # Bucle principal del programa
    try:
        while True:
            print("\n===== SISTEMA DE PRÉSTAMOS - SOPORTE TÉCNICO =====")
            print("1. Acceso como administrador de soporte")
            print("2. Acceso como estudiante")
            print("3. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                limite_soporte = LimiteSoporte()
                limite_soporte.menu_administrador_soporte()
            elif opcion == "2":
                limite_estudiante = LimiteEstudiante()
                limite_estudiante.menu_estudiante()
            elif opcion == "3":
                print("Gracias por usar el sistema. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
    finally:
        # Cerrar la conexión a MongoDB al finalizar
        mongo = MongoDB()
        mongo.close_connection()

if __name__ == "__main__":
    main()
