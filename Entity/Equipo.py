class Equipo:
    def __init__(self, id, tipo, marca, modelo, disponible=True):
        self.id = id
        self.tipo = tipo  # laptop, tablet, disco duro, etc.
        self.marca = marca
        self.modelo = modelo
        self.disponible = disponible
    
    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.tipo} {self.marca} {self.modelo} - {estado}"
