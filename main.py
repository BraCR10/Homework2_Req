# main.py
from Limite.limite_soporte import LimiteSoporte
from Limite.limite_estudiante import LimiteEstudiante

def main():
    while True:
        print("\n===== SISTEMA DE PRÉSTAMOS - SOPORTE TÉCNICO =====")
        print("1. Acceso como administrador de soporte")
        print("2. Acceso como estudiante")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            limite_soporte = LimiteSoporte()
            limite_soporte.menu_administrador_soporte()
        elif opcion == "2":
            limite_estudiante = LimiteEstudiante()
            limite_estudiante.menu_estudiante()
        elif opcion == "3":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    # Inicialización de datos de prueba para facilitar las demostraciones
    from Dominio.estudiante_dao import EstudianteDAO
    from Dominio.equipo_dao import EquipoDAO
    from Control.controlador_solicitud import ControladorSolicitud
    from Control.controlador_prestamo import ControladorPrestamo
    from Entity.enumeraciones import EstadoPrestamo
    
    # Crear algunos datos de prueba (solicitudes y préstamos)
    controlador_solicitud = ControladorSolicitud()
    controlador_prestamo = ControladorPrestamo()
    
    # Crear una solicitud para un estudiante
    solicitud1, _ = controlador_solicitud.hacer_solicitud("12345678", [1, 3])
    solicitud2, _ = controlador_solicitud.hacer_solicitud("23456789", [2])
    
    # Aprobar las solicitudes
    controlador_solicitud.aprobar_solicitud(solicitud1.id)
    controlador_solicitud.aprobar_solicitud(solicitud2.id)
    
    # Crear préstamos para las solicitudes aprobadas
    prestamo1, _ = controlador_prestamo.crear_prestamo(solicitud1)
    prestamo2, _ = controlador_prestamo.crear_prestamo(solicitud2)
    
    # Marcar un préstamo como vencido para pruebas de morosidad
    controlador_prestamo.actualizar_estado(prestamo1.id, EstadoPrestamo.VENCIDO)
    
    print("Datos de prueba cargados correctamente.")
    print("Hay 2 estudiantes con préstamos, uno de ellos con morosidad.")
    
    main()