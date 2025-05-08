# Control/controlador_prestamo.py
from Dominio.prestamo_dao import PrestamoDAO
from Dominio.solicitud_dao import SolicitudDAO
from Dominio.equipo_dao import EquipoDAO
from Entity.Prestamo import Prestamo
from Entity.enumeraciones import EstadoPrestamo, EstadoSolicitud
from datetime import datetime

class ControladorPrestamo:
    def __init__(self):
        self.prestamo_dao = PrestamoDAO()
        self.solicitud_dao = SolicitudDAO()
        self.equipo_dao = EquipoDAO()
    
    def crear_prestamo(self, solicitud):
        if solicitud.estado != EstadoSolicitud.APROBADO:
            return None, "La solicitud debe estar aprobada para crear un préstamo"
        
        nuevo_prestamo = Prestamo(None, solicitud)
        prestamo_guardado = self.prestamo_dao.agregar(nuevo_prestamo)
        
        return prestamo_guardado, "Préstamo creado exitosamente"
    
    def confirma_devolucion(self, id_prestamo):
        prestamo = self.prestamo_dao.obtener_por_id(id_prestamo)
        if not prestamo:
            return False, "Préstamo no encontrado"
        
        if prestamo.estado == EstadoPrestamo.FINALIZADO:
            return False, "El préstamo ya está finalizado"
        
        # Marcar el préstamo como finalizado
        self.prestamo_dao.finalizar_prestamo(id_prestamo)
        
        # Marcar los equipos como disponibles de nuevo
        for equipo in prestamo.solicitud.equipos_solicitados:
            self.equipo_dao.actualizar_disponibilidad(equipo.id, True)
        
        return True, "Préstamo finalizado correctamente"
    
    def actualizar_estado(self, id_prestamo, nuevo_estado):
        if not isinstance(nuevo_estado, EstadoPrestamo):
            return False, "Estado no válido"
            
        resultado = self.prestamo_dao.actualizar_estado(id_prestamo, nuevo_estado)
        if resultado:
            return True, f"Estado de préstamo cambiado a {nuevo_estado.value}"
        else:
            return False, "Préstamo no encontrado"
    
    def obtener_prestamos_vencidos(self):
        # Verificar los préstamos activos para ver si alguno está vencido
        prestamos_activos = [p for p in self.prestamo_dao.obtener_todos() if p.estado == EstadoPrestamo.ACTIVO]
        for prestamo in prestamos_activos:
            if prestamo.esta_vencido():
                self.prestamo_dao.actualizar_estado(prestamo.id, EstadoPrestamo.VENCIDO)
        
        # Devolver los préstamos vencidos
        return self.prestamo_dao.obtener_vencidos()
    
    def consultar_morosidades(self):
        prestamos_vencidos = self.obtener_prestamos_vencidos()
        estudiantes_morosos = []
        
        for prestamo in prestamos_vencidos:
            estudiante = prestamo.solicitud.estudiante
            if estudiante not in estudiantes_morosos:
                estudiantes_morosos.append(estudiante)
        
        return estudiantes_morosos