# Sistema de Préstamos - Iformacion Generas

## Descripción General
El Sistema de Préstamos Soporte de Computacion es una aplicación para gestionar el préstamo de equipos electrónicos a estudiantes. Permite a los estudiantes solicitar préstamos y a los usuarios de soporte técnico aprobar solicitudes, registrar devoluciones y consultar morosidades.

## Requisitos
- Python 3.x
- MongoDB (local o Atlas)
- Paquetes: pymongo, python-dotenv, Pillow

## Configuración Inicial
1. Clonar o descargar el repositorio
2. Crear un archivo `.env` basado en `.env_example` usando el usuario para prueba:
   ```
    MONGO_URI=mongodb+srv://App:Apppass1234@clusterdbhomework.nqbu0ho.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDBHomework
   MONGO_DB_NAME=sistema_prestamos
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución
Para iniciar la aplicación:
```
python main.py
```

## Módulos Principales

### Menú Principal
Desde aquí se puede acceder a las interfaces de Estudiante o Soporte Técnico.

### Acceso para Estudiantes
Permite a los estudiantes:

1. **Solicitar Préstamo**:
   - Ingresar DNI para identificarse
   - Si es nuevo usuario, registrarse en el sistema
   - Seleccionar equipos disponibles
   - Confirmar la solicitud

2. **Consultar Solicitudes**:
   - Ver histórico de solicitudes realizadas
   - Consultar estado (Pendiente, Aprobado, Rechazado)

### Acceso para Soporte Técnico
Permite al personal de soporte:

1. **Aprobar Solicitudes**:
   - Ver solicitudes pendientes
   - Aprobar o rechazar solicitudes

2. **Registrar Devolución**:
   - Buscar préstamo por número de seguimiento
   - Confirmar la devolución del equipo

3. **Consultar Estudiantes Morosos**:
   - Ver lista de estudiantes con préstamos vencidos

4. **Consultar Estudiantes con N Préstamos**:
   - Buscar estudiantes según cantidad de préstamos realizados

5. **Ver Historial de Solicitudes**:
   - Consultar todas las solicitudes realizadas

## Reglas del Sistema
- Los préstamos tienen un plazo de 7 días
- Los estudiantes con morosidad no pueden solicitar nuevos préstamos
- Cada solicitud recibe un número de seguimiento único
- Los equipos prestados no están disponibles para nuevas solicitudes

## Utilidades
En la carpeta `utils` se incluyen scripts para:
- Resetear la base de datos (`reset_db.py`)
- Generar reportes del sistema (`reporte_db.py`)
- Verificar conexión con MongoDB Atlas (`test_atlas.py`)

## Estructura del Proyecto
El sistema sigue un patrón arquitectónico por capas:
- **Entity**: Clases de dominio (Estudiante, Equipo, Solicitud, Préstamo)
- **Control**: Lógica de negocio
- **Limite**: Interfaces de usuario
- **Persistencia**: Acceso a datos (MongoDB)