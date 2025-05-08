# Persistencia/estudiante_dao.py
from bson.objectid import ObjectId
from Persistencia.mongo_base import MongoDB
from Entity.Estudiante import Estudiante

class EstudianteDAO:
    def __init__(self):
        self.mongo = MongoDB()
        self.coleccion = self.mongo.get_collection('estudiantes')
        
        # Crear índices para mejorar rendimiento
        self.coleccion.create_index('dni', unique=True)
    
    def obtener_todos(self):
        """Obtiene todos los estudiantes de la base de datos"""
        estudiantes_docs = self.coleccion.find()
        return [self._doc_a_entity(doc) for doc in estudiantes_docs]
    
    def obtener_por_id(self, id):
        """Obtiene un estudiante por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        
        doc = self.coleccion.find_one({"_id": id})
        return self._doc_a_entity(doc) if doc else None
    
    def obtener_por_dni(self, dni):
        """Obtiene un estudiante por su DNI"""
        doc = self.coleccion.find_one({"dni": dni})
        return self._doc_a_entity(doc) if doc else None
    
    def agregar(self, estudiante):
        """Agrega un nuevo estudiante a la base de datos"""
        # Convertir la entidad a documento
        doc = self._entity_a_doc(estudiante)
        
        # Eliminar el _id si es None (MongoDB generará uno automáticamente)
        if '_id' in doc and doc['_id'] is None:
            del doc['_id']
        
        # Insertar en la colección
        resultado = self.coleccion.insert_one(doc)
        
        # Obtener el documento insertado
        nuevo_doc = self.coleccion.find_one({"_id": resultado.inserted_id})
        
        # Convertir de vuelta a entidad
        return self._doc_a_entity(nuevo_doc)
    
    def actualizar(self, estudiante):
        """Actualiza un estudiante existente"""
        # Convertir la entidad a documento
        doc = self._entity_a_doc(estudiante)
        
        # Asegurar que id_busqueda sea un ObjectId válido
        id_busqueda = doc['_id']
        if isinstance(id_busqueda, str) and ObjectId.is_valid(id_busqueda):
            id_busqueda = ObjectId(id_busqueda)
        
        # Actualizar el documento en la colección
        self.coleccion.update_one(
            {"_id": id_busqueda},
            {"$set": {k: v for k, v in doc.items() if k != '_id'}}
        )
        
        # Obtener el documento actualizado
        doc_actualizado = self.coleccion.find_one({"_id": id_busqueda})
        
        # Convertir de vuelta a entidad
        return self._doc_a_entity(doc_actualizado)
    
    def eliminar(self, id):
        """Elimina un estudiante por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
            
        resultado = self.coleccion.delete_one({"_id": id})
        return resultado.deleted_count > 0
    
    def _entity_a_doc(self, estudiante):
        """Convierte una entidad Estudiante a un documento MongoDB"""
        return {
            "_id": estudiante.id,
            "dni": estudiante.dni,
            "correo": estudiante.correo,
            "nombre": estudiante.nombre
        }
    
    def _doc_a_entity(self, doc):
        """Convierte un documento MongoDB a una entidad Estudiante"""
        if not doc:
            return None
            
        return Estudiante(
            id=str(doc["_id"]),
            dni=doc["dni"],
            correo=doc["correo"],
            nombre=doc["nombre"]
        )
