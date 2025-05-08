# Dominio/solicitud_dao.py
from Entity.Solicitud import Solicitud
from Entity.enumeraciones import EstadoSolicitud
from datetime import datetime, timedelta

class SolicitudDAO:
    def __init__(self):
        self.solicitudes = []
        self.contador_id = 1
    
    def obtener_todas(self):
        return self.solicitudes
    
    def obtener_por_id(self, id):
        for solicitud in self.solicitudes:
            if solicitud.id == id:
                return solicitud
        return None
    
    def obtener_por_estudiante(self, id_estudiante):
        return [s for s in self.solicitudes if s.estudiante.id == id_estudiante]
    
    def agregar(self, solicitud):
        if not solicitud.id:
            solicitud.id = self.contador_id
            self.contador_id += 1
        self.solicitudes.append(solicitud)
        return solicitud
    
    def actualizar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self.obtener_por_id(id_solicitud)
        if solicitud:
            solicitud.cambiar_estado(nuevo_estado)
            return True
        return False