# Control/controlador_estudiante.py
from Persistencia.estudiante_dao import EstudianteDAO
from Persistencia.prestamo_dao import PrestamoDAO
from Entity.enumeraciones import EstadoPrestamo

class ControladorEstudiante:
    def __init__(self):
        self.estudiante_dao = EstudianteDAO()
        self.prestamo_dao = PrestamoDAO()
    
    def obtener_todos_estudiantes(self):
        return self.estudiante_dao.obtener_todos()
    
    def obtener_estudiante_por_dni(self, dni):
        return self.estudiante_dao.obtener_por_dni(dni)
    
    def registrar_estudiante(self, estudiante):
        return self.estudiante_dao.agregar(estudiante)
    
    def obtener_estudiante_prestamo(self, id_prestamo):
        prestamo = self.prestamo_dao.obtener_por_id(id_prestamo)
        if prestamo:
            return prestamo.solicitud.estudiante
        return None
    
    def consultar_morosidad(self, dni_estudiante):
        estudiante = self.estudiante_dao.obtener_por_dni(dni_estudiante)
        if not estudiante:
            return False
        
        prestamos = self.prestamo_dao.obtener_por_estudiante(estudiante.id)
        for prestamo in prestamos:
            if prestamo.estado == EstadoPrestamo.VENCIDO or prestamo.esta_vencido():
                return True
        
        return False
