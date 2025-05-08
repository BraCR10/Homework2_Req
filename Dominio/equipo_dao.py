
# Dominio/equipo_dao.py
from Entity.Equipo import Equipo

class EquipoDAO:
    def __init__(self):
        # Datos falsos para simular una base de datos
        self.equipos = [
            Equipo(1, "Laptop", "Dell", "Latitude 7420", True),
            Equipo(2, "Laptop", "HP", "Probook 450", True),
            Equipo(3, "Tablet", "Samsung", "Galaxy Tab S7", True),
            Equipo(4, "Disco Duro", "Western Digital", "2TB USB 3.0", True),
            Equipo(5, "Software", "Microsoft", "Office 365", True),
            Equipo(6, "Laptop", "Lenovo", "ThinkPad X1", True),
            Equipo(7, "Tablet", "Apple", "iPad Pro", True),
            Equipo(8, "Disco Duro", "Seagate", "4TB USB 3.0", True)
        ]
    
    def obtener_todos(self):
        return self.equipos
    
    def obtener_disponibles(self):
        return [equipo for equipo in self.equipos if equipo.disponible]
    
    def obtener_por_id(self, id):
        for equipo in self.equipos:
            if equipo.id == id:
                return equipo
        return None
    
    def actualizar_disponibilidad(self, id_equipo, disponible):
        equipo = self.obtener_por_id(id_equipo)
        if equipo:
            equipo.disponible = disponible
            return True
        return False
