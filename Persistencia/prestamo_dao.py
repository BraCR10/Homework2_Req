# Persistencia/prestamo_dao.py
from bson.objectid import ObjectId
from datetime import datetime
from Persistencia.mongo_base import MongoDB
from Entity.Prestamo import Prestamo
from Entity.enumeraciones import EstadoPrestamo
from Persistencia.solicitud_dao import SolicitudDAO

class PrestamoDAO:
    def __init__(self):
        self.mongo = MongoDB()
        self.coleccion = self.mongo.get_collection('prestamos')
        self.solicitud_dao = SolicitudDAO()
        
        # Crear índices para mejorar rendimiento
        self.coleccion.create_index('id_solicitud')
        self.coleccion.create_index([('estado', 1), ('fecha_vencimiento', 1)])
    
    def obtener_todos(self):
        """Obtiene todos los préstamos de la base de datos"""
        prestamos_docs = self.coleccion.find()
        return [self._doc_a_entity(doc) for doc in prestamos_docs]
    
    def obtener_por_id(self, id):
        """Obtiene un préstamo por su ID"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        
        doc = self.coleccion.find_one({"_id": id})
        return self._doc_a_entity(doc) if doc else None
    
    def obtener_por_estudiante(self, id_estudiante):
        """Obtiene los préstamos de un estudiante específico"""
        # Primero obtenemos las solicitudes del estudiante
        solicitudes = self.solicitud_dao.obtener_por_estudiante(id_estudiante)
        ids_solicitudes = [solicitud.id for solicitud in solicitudes]
        
        # Convertir string IDs a ObjectIds si es necesario
        ids_solicitudes_obj = []
        for id_sol in ids_solicitudes:
            if isinstance(id_sol, str) and ObjectId.is_valid(id_sol):
                ids_solicitudes_obj.append(ObjectId(id_sol))
            else:
                ids_solicitudes_obj.append(id_sol)
        
        # Buscar préstamos por IDs de solicitudes
        prestamos_docs = self.coleccion.find({"id_solicitud": {"$in": ids_solicitudes_obj}})
        return [self._doc_a_entity(doc) for doc in prestamos_docs]
    
    def obtener_vencidos(self):
        """Obtiene los préstamos vencidos"""
        ahora = datetime.now()
        # Buscar préstamos activos con fecha de vencimiento anterior a la actual
        filtro = {
            "estado": EstadoPrestamo.ACTIVO.value,
            "fecha_vencimiento": {"$lt": ahora}
        }
        prestamos_docs = self.coleccion.find(filtro)
        return [self._doc_a_entity(doc) for doc in prestamos_docs]
    
    def agregar(self, prestamo):
        """Agrega un nuevo préstamo a la base de datos"""
        # Convertir la entidad a documento
        doc = self._entity_a_doc(prestamo)
        
        # Eliminar el _id si es None (MongoDB generará uno automáticamente)
        if '_id' in doc and doc['_id'] is None:
            del doc['_id']
        
        # Insertar en la colección
        resultado = self.coleccion.insert_one(doc)
        
        # Obtener el documento insertado
        nuevo_doc = self.coleccion.find_one({"_id": resultado.inserted_id})
        
        # Convertir de vuelta a entidad
        return self._doc_a_entity(nuevo_doc)
    
    def actualizar_estado(self, id_prestamo, nuevo_estado):
        """Actualiza el estado de un préstamo"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id_prestamo, str) and ObjectId.is_valid(id_prestamo):
            id_prestamo = ObjectId(id_prestamo)
        
        # Obtener el valor del estado (enum o string)
        if isinstance(nuevo_estado, EstadoPrestamo):
            valor_estado = nuevo_estado.value
        else:
            valor_estado = nuevo_estado
            
        resultado = self.coleccion.update_one(
            {"_id": id_prestamo},
            {"$set": {"estado": valor_estado}}
        )
        
        return resultado.matched_count > 0
    
    def finalizar_prestamo(self, id_prestamo):
        """Finaliza un préstamo registrando la fecha de devolución"""
        # Convertir string ID a ObjectId si es necesario
        if isinstance(id_prestamo, str) and ObjectId.is_valid(id_prestamo):
            id_prestamo = ObjectId(id_prestamo)
            
        fecha_actual = datetime.now()
        
        resultado = self.coleccion.update_one(
            {"_id": id_prestamo},
            {
                "$set": {
                    "estado": EstadoPrestamo.FINALIZADO.value,
                    "fecha_devolucion": fecha_actual
                }
            }
        )
        
        return resultado.matched_count > 0
    
    def _entity_a_doc(self, prestamo):
        """Convierte una entidad Prestamo a un documento MongoDB"""
        # Obtener ID de la solicitud
        id_solicitud = prestamo.solicitud.id if prestamo.solicitud else None
        if isinstance(id_solicitud, str) and ObjectId.is_valid(id_solicitud):
            id_solicitud = ObjectId(id_solicitud)
        
        # Crear documento
        return {
            "_id": prestamo.id,
            "id_solicitud": id_solicitud,
            "fecha_vencimiento": prestamo.fecha_vencimiento,
            "fecha_devolucion": prestamo.fecha_devolucion,
            "estado": prestamo.estado.value
        }
    
    def _doc_a_entity(self, doc):
        """Convierte un documento MongoDB a una entidad Prestamo"""
        if not doc:
            return None
        
        # Obtener solicitud
        solicitud = self.solicitud_dao.obtener_por_id(doc["id_solicitud"])
        
        # Crear entity
        prestamo = Prestamo(
            id=str(doc["_id"]),
            solicitud=solicitud,
            fecha_devolucion=doc.get("fecha_devolucion")
        )
        
        # Establecer valores adicionales
        prestamo.fecha_vencimiento = doc["fecha_vencimiento"]
        prestamo.estado = EstadoPrestamo(doc["estado"])
        
        return prestamo
