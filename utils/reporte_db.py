# generar_reporte.py
"""
Script para generar un informe sobre el estado de la base de datos MongoDB.
Este script puede ser útil para diagnóstico o para presentaciones.
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Persistencia.mongo_base import MongoDB
from Persistencia.estudiante_dao import EstudianteDAO
from Persistencia.equipo_dao import EquipoDAO
from Persistencia.solicitud_dao import SolicitudDAO
from Persistencia.prestamo_dao import PrestamoDAO
from Entity.enumeraciones import EstadoPrestamo, EstadoSolicitud
from datetime import datetime
import os
from dotenv import load_dotenv
import json

def generar_reporte():
    """Genera un informe detallado sobre el estado de la base de datos"""
    # Cargar variables de entorno
    load_dotenv()
    
    print("Generando reporte del sistema de préstamos...")
    print("-" * 50)
    
    # Conexión a MongoDB
    mongo = MongoDB()
    
    try:
        # Instanciar DAOs
        estudiante_dao = EstudianteDAO()
        equipo_dao = EquipoDAO()
        solicitud_dao = SolicitudDAO()
        prestamo_dao = PrestamoDAO()
        
        # Información de la conexión
        mongo_uri = os.getenv("MONGO_URI", "")
        es_atlas = "mongodb+srv://" in mongo_uri
        db_name = os.getenv("MONGO_DB_NAME", "sistema_prestamos")
        
        print(f"Tipo de conexión: {'MongoDB Atlas (Cloud)' if es_atlas else 'MongoDB Local'}")
        print(f"Base de datos: {db_name}")
        print(f"Fecha del reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # Estadísticas generales
        estudiantes = estudiante_dao.obtener_todos()
        equipos = equipo_dao.obtener_todos()
        solicitudes = solicitud_dao.obtener_todas()
        prestamos = prestamo_dao.obtener_todos()
        
        print("ESTADÍSTICAS GENERALES:")
        print(f"Total de estudiantes: {len(estudiantes)}")
        print(f"Total de equipos: {len(equipos)}")
        print(f"Total de solicitudes: {len(solicitudes)}")
        print(f"Total de préstamos: {len(prestamos)}")
        print("-" * 50)
        
        # Estadísticas de equipos
        equipos_disponibles = [e for e in equipos if e.disponible]
        print("ESTADÍSTICAS DE EQUIPOS:")
        print(f"Equipos disponibles: {len(equipos_disponibles)} ({round(len(equipos_disponibles)/len(equipos)*100, 2)}%)")
        print(f"Equipos prestados: {len(equipos) - len(equipos_disponibles)} ({round((len(equipos) - len(equipos_disponibles))/len(equipos)*100, 2)}%)")
        
        # Tipos de equipos
        tipos_equipos = {}
        for equipo in equipos:
            tipo = equipo.tipo
            if tipo in tipos_equipos:
                tipos_equipos[tipo] += 1
            else:
                tipos_equipos[tipo] = 1
        
        print("\nDISTRIBUCIÓN POR TIPO DE EQUIPO:")
        for tipo, cantidad in tipos_equipos.items():
            print(f"- {tipo}: {cantidad} ({round(cantidad/len(equipos)*100, 2)}%)")
        print("-" * 50)
        
        # Estadísticas de solicitudes
        estados_solicitudes = {}
        for solicitud in solicitudes:
            estado = solicitud.estado.value
            if estado in estados_solicitudes:
                estados_solicitudes[estado] += 1
            else:
                estados_solicitudes[estado] = 1
        
        print("ESTADÍSTICAS DE SOLICITUDES:")
        for estado, cantidad in estados_solicitudes.items():
            print(f"- {estado}: {cantidad} ({round(cantidad/len(solicitudes)*100, 2)}%)")
        print("-" * 50)
        
        # Estadísticas de préstamos
        estados_prestamos = {}
        for prestamo in prestamos:
            estado = prestamo.estado.value
            if estado in estados_prestamos:
                estados_prestamos[estado] += 1
            else:
                estados_prestamos[estado] = 1
        
        print("ESTADÍSTICAS DE PRÉSTAMOS:")
        for estado, cantidad in estados_prestamos.items():
            print(f"- {estado}: {cantidad} ({round(cantidad/len(prestamos)*100, 2)}%)")
        
        # Préstamos por estudiante
        prestamos_por_estudiante = {}
        for prestamo in prestamos:
            id_estudiante = prestamo.solicitud.estudiante.id
            nombre_estudiante = prestamo.solicitud.estudiante.nombre
            if id_estudiante in prestamos_por_estudiante:
                prestamos_por_estudiante[id_estudiante]["cantidad"] += 1
            else:
                prestamos_por_estudiante[id_estudiante] = {
                    "nombre": nombre_estudiante,
                    "cantidad": 1
                }
        
        print("\nTOP 3 ESTUDIANTES CON MÁS PRÉSTAMOS:")
        estudiantes_ordenados = sorted(
            prestamos_por_estudiante.items(), 
            key=lambda x: x[1]["cantidad"], 
            reverse=True
        )
        
        for i, (id_est, datos) in enumerate(estudiantes_ordenados[:3], 1):
            print(f"{i}. {datos['nombre']}: {datos['cantidad']} préstamos")
        
        print("-" * 50)
        
        # Guardar reporte en archivo
        nombre_archivo = f"Reportes/reporte_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("REPORTE DEL SISTEMA DE PRÉSTAMOS\n")
            f.write("-" * 50 + "\n")
            f.write(f"Tipo de conexión: {'MongoDB Atlas (Cloud)' if es_atlas else 'MongoDB Local'}\n")
            f.write(f"Base de datos: {db_name}\n")
            f.write(f"Fecha del reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n")
            f.write("ESTADÍSTICAS GENERALES:\n")
            f.write(f"Total de estudiantes: {len(estudiantes)}\n")
            f.write(f"Total de equipos: {len(equipos)}\n")
            f.write(f"Total de solicitudes: {len(solicitudes)}\n")
            f.write(f"Total de préstamos: {len(prestamos)}\n")
            # Añadir resto del reporte...
        
        print(f"Reporte guardado en el archivo: {nombre_archivo}")
        
    except Exception as e:
        print(f"Error al generar el reporte: {e}")
    finally:
        # Cerrar la conexión
        mongo.close_connection()

if __name__ == "__main__":
    generar_reporte()
