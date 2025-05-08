# Persistencia/mongo_base.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import sys

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales desde variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB_NAME", "sistema_prestamos")

class MongoDB:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            try:
                # Verificar si tenemos la URI configurada
                if not MONGO_URI:
                    raise Exception("La variable de entorno MONGO_URI no está configurada. Por favor, revisa el archivo .env")
                
                # Parámetros de conexión para mejor rendimiento y compatibilidad con Atlas
                cls._client = MongoClient(
                    MONGO_URI, 
                    retryWrites=True,
                    w="majority",
                    connectTimeoutMS=30000,
                    socketTimeoutMS=None,
                    serverSelectionTimeoutMS=30000
                )
                cls._db = cls._client[MONGO_DB]
                
                # Verificar conexión
                cls._client.server_info()
                print(f"Conectado a MongoDB: {MONGO_DB}")
                print(f"Usando: {'MongoDB Atlas' if 'mongodb+srv://' in MONGO_URI else 'MongoDB Local'}")
            except Exception as e:
                print(f"Error al conectar a MongoDB: {e}")
                print("Asegúrate de tener MongoDB instalado o configura correctamente el archivo .env")
                print("Si estás usando MongoDB Atlas, verifica que:")
                print("- Tu IP esté en la lista blanca")
                print("- El usuario y contraseña sean correctos")
                print("- El cluster esté activo")
                sys.exit(1)
        return cls._instance
    
    def get_collection(self, collection_name):
        """Obtiene una colección específica"""
        return self._db[collection_name]
    
    def close_connection(self):
        """Cierra la conexión a MongoDB"""
        if self._client:
            self._client.close()
            MongoDB._instance = None
            MongoDB._client = None
            MongoDB._db = None
            print("Conexión a MongoDB cerrada")