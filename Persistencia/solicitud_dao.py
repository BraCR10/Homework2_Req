# Persistencia/solicitud_dao.py
from bson.objectid import ObjectId
from datetime import datetime
from Persistencia.mongo_base import MongoDB
from Entity.Solicitud import Solicitud
from Entity.enumeraciones import EstadoSolicitud
from Persistencia.estudiante_dao import EstudianteDAO
from Persistencia.equipo_dao import EquipoDAO
import random

class SolicitudDAO:
    def __init__(self):
        self.mongo = MongoDB()
        self.coleccion = self.mongo.get_collection('solicitudes')
        self.estudiante_dao = EstudianteDAO()
        self.equipo_dao = EquipoDAO()
        self.contador_coleccion = self.mongo.get_collection('contadores')
        
        # Crear índices para mejorar rendimiento
        self.coleccion.create_index('id_estudiante')
        self.coleccion.create_index('numero_seguimiento', unique=True)
        
        # Inicializar contador de número de seguimiento si no existe
        if not self.contador_coleccion.find_one({"_id": "numero_seguimiento"}):
            self.contador_coleccion.insert_one({"_id": "numero_seguimiento", "valor": 100})
    
    def _obtener_siguiente_numero_seguimiento(self):
        """Obtiene el siguiente número de seguimiento disponible"""
        resultado = self.contador_coleccion.find_one_and_update(
            {"_id": "numero_seguimiento"},
            {"$inc": {"valor": 1}},
            return_document=True
        )
        return resultado["valor"]
    
    def obtener_todas(self):
        """Obtiene todas las solicitudes de la base de datos"""
        solicitudes_docs = self.coleccion.find()
        return [self._doc_a_entity(doc) for doc in solicitudes_docs]
    
    def obtener_por_id(self, id):
        """Obtiene una solicitud por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        
        doc = self.coleccion.find_one({"_id": id})
        return self._doc_a_entity(doc) if doc else None
    
    def obtener_por_numero_seguimiento(self, numero_seguimiento):
        """Obtiene una solicitud por su número de seguimiento"""
        try:
            numero_seguimiento = int(numero_seguimiento)
            doc = self.coleccion.find_one({"numero_seguimiento": numero_seguimiento})
            return self._doc_a_entity(doc) if doc else None
        except ValueError:
            return None
    
    def obtener_por_estudiante(self, id_estudiante):
        """Obtiene las solicitudes de un estudiante específico"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id_estudiante, str) and ObjectId.is_valid(id_estudiante):
            id_estudiante = ObjectId(id_estudiante)
            
        solicitudes_docs = self.coleccion.find({"id_estudiante": id_estudiante})
        return [self._doc_a_entity(doc) for doc in solicitudes_docs]
    
    def agregar(self, solicitud):
        """Agrega una nueva solicitud a la base de datos"""
        # Asignar un número de seguimiento si no tiene
        if not solicitud.numero_seguimiento:
            solicitud.numero_seguimiento = self._obtener_siguiente_numero_seguimiento()
        
        # Convertir la entidad a documento
        doc = self._entity_a_doc(solicitud)
        
        # Eliminar el _id si es None (MongoDB generará uno automáticamente)
        if '_id' in doc and doc['_id'] is None:
            del doc['_id']
        
        # Insertar en la colección
        resultado = self.coleccion.insert_one(doc)
        
        # Obtener el documento insertado
        nuevo_doc = self.coleccion.find_one({"_id": resultado.inserted_id})
        
        # Convertir de vuelta a entidad
        return self._doc_a_entity(nuevo_doc)
    
    def actualizar_estado(self, id_solicitud, nuevo_estado):
        """Actualiza el estado de una solicitud por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id_solicitud, str) and ObjectId.is_valid(id_solicitud):
            id_solicitud = ObjectId(id_solicitud)
        
        # Obtener el valor del estado (enum o string)
        if isinstance(nuevo_estado, EstadoSolicitud):
            valor_estado = nuevo_estado.value
        else:
            valor_estado = nuevo_estado
            
        resultado = self.coleccion.update_one(
            {"_id": id_solicitud},
            {"$set": {"estado": valor_estado}}
        )
        
        return resultado.matched_count > 0
    
    def actualizar_estado_por_numero_seguimiento(self, numero_seguimiento, nuevo_estado):
        """Actualiza el estado de una solicitud por su número de seguimiento"""
        try:
            numero_seguimiento = int(numero_seguimiento)
            
            # Obtener el valor del estado (enum o string)
            if isinstance(nuevo_estado, EstadoSolicitud):
                valor_estado = nuevo_estado.value
            else:
                valor_estado = nuevo_estado
                
            resultado = self.coleccion.update_one(
                {"numero_seguimiento": numero_seguimiento},
                {"$set": {"estado": valor_estado}}
            )
            
            return resultado.matched_count > 0
        except ValueError:
            return False
    
    def eliminar(self, id):
        """Elimina una solicitud por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
            
        resultado = self.coleccion.delete_one({"_id": id})
        return resultado.deleted_count > 0
    
    def _entity_a_doc(self, solicitud):
        """Convierte una entidad Solicitud a un documento MongoDB"""
        # Obtener IDs de equipos solicitados (si existen)
        ids_equipos = []
        if solicitud.equipos_solicitados:
            ids_equipos = [equipo.id for equipo in solicitud.equipos_solicitados]
            # Convertir a ObjectId si son string válidos
            ids_equipos = [
                ObjectId(id) if isinstance(id, str) and ObjectId.is_valid(id) else id 
                for id in ids_equipos if id is not None
            ]
        
        # Obtener ID del estudiante
        id_estudiante = solicitud.estudiante.id if solicitud.estudiante else None
        if isinstance(id_estudiante, str) and ObjectId.is_valid(id_estudiante):
            id_estudiante = ObjectId(id_estudiante)
        
        # Crear documento
        return {
            "_id": solicitud.id,
            "id_estudiante": id_estudiante,
            "ids_equipos": ids_equipos,
            "fecha_solicitud": solicitud.fecha_solicitud,
            "estado": solicitud.estado.value,
            "numero_seguimiento": solicitud.numero_seguimiento
        }
    
    def _doc_a_entity(self, doc):
        """Convierte un documento MongoDB a una entidad Solicitud"""
        if not doc:
            return None
        
        # Obtener estudiante
        estudiante = self.estudiante_dao.obtener_por_id(doc["id_estudiante"])
        
        # Obtener equipos
        equipos = []
        for id_equipo in doc.get("ids_equipos", []):
            equipo = self.equipo_dao.obtener_por_id(id_equipo)
            if equipo:
                equipos.append(equipo)
        
        # Crear entity
        solicitud = Solicitud(
            id=str(doc["_id"]),
            estudiante=estudiante,
            equipos_solicitados=equipos,
            fecha_solicitud=doc["fecha_solicitud"],
            numero_seguimiento=doc.get("numero_seguimiento")
        )
        
        # Establecer estado
        solicitud.estado = EstadoSolicitud(doc["estado"])
        
        return solicitud