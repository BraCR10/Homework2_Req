# Persistencia/equipo_dao.py
from bson.objectid import ObjectId
from Persistencia.mongo_base import MongoDB
from Entity.Equipo import Equipo

class EquipoDAO:
    def __init__(self):
        self.mongo = MongoDB()
        self.coleccion = self.mongo.get_collection('equipos')
    
    def obtener_todos(self):
        """Obtiene todos los equipos de la base de datos"""
        equipos_docs = self.coleccion.find()
        return [self._doc_a_entity(doc) for doc in equipos_docs]
    
    def obtener_disponibles(self):
        """Obtiene todos los equipos disponibles"""
        equipos_docs = self.coleccion.find({"disponible": True})
        return [self._doc_a_entity(doc) for doc in equipos_docs]
    
    def obtener_por_id(self, id):
        """Obtiene un equipo por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        
        doc = self.coleccion.find_one({"_id": id})
        return self._doc_a_entity(doc) if doc else None
    
    def agregar(self, equipo):
        """Agrega un nuevo equipo a la base de datos"""
        # Convertir la entidad a documento
        doc = self._entity_a_doc(equipo)
        
        # Eliminar el _id si es None (MongoDB generará uno automáticamente)
        if '_id' in doc and doc['_id'] is None:
            del doc['_id']
        
        # Insertar en la colección
        resultado = self.coleccion.insert_one(doc)
        
        # Obtener el documento insertado
        nuevo_doc = self.coleccion.find_one({"_id": resultado.inserted_id})
        
        # Convertir de vuelta a entidad
        return self._doc_a_entity(nuevo_doc)
    
    def actualizar(self, equipo):
        """Actualiza un equipo existente"""
        # Convertir la entidad a documento
        doc = self._entity_a_doc(equipo)
        
        # Actualizar en la base de datos
        id_busqueda = doc['_id']
        if isinstance(id_busqueda, str) and ObjectId.is_valid(id_busqueda):
            id_busqueda = ObjectId(id_busqueda)
        
        self.coleccion.update_one(
            {"_id": id_busqueda},
            {"$set": {k: v for k, v in doc.items() if k != '_id'}}
        )
        
        # Obtener el documento actualizado
        doc_actualizado = self.coleccion.find_one({"_id": id_busqueda})
        
        # Convertir de vuelta a entidad
        return self._doc_a_entity(doc_actualizado)
    
    def actualizar_disponibilidad(self, id_equipo, disponible):
        """Actualiza la disponibilidad de un equipo"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id_equipo, str) and ObjectId.is_valid(id_equipo):
            id_equipo = ObjectId(id_equipo)
            
        resultado = self.coleccion.update_one(
            {"_id": id_equipo},
            {"$set": {"disponible": disponible}}
        )
        
        return resultado.matched_count > 0
    
    def eliminar(self, id):
        """Elimina un equipo por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
            
        resultado = self.coleccion.delete_one({"_id": id})
        return resultado.deleted_count > 0
    
    def _entity_a_doc(self, equipo):
        """Convierte una entidad Equipo a un documento MongoDB"""
        return {
            "_id": equipo.id,
            "tipo": equipo.tipo,
            "marca": equipo.marca,
            "modelo": equipo.modelo,
            "disponible": equipo.disponible
        }
    
    def _doc_a_entity(self, doc):
        """Convierte un documento MongoDB a una entidad Equipo"""
        if not doc:
            return None
            
        return Equipo(
            id=str(doc["_id"]),
            tipo=doc["tipo"],
            marca=doc["marca"],
            modelo=doc["modelo"],
            disponible=doc["disponible"]
        )
