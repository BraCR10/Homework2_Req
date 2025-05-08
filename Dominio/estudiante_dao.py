# Dominio/estudiante_dao.py
from Entity.Estudiante import Estudiante

class EstudianteDAO:
    def __init__(self):
        # Datos falsos para simular una base de datos
        self.estudiantes = [
            Estudiante(1, "12345678", "estudiante1@universidad.edu", "María Rodríguez"),
            Estudiante(2, "23456789", "estudiante2@universidad.edu", "Juan Pérez"),
            Estudiante(3, "34567890", "estudiante3@universidad.edu", "Ana González"),
            Estudiante(4, "45678901", "estudiante4@universidad.edu", "Carlos Martínez"),
            Estudiante(5, "56789012", "estudiante5@universidad.edu", "Laura Sánchez")
        ]
    
    def obtener_todos(self):
        return self.estudiantes
    
    def obtener_por_id(self, id):
        for estudiante in self.estudiantes:
            if estudiante.id == id:
                return estudiante
        return None
    
    def obtener_por_dni(self, dni):
        for estudiante in self.estudiantes:
            if estudiante.dni == dni:
                return estudiante
        return None
    
    def agregar(self, estudiante):
        # Simulamos un auto-incremento de ID
        if not estudiante.id:
            estudiante.id = max(e.id for e in self.estudiantes) + 1
        self.estudiantes.append(estudiante)
        return estudiante