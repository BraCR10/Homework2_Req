# test_atlas_connection.py
"""
Script para verificar la conexión a MongoDB Atlas.
Ejecutar este script antes de ejecutar la aplicación para asegurarse
de que la conexión a MongoDB Atlas está configurada correctamente.
"""

from Persistencia.mongo_base import MongoDB
from dotenv import load_dotenv
import os

def verificar_atlas():
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener la URI para verificar si es Atlas
    mongo_uri = os.getenv("MONGO_URI", "")
    
    if not mongo_uri:
        print("ERROR: No se ha configurado la variable MONGO_URI en el archivo .env")
        print("Por favor, crea un archivo .env basado en .env.atlas y configura tus credenciales")
        return False
    
    if not "mongodb+srv://" in mongo_uri:
        print("ADVERTENCIA: No estás usando MongoDB Atlas (mongodb+srv://)")
        print(f"URI configurada: {mongo_uri}")
        respuesta = input("¿Deseas continuar de todos modos? (s/n): ")
        if respuesta.lower() != 's':
            return False
    
    try:
        # Intentar establecer conexión
        print("Intentando conectar a MongoDB...")
        mongo = MongoDB()
        
        # Probar operaciones básicas - listar colecciones
        db = mongo._db
        collections = db.list_collection_names()
        print(f"Colecciones en la base de datos: {collections}")
        
        # Verificar que podamos realizar operaciones CRUD
        test_collection = mongo.get_collection("test_connection")
        
        # Insertar un documento
        test_id = test_collection.insert_one({"test": "atlas_connection"}).inserted_id
        print(f"Documento insertado con ID: {test_id}")
        
        # Buscar el documento
        doc = test_collection.find_one({"_id": test_id})
        print(f"Documento recuperado: {doc}")
        
        # Eliminar el documento (limpieza)
        test_collection.delete_one({"_id": test_id})
        print("Documento eliminado")
        
        # Verificar que se eliminó
        count = test_collection.count_documents({})
        print(f"Documentos restantes en la colección de prueba: {count}")
        
        print("\n✅ Conexión a MongoDB Atlas exitosa!")
        print("La base de datos está correctamente configurada y operativa.")
        
        # Cerrar conexión
        mongo.close_connection()
        return True
        
    except Exception as e:
        print(f"\n❌ Error al conectar o realizar operaciones en MongoDB: {e}")
        print("\nPosibles soluciones:")
        print("1. Verifica que las credenciales en el archivo .env sean correctas")
        print("2. Comprueba que tu IP esté en la lista blanca de MongoDB Atlas")
        print("3. Asegúrate que el cluster de MongoDB Atlas esté activo")
        print("4. Verifica tu conexión a internet")
        return False

if __name__ == "__main__":
    verificar_atlas()
