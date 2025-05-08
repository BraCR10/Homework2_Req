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
    from Entity.Solicitud import Solicitud
    from Entity.Estudiante import Estudiante
    
    # Objetos DAO y controladores
    estudiante_dao = EstudianteDAO()
    equipo_dao = EquipoDAO()
    controlador_solicitud = ControladorSolicitud()
    controlador_prestamo = ControladorPrestamo()
    
    # Obtener estudiantes por DNI
    estudiante1 = estudiante_dao.obtener_por_dni("12345678")  # María Rodríguez
    estudiante2 = estudiante_dao.obtener_por_dni("23456789")  # Juan Pérez
    estudiante3 = estudiante_dao.obtener_por_dni("45678901")  # Carlos Martínez
    
    # Crear solicitudes iniciales
    solicitud1 = controlador_solicitud.solicitud_dao.agregar(
        Solicitud(None, estudiante1, [equipo_dao.obtener_por_id(1), equipo_dao.obtener_por_id(3)])
    )
    
    solicitud2 = controlador_solicitud.solicitud_dao.agregar(
        Solicitud(None, estudiante2, [equipo_dao.obtener_por_id(2)])
    )
    
    # Aprobar las solicitudes
    controlador_solicitud.aprobar_solicitud(solicitud1.id)
    controlador_solicitud.aprobar_solicitud(solicitud2.id)
    
    # Crear préstamos para las solicitudes aprobadas
    prestamo1, _ = controlador_prestamo.crear_prestamo(solicitud1)
    prestamo2, _ = controlador_prestamo.crear_prestamo(solicitud2)
    
    # Marcar un préstamo como vencido para pruebas de morosidad
    controlador_prestamo.actualizar_estado(prestamo1.id, EstadoPrestamo.VENCIDO)
    
    # Crear más solicitudes y préstamos para probar el caso de uso de estudiantes con más préstamos
    # El estudiante con DNI 12345678 (María Rodríguez) tendrá 6 préstamos en total
    equipos_disponibles = equipo_dao.obtener_disponibles()
    
    # Función auxiliar para crear solicitudes y préstamos
    def crear_solicitud_y_prestamo(estudiante, id_equipo):
        equipo = equipo_dao.obtener_por_id(id_equipo)
        if equipo and equipo.disponible:
            # Crear y guardar la solicitud
            solicitud = controlador_solicitud.solicitud_dao.agregar(
                Solicitud(None, estudiante, [equipo])
            )
            
            # Aprobar la solicitud
            exito, _ = controlador_solicitud.aprobar_solicitud(solicitud.id)
            
            if exito:
                # Crear el préstamo
                solicitud_actualizada = controlador_solicitud.solicitud_dao.obtener_por_id(solicitud.id)
                return controlador_prestamo.crear_prestamo(solicitud_actualizada)
        
        return None, "No se pudo crear la solicitud/préstamo"
    
    # Crear 5 préstamos adicionales para María (tendrá 6 en total)
    for i in range(5):
        id_equipo = (i % 4) + 5  # Usar equipos 5, 6, 7, 8, 5
        crear_solicitud_y_prestamo(estudiante1, id_equipo)
    
    # Crear 4 préstamos para Carlos
    for i in range(4):
        id_equipo = (i % 4) + 1  # Usar equipos 1, 2, 3, 4
        crear_solicitud_y_prestamo(estudiante3, id_equipo)
    
    print("Datos de prueba cargados correctamente.")
    print("Hay estudiantes con diferentes cantidades de préstamos:")
    print("- María Rodríguez: 6 préstamos (uno con morosidad)")
    print("- Carlos Martínez: 4 préstamos")
    print("- Juan Pérez: 1 préstamo")
    
    main()