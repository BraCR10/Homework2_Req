# Entity/solicitud.py
from datetime import datetime
from Entity.enumeraciones import EstadoSolicitud

class Solicitud:
    def __init__(self, id, estudiante, equipos_solicitados, fecha_solicitud=None):
        self.id = id
        self.estudiante = estudiante
        self.equipos_solicitados = equipos_solicitados  # Lista de objetos Equipo
        self.fecha_solicitud = fecha_solicitud or datetime.now()
        self.estado = EstadoSolicitud.PENDIENTE
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
    
    def __str__(self):
        return f"Solicitud #{self.id} - Estado: {self.estado.value} - Fecha: {self.fecha_solicitud.strftime('%d/%m/%Y')}"
