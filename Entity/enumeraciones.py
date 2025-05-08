from enum import Enum

class EstadoSolicitud(Enum):
    PENDIENTE = "Pendiente"
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado"

class EstadoPrestamo(Enum):
    ACTIVO = "Activo"
    FINALIZADO = "Finalizado"
    VENCIDO = "Vencido"
    BLOQUEADO = "Bloqueado"