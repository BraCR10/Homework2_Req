
# Entity/prestamo.py
from datetime import datetime, timedelta
from Entity.enumeraciones import EstadoPrestamo

class Prestamo:
    def __init__(self, id, solicitud, fecha_devolucion=None):
        self.id = id
        self.solicitud = solicitud
        self.fecha_solicitud = solicitud.fecha_solicitud
        self.fecha_devolucion = fecha_devolucion
        self.estado = EstadoPrestamo.ACTIVO
        
        # Por defecto, establecemos una fecha de vencimiento de 7 días
        self.fecha_vencimiento = self.fecha_solicitud + timedelta(days=7)
    
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
    
    def esta_vencido(self):
        return datetime.now() > self.fecha_vencimiento and self.estado == EstadoPrestamo.ACTIVO
    
    def finalizar(self):
        self.estado = EstadoPrestamo.FINALIZADO
        self.fecha_devolucion = datetime.now()
    
    def __str__(self):
        estado_str = self.estado.value
        return f"Préstamo #{self.id} - Estado: {estado_str} - Inicio: {self.fecha_solicitud.strftime('%d/%m/%Y')}"