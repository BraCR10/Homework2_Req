# Limite/limite_soporte.py
from Control.controlador_solicitud import ControladorSolicitud
from Control.controlador_prestamo import ControladorPrestamo
from Control.controlador_estudiante import ControladorEstudiante
from Entity.enumeraciones import EstadoSolicitud, EstadoPrestamo

class LimiteSoporte:
    def __init__(self):
        self.controlador_solicitud = ControladorSolicitud()
        self.controlador_prestamo = ControladorPrestamo()
        self.controlador_estudiante = ControladorEstudiante()
    
    def menu_administrador_soporte(self):
        salir = False
        while not salir:
            print("\n===== SISTEMA DE SOPORTE TÉCNICO =====")
            print("1. Aprobar solicitud de préstamo")
            print("2. Registrar devolución de equipo")
            print("3. Consultar estudiantes morosos")
            print("4. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.menu_aprobar_solicitud()
            elif opcion == "2":
                self.menu_devolucion_prestamo()
            elif opcion == "3":
                self.consultar_morosidades()
            elif opcion == "4":
                print("Volviendo al menú principal...")
                salir = True
            else:
                print("Opción no válida. Intente de nuevo.")
    
    def menu_aprobar_solicitud(self):
        print("\n----- APROBAR SOLICITUD DE PRÉSTAMO -----")
        id_solicitud = input("Ingrese el ID de la solicitud: ")
        
        try:
            id_solicitud = int(id_solicitud)
        except ValueError:
            print("El ID debe ser un número entero.")
            return
        
        exito, mensaje = self.controlador_solicitud.aprobar_solicitud(id_solicitud)
        print(mensaje)
        
        if exito:
            # Si se aprobó la solicitud, crear el préstamo
            solicitud = self.controlador_solicitud.solicitud_dao.obtener_por_id(id_solicitud)
            prestamo, mensaje_prestamo = self.controlador_prestamo.crear_prestamo(solicitud)
            
            if prestamo:
                self.mostrar_prestamo(prestamo)
            else:
                print(mensaje_prestamo)
    
    def mostrar_prestamo(self, prestamo):
        print("\n----- DETALLES DEL PRÉSTAMO -----")
        print(f"ID: {prestamo.id}")
        print(f"Estado: {prestamo.estado.value}")
        print(f"Fecha de solicitud: {prestamo.fecha_solicitud.strftime('%d/%m/%Y')}")
        print(f"Fecha de vencimiento: {prestamo.fecha_vencimiento.strftime('%d/%m/%Y')}")
        
        estudiante = prestamo.solicitud.estudiante
        print(f"\nEstudiante: {estudiante.nombre}")
        print(f"DNI: {estudiante.dni}")
        print(f"Correo: {estudiante.correo}")
        
        print("\nEquipos prestados:")
        for equipo in prestamo.solicitud.equipos_solicitados:
            print(f"- {equipo.tipo} {equipo.marca} {equipo.modelo}")
    
    def menu_devolucion_prestamo(self):
        print("\n----- REGISTRAR DEVOLUCIÓN DE PRÉSTAMO -----")
        id_prestamo = input("Ingrese el ID del préstamo: ")
        
        try:
            id_prestamo = int(id_prestamo)
        except ValueError:
            print("El ID debe ser un número entero.")
            return
        
        exito, mensaje = self.controlador_prestamo.confirma_devolucion(id_prestamo)
        print(mensaje)
        
        if exito:
            self.mostrar_confirmacion_prestamo_devolucion()
    
    def mostrar_confirmacion_prestamo_devolucion(self):
        print("\n¡Devolución registrada correctamente!")
        print("Los equipos han sido marcados como disponibles.")
    
    def consultar_morosidades(self):
        print("\n----- ESTUDIANTES CON MOROSIDAD -----")
        estudiantes_morosos = self.controlador_prestamo.consultar_morosidades()
        
        if not estudiantes_morosos:
            print("No hay estudiantes con morosidad.")
            return
        
        self.mostrar_estudiantes(estudiantes_morosos)
    
    def mostrar_estudiantes(self, estudiantes):
        print("\nLista de estudiantes:")
        for i, estudiante in enumerate(estudiantes, 1):
            print(f"{i}. {estudiante.nombre} (DNI: {estudiante.dni}, Email: {estudiante.correo})")

