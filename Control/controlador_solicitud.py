# Control/controlador_solicitud.py
from Dominio.solicitud_dao import SolicitudDAO
from Dominio.equipo_dao import EquipoDAO
from Dominio.estudiante_dao import EstudianteDAO
from Entity.Solicitud import Solicitud
from Entity.enumeraciones import EstadoSolicitud

class ControladorSolicitud:
    def __init__(self):
        self.solicitud_dao = SolicitudDAO()
        self.equipo_dao = EquipoDAO()
        self.estudiante_dao = EstudianteDAO()
    
    def hacer_solicitud(self, dni_estudiante, ids_equipos_solicitados):
        estudiante = self.estudiante_dao.obtener_por_dni(dni_estudiante)
        if not estudiante:
            return None, "Estudiante no encontrado"
        
        equipos_solicitados = []
        for id_equipo in ids_equipos_solicitados:
            equipo = self.equipo_dao.obtener_por_id(id_equipo)
            if not equipo:
                return None, f"Equipo con ID {id_equipo} no encontrado"
            if not equipo.disponible:
                return None, f"Equipo {equipo.tipo} {equipo.marca} no está disponible"
            equipos_solicitados.append(equipo)
        
        nueva_solicitud = Solicitud(None, estudiante, equipos_solicitados)
        solicitud_guardada = self.solicitud_dao.agregar(nueva_solicitud)
        
        return solicitud_guardada, "Solicitud creada exitosamente"
    
    def añadir_solicitud(self, dni_estudiante, ids_equipos_solicitados):
        # Aseguramos que este método solo llame a hacer_solicitud para mantener la consistencia
        return self.hacer_solicitud(dni_estudiante, ids_equipos_solicitados)
    
    def aprobar_solicitud(self, id_solicitud):
        solicitud = self.solicitud_dao.obtener_por_id(id_solicitud)
        if not solicitud:
            return False, "Solicitud no encontrada"
        
        if solicitud.estado != EstadoSolicitud.PENDIENTE:
            return False, f"La solicitud ya fue {solicitud.estado.value.lower()}"
        
        # Marcar los equipos como no disponibles
        for equipo in solicitud.equipos_solicitados:
            self.equipo_dao.actualizar_disponibilidad(equipo.id, False)
        
        # Cambiar el estado de la solicitud
        self.solicitud_dao.actualizar_estado(id_solicitud, EstadoSolicitud.APROBADO)
        
        return True, "Solicitud aprobada exitosamente"
    
    def cambiar_estado(self, id_solicitud, nuevo_estado):
        if not isinstance(nuevo_estado, EstadoSolicitud):
            return False, "Estado no válido"
            
        resultado = self.solicitud_dao.actualizar_estado(id_solicitud, nuevo_estado)
        if resultado:
            return True, f"Estado de solicitud cambiado a {nuevo_estado.value}"
        else:
            return False, "Solicitud no encontrada"
