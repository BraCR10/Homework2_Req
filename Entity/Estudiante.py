class Estudiante:
    def __init__(self, id, dni, correo, nombre):
        self.id = id
        self.dni = dni
        self.correo = correo
        self.nombre = nombre
    
    def __str__(self):
        return f"Estudiante {self.nombre} (DNI: {self.dni})"
