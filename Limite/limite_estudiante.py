
# Limite/limite_estudiante.py
from Control.controlador_solicitud import ControladorSolicitud
from Control.controlador_estudiante import ControladorEstudiante
from Dominio.equipo_dao import EquipoDAO
from Entity.Solicitud import Solicitud
from Entity.Estudiante import Estudiante

class LimiteEstudiante:
    def __init__(self):
        self.controlador_solicitud = ControladorSolicitud()
        self.controlador_estudiante = ControladorEstudiante()
        self.equipo_dao = EquipoDAO()
    
    def menu_estudiante(self):
        salir = False
        while not salir:
            print("\n===== SISTEMA DE PRÉSTAMOS - ESTUDIANTE =====")
            print("1. Solicitar préstamo de equipo")
            print("2. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.hacer_solicitud()
            elif opcion == "2":
                print("Volviendo al menú principal...")
                salir = True
            else:
                print("Opción no válida. Intente de nuevo.")
    
    def hacer_solicitud(self):
        print("\n----- SOLICITUD DE PRÉSTAMO -----")
        
        # Solicitar DNI al momento de hacer la solicitud
        dni_estudiante = input("Ingrese su DNI: ")
        
        # Verificar si el estudiante existe
        estudiante = self.controlador_estudiante.obtener_estudiante_por_dni(dni_estudiante)
        
        if not estudiante:
            # Si el estudiante no existe, solicitamos información básica y lo agregamos
            print("DNI no registrado. Registrando nuevo estudiante...")
            nombre = input("Ingrese su nombre completo: ")
            correo = input("Ingrese su correo electrónico: ")
            
            # Crear nuevo estudiante usando el controlador
            nuevo_estudiante = Estudiante(None, dni_estudiante, correo, nombre)
            estudiante = self.controlador_estudiante.registrar_estudiante(nuevo_estudiante)
            print(f"¡Estudiante registrado exitosamente!")
        
        print(f"Bienvenido/a, {estudiante.nombre}!")
        
        # Verificar morosidad del estudiante
        if self.controlador_estudiante.consultar_morosidad(dni_estudiante):
            print("No puede realizar solicitudes debido a que tiene préstamos vencidos.")
            return
        
        # Mostrar equipos disponibles
        equipos_disponibles = self.equipo_dao.obtener_disponibles()
        if not equipos_disponibles:
            print("No hay equipos disponibles en este momento.")
            return
        
        print("\nEquipos disponibles:")
        for i, equipo in enumerate(equipos_disponibles, 1):
            print(f"{i}. {equipo.tipo} {equipo.marca} {equipo.modelo}")
        
        # Seleccionar equipos
        seleccion = input("\nSeleccione los números de equipos separados por comas (ej: 1,3,5): ")
        indices_seleccionados = []
        
        try:
            indices_seleccionados = [int(i.strip()) for i in seleccion.split(",")]
            if not indices_seleccionados:  # Verificamos si la lista está vacía
                print("Debe seleccionar al menos un equipo.")
                return
        except ValueError:
            print("Entrada no válida. Debe ingresar números separados por comas.")
            return
        
        # Verificar índices válidos
        if any(i < 1 or i > len(equipos_disponibles) for i in indices_seleccionados):
            print("Uno o más índices están fuera de rango.")
            return
        
        # Obtener IDs de equipos seleccionados
        ids_equipos_solicitados = [equipos_disponibles[i-1].id for i in indices_seleccionados]
        
        # Usar el objeto estudiante directamente en lugar de buscar por DNI nuevamente
        solicitud = self.controlador_solicitud.solicitud_dao.agregar(
            Solicitud(None, estudiante, [self.equipo_dao.obtener_por_id(id_eq) for id_eq in ids_equipos_solicitados])
        )
        
        if solicitud:
            print("Solicitud creada exitosamente")
            self.mostrar_confirmacion_solicitud(solicitud.id)
        else:
            print("Error al crear la solicitud")
    
    def mostrar_confirmacion_solicitud(self, id_solicitud):
        print(f"\n¡Solicitud #{id_solicitud} creada exitosamente!")
        print("La solicitud está pendiente de aprobación por parte del personal de soporte.")
        print("Por favor, espere a que su solicitud sea procesada.")