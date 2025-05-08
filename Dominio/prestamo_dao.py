# Dominio/prestamo_dao.py
from Entity.Prestamo import Prestamo
from Entity.enumeraciones import EstadoPrestamo
from datetime import datetime, timedelta

class PrestamoDAO:
    def __init__(self):
        self.prestamos = []
        self.contador_id = 1
    
    def obtener_todos(self):
        return self.prestamos
    
    def obtener_por_id(self, id):
        for prestamo in self.prestamos:
            if prestamo.id == id:
                return prestamo
        return None
    
    def obtener_por_estudiante(self, id_estudiante):
        return [p for p in self.prestamos if p.solicitud.estudiante.id == id_estudiante]
    
    def obtener_vencidos(self):
        ahora = datetime.now()
        return [p for p in self.prestamos if p.fecha_vencimiento < ahora and p.estado == EstadoPrestamo.ACTIVO]
    
    def agregar(self, prestamo):
        if not prestamo.id:
            prestamo.id = self.contador_id
            self.contador_id += 1
        self.prestamos.append(prestamo)
        return prestamo
    
    def actualizar_estado(self, id_prestamo, nuevo_estado):
        prestamo = self.obtener_por_id(id_prestamo)
        if prestamo:
            prestamo.actualizar_estado(nuevo_estado)
            return True
        return False
    
    def finalizar_prestamo(self, id_prestamo):
        prestamo = self.obtener_por_id(id_prestamo)
        if prestamo:
            prestamo.finalizar()
            return True