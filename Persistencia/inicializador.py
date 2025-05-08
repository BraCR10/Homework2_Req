# Persistencia/inicializador.py
from Persistencia.mongo_base import MongoDB
from Entity.enumeraciones import EstadoSolicitud, EstadoPrestamo
from datetime import datetime, timedelta
from bson.objectid import ObjectId

def inicializar_base_datos(cargar_datos_prueba=True):
    """
    Inicializa la base de datos MongoDB.
    Opcionalmente carga datos de prueba.
    """
    print("Inicializando base de datos MongoDB...")
    
    # Conexión a MongoDB
    mongo = MongoDB()
    
    # Obtener colecciones
    coleccion_estudiantes = mongo.get_collection('estudiantes')
    coleccion_equipos = mongo.get_collection('equipos')
    coleccion_solicitudes = mongo.get_collection('solicitudes')
    coleccion_prestamos = mongo.get_collection('prestamos')
    coleccion_contadores = mongo.get_collection('contadores')
    
    # Crear índices para mejorar rendimiento
    coleccion_estudiantes.create_index('dni', unique=True)
    coleccion_solicitudes.create_index('id_estudiante')
    coleccion_solicitudes.create_index('numero_seguimiento', unique=True)
    coleccion_prestamos.create_index('id_solicitud')
    coleccion_prestamos.create_index([('estado', 1), ('fecha_vencimiento', 1)])
    
    print("Índices creados correctamente")
    
    # Cargar datos de prueba si se solicita
    if cargar_datos_prueba:
        # Verificar si ya existen datos
        if coleccion_estudiantes.count_documents({}) > 0:
            print("Ya existen datos en la base de datos")
            return
        
        print("Cargando datos de prueba...")
        _cargar_datos_de_prueba(mongo)
        print("Datos de prueba cargados correctamente")

def _cargar_datos_de_prueba(mongo):
    """
    Carga datos de prueba en MongoDB
    """
    # Obtener colecciones
    coleccion_estudiantes = mongo.get_collection('estudiantes')
    coleccion_equipos = mongo.get_collection('equipos')
    coleccion_solicitudes = mongo.get_collection('solicitudes')
    coleccion_prestamos = mongo.get_collection('prestamos')
    coleccion_contadores = mongo.get_collection('contadores')
    
    # Inicializar contador de número de seguimiento
    coleccion_contadores.insert_one({"_id": "numero_seguimiento", "valor": 100})
    
    # Agregar estudiantes
    estudiantes_docs = [
        {
            "dni": "12345678",
            "correo": "estudiante1@universidad.edu",
            "nombre": "María Rodríguez"
        },
        {
            "dni": "23456789",
            "correo": "estudiante2@universidad.edu",
            "nombre": "Juan Pérez"
        },
        {
            "dni": "34567890",
            "correo": "estudiante3@universidad.edu",
            "nombre": "Ana González"
        },
        {
            "dni": "45678901",
            "correo": "estudiante4@universidad.edu",
            "nombre": "Carlos Martínez"
        },
        {
            "dni": "56789012",
            "correo": "estudiante5@universidad.edu",
            "nombre": "Laura Sánchez"
        }
    ]
    
    resultado_estudiantes = coleccion_estudiantes.insert_many(estudiantes_docs)
    ids_estudiantes = resultado_estudiantes.inserted_ids
    
    # Crear mapeo de DNI a _id
    estudiantes_por_dni = {}
    for i, estudiante in enumerate(estudiantes_docs):
        estudiantes_por_dni[estudiante['dni']] = ids_estudiantes[i]
    
    # Agregar equipos
    equipos_docs = [
        {
            "tipo": "Laptop",
            "marca": "Dell",
            "modelo": "Latitude 7420",
            "disponible": True
        },
        {
            "tipo": "Laptop",
            "marca": "HP",
            "modelo": "Probook 450",
            "disponible": True
        },
        {
            "tipo": "Tablet",
            "marca": "Samsung",
            "modelo": "Galaxy Tab S7",
            "disponible": True
        },
        {
            "tipo": "Disco Duro",
            "marca": "Western Digital",
            "modelo": "2TB USB 3.0",
            "disponible": True
        },
        {
            "tipo": "Software",
            "marca": "Microsoft",
            "modelo": "Office 365",
            "disponible": True
        },
        {
            "tipo": "Laptop",
            "marca": "Lenovo",
            "modelo": "ThinkPad X1",
            "disponible": True
        },
        {
            "tipo": "Tablet",
            "marca": "Apple",
            "modelo": "iPad Pro",
            "disponible": True
        },
        {
            "tipo": "Disco Duro",
            "marca": "Seagate",
            "modelo": "4TB USB 3.0",
            "disponible": True
        }
    ]
    
    resultado_equipos = coleccion_equipos.insert_many(equipos_docs)
    ids_equipos = resultado_equipos.inserted_ids
    
    # Crear solicitudes y préstamos
    # Solicitud 1: María solicita laptop Dell y tablet Samsung (morosidad)
    solicitud1 = {
        "id_estudiante": estudiantes_por_dni["12345678"],
        "ids_equipos": [ids_equipos[0], ids_equipos[2]],
        "fecha_solicitud": datetime.now() - timedelta(days=15),
        "estado": EstadoSolicitud.APROBADO.value,
        "numero_seguimiento": 101
    }
    resultado_solicitud1 = coleccion_solicitudes.insert_one(solicitud1)
    id_solicitud1 = resultado_solicitud1.inserted_id
    # Préstamo 1 (vencido): Para la solicitud 1
    prestamo1 = {
        "id_solicitud": id_solicitud1,
        "fecha_vencimiento": datetime.now() - timedelta(days=7),
        "fecha_devolucion": None,
        "estado": EstadoPrestamo.VENCIDO.value
    }
    coleccion_prestamos.insert_one(prestamo1)

    # Solicitud 2: Carlos solicita disco duro (morosidad)
    solicitud2 = {
        "id_estudiante": estudiantes_por_dni["45678901"],
        "ids_equipos": [ids_equipos[3]],
        "fecha_solicitud": datetime.now() - timedelta(days=12),
        "estado": EstadoSolicitud.APROBADO.value,
        "numero_seguimiento": 102
    }
    resultado_solicitud2 = coleccion_solicitudes.insert_one(solicitud2)
    id_solicitud2 = resultado_solicitud2.inserted_id
    # Préstamo 2 (vencido): Para la solicitud 2
    prestamo2 = {
        "id_solicitud": id_solicitud2,
        "fecha_vencimiento": datetime.now() - timedelta(days=5),
        "fecha_devolucion": None,
        "estado": EstadoPrestamo.VENCIDO.value
    }
    coleccion_prestamos.insert_one(prestamo2)

    # Solicitud 3: Juan solicita laptop HP (activo)
    solicitud3 = {
        "id_estudiante": estudiantes_por_dni["23456789"],
        "ids_equipos": [ids_equipos[1]],
        "fecha_solicitud": datetime.now(),
        "estado": EstadoSolicitud.APROBADO.value,
        "numero_seguimiento": 103
    }
    resultado_solicitud3 = coleccion_solicitudes.insert_one(solicitud3)
    id_solicitud3 = resultado_solicitud3.inserted_id
    # Préstamo 3 (activo): Para la solicitud 3
    prestamo3 = {
        "id_solicitud": id_solicitud3,
        "fecha_vencimiento": datetime.now() + timedelta(days=7),
        "fecha_devolucion": None,
        "estado": EstadoPrestamo.ACTIVO.value
    }
    coleccion_prestamos.insert_one(prestamo3)
    
    # Crear más solicitudes y préstamos para María (tendrá 6 en total incluyendo el anterior)
    numero_seguimiento = 104
    
    for i in range(5):
        id_equipo = ids_equipos[(i % 4) + 3]  # Usar equipos 4, 5, 6, 7, 8
        
        solicitud = {
            "id_estudiante": estudiantes_por_dni["12345678"],  # María Rodríguez
            "ids_equipos": [id_equipo],
            "fecha_solicitud": datetime.now(),
            "estado": EstadoSolicitud.APROBADO.value,
            "numero_seguimiento": numero_seguimiento
        }
        
        numero_seguimiento += 1
        
        resultado_solicitud = coleccion_solicitudes.insert_one(solicitud)
        id_solicitud = resultado_solicitud.inserted_id
        
        prestamo = {
            "id_solicitud": id_solicitud,
            "fecha_vencimiento": datetime.now() + timedelta(days=7),
            "fecha_devolucion": None,
            "estado": EstadoPrestamo.ACTIVO.value
        }
        
        coleccion_prestamos.insert_one(prestamo)
    
    # Crear 4 préstamos para Carlos
    for i in range(4):
        id_equipo = ids_equipos[(i % 4)]  # Usar equipos 1, 2, 3, 4
        
        solicitud = {
            "id_estudiante": estudiantes_por_dni["45678901"],  # Carlos Martínez
            "ids_equipos": [id_equipo],
            "fecha_solicitud": datetime.now(),
            "estado": EstadoSolicitud.APROBADO.value,
            "numero_seguimiento": numero_seguimiento
        }
        
        numero_seguimiento += 1
        
        resultado_solicitud = coleccion_solicitudes.insert_one(solicitud)
        id_solicitud = resultado_solicitud.inserted_id
        
        prestamo = {
            "id_solicitud": id_solicitud,
            "fecha_vencimiento": datetime.now() + timedelta(days=7),
            "fecha_devolucion": None,
            "estado": EstadoPrestamo.ACTIVO.value
        }
        
        coleccion_prestamos.insert_one(prestamo)
        
    # Crear solicitudes pendientes para demostración
    solicitud_pendiente1 = {
        "id_estudiante": estudiantes_por_dni["34567890"],  # Ana González
        "ids_equipos": [ids_equipos[5]],  # Lenovo ThinkPad
        "fecha_solicitud": datetime.now(),
        "estado": EstadoSolicitud.PENDIENTE.value,
        "numero_seguimiento": numero_seguimiento
    }
    
    numero_seguimiento += 1
    coleccion_solicitudes.insert_one(solicitud_pendiente1)
    
    solicitud_pendiente2 = {
        "id_estudiante": estudiantes_por_dni["56789012"],  # Laura Sánchez
        "ids_equipos": [ids_equipos[6], ids_equipos[7]],  # iPad Pro y Disco Duro Seagate
        "fecha_solicitud": datetime.now(),
        "estado": EstadoSolicitud.PENDIENTE.value,
        "numero_seguimiento": numero_seguimiento
    }
    
    coleccion_solicitudes.insert_one(solicitud_pendiente2)
    
    # Actualizar el contador para que esté sincronizado con los datos cargados
    coleccion_contadores.update_one(
        {"_id": "numero_seguimiento"},
        {"$set": {"valor": numero_seguimiento}}
    )