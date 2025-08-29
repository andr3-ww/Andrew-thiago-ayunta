import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='1234',
            ssl_disabled=True
        )
        if connection.is_connected():
            print('Conexión exitosa a MySQL')
            return connection
    except Error as e:
        print(f'Error al conectar a MySQL: {e}')
        return None

def create_database_and_tables(connection):
    try:
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS hotel_sheldon")
        cursor.execute("USE hotel_sheldon")

        # Crear tablas
        # Tabla de tipos de habitaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_habitacion (
                id_tipo INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                descripcion TEXT,
                precio_por_noche DECIMAL(10, 2) NOT NULL,
                capacidad INT NOT NULL
            )
        """)

        # Tabla de habitaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
                numero VARCHAR(10) NOT NULL,
                id_tipo INT NOT NULL,
                piso INT NOT NULL,
                estado ENUM('disponible', 'ocupada', 'mantenimiento') DEFAULT 'disponible',
                FOREIGN KEY (id_tipo) REFERENCES tipos_habitacion(id_tipo)
            )
        """)

        # Tabla de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                telefono VARCHAR(20) NOT NULL,
                direccion TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabla de servicios adicionales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                descripcion TEXT,
                precio DECIMAL(10, 2) NOT NULL
            )
        """)

        # Tabla de reservas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id_reserva INT AUTO_INCREMENT PRIMARY KEY,
                id_cliente INT NOT NULL,
                id_habitacion INT NOT NULL,
                fecha_ingreso DATETIME NOT NULL,
                fecha_salida DATETIME NOT NULL,
                estado ENUM('confirmada', 'cancelada', 'completada') DEFAULT 'confirmada',
                fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
                huespedes_adicionales INT DEFAULT 0,
                observaciones TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion)
            )
        """)

        # Tabla de relación entre reservas y servicios adicionales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas_servicios (
                id_reserva INT NOT NULL,
                id_servicio INT NOT NULL,
                cantidad INT DEFAULT 1,
                fecha_solicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id_reserva, id_servicio),
                FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva),
                FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
            )
        """)

        # Tabla de empleados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                telefono VARCHAR(20) NOT NULL,
                puesto VARCHAR(50) NOT NULL,
                fecha_contratacion DATE NOT NULL
            )
        """)

        # Tabla de pagos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
                id_pago INT AUTO_INCREMENT PRIMARY KEY,
                id_reserva INT NOT NULL,
                monto DECIMAL(10, 2) NOT NULL,
                metodo_pago ENUM('tarjeta', 'efectivo', 'transferencia') NOT NULL,
                fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado ENUM('pendiente', 'completado', 'reembolsado') DEFAULT 'pendiente',
                FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva)
            )
        """)
        

        print("Base de datos y tablas creadas exitosamente")
    except Error as e:
        print(f'Error al crear la base de datos o las tablas: {e}')
    finally:
        if cursor:
            cursor.close()
    
    

def poblar_base_datos(connection):
    try:
        cursor = connection.cursor()

        # Insertar tipos de habitaciones
        tipos_habitacion = [
            ("Familiar", "Habitación familiar con capacidad para hasta 4 personas", 120.00, 4),
            ("Spa", "Habitación con acceso exclusivo al spa", 180.00, 2),
            ("Suite de Lujo", "Suite presidencial con todas las comodidades", 300.00, 2)
        ]

        for tipo in tipos_habitacion:
            cursor.execute("""
                INSERT INTO tipos_habitacion (nombre, descripcion, precio_por_noche, capacidad)
                VALUES (%s, %s, %s, %s)
            """, tipo)

        # Obtener los IDs de los tipos de habitaciones insertados
        cursor.execute("SELECT id_tipo FROM tipos_habitacion")
        tipos_ids = cursor.fetchall()

        # Insertar habitaciones
        habitaciones = [
            ("101", tipos_ids[0][0], 1),
            ("102", tipos_ids[0][0], 1),
            ("201", tipos_ids[1][0], 2),
            ("202", tipos_ids[1][0], 2),
            ("301", tipos_ids[2][0], 3),
            ("302", tipos_ids[2][0], 3)
        ]

        for habitacion in habitaciones:
            cursor.execute("""
                INSERT INTO habitaciones (numero, id_tipo, piso)
                VALUES (%s, %s, %s)
            """, habitacion)

        # Insertar clientes
        clientes = [
            ("Juan", "Pérez", "juan.perez@example.com", "1234567890", "Calle Falsa 123"),
            ("Ana", "Gómez", "ana.gomez@example.com", "0987654321", "Avenida Siempre Viva 456"),
            ("Carlos", "Rodríguez", "carlos.rodriguez@example.com", "5555555555", "Boulevard de los Sueños 789")
        ]

        for cliente in clientes:
            cursor.execute("""
                INSERT INTO clientes (nombre, apellido, email, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s)
            """, cliente)

        # Insertar servicios
        servicios = [
            ("Desayuno", "Desayuno buffet completo", 15.00),
            ("Cena", "Cena de tres platos", 30.00),
            ("Lavandería", "Servicio de lavandería", 20.00),
            ("Spa", "Acceso al spa por día", 50.00),
            ("Estacionamiento", "Estacionamiento por día", 10.00)
        ]

        for servicio in servicios:
            cursor.execute("""
                INSERT INTO servicios (nombre, descripcion, precio)
                VALUES (%s, %s, %s)
            """, servicio)

        connection.commit()
        print("Base de datos poblada exitosamente con datos iniciales")
    except Error as e:
        print(f'Error al poblar la base de datos: {e}')
    finally:
        if cursor:
            cursor.close()

def guardar_reserva_en_db(fecha_ingreso, fecha_salida, nombre, apellido, telefono, email, preferencias, huespedes, tipo_habitacion):
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="hotel_sheldon"
        )
        cursor = conexion.cursor()

        # Primero, verificar si el cliente ya existe
        cursor.execute("SELECT id_cliente FROM clientes WHERE email = %s", (email,))
        cliente = cursor.fetchone()

        if not cliente:
            # Si el cliente no existe, crearlo
            cursor.execute("""
                INSERT INTO clientes (nombre, apellido, email, telefono)
                VALUES (%s, %s, %s, %s)
            """, (nombre, apellido, email, telefono))
            cliente_id = cursor.lastrowid
        else:
            cliente_id = cliente[0]

        # Obtener el id_tipo de la habitación basada en el nombre del tipo
        cursor.execute("SELECT id_tipo FROM tipos_habitacion WHERE nombre = %s", (tipo_habitacion,))
        tipo = cursor.fetchone()
        if not tipo:
            raise Exception(f"Tipo de habitación '{tipo_habitacion}' no encontrado")

        tipo_id = tipo[0]

        # Buscar una habitación disponible del tipo solicitado
        cursor.execute("""
            SELECT id_habitacion FROM habitaciones
            WHERE id_tipo = %s AND estado = 'disponible'
            LIMIT 1
        """, (tipo_id,))
        habitacion = cursor.fetchone()
        if not habitacion:
            raise Exception(f"No hay habitaciones disponibles del tipo '{tipo_habitacion}'")

        habitacion_id = habitacion[0]

        # Insertar la reserva
        cursor.execute("""
            INSERT INTO reservas (id_cliente, id_habitacion, fecha_ingreso, fecha_salida, huespedes_adicionales, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cliente_id, habitacion_id, fecha_ingreso, fecha_salida, max(0, huespedes - 2), preferencias))  # Asumiendo que las habitaciones base son para 2 personas

        # Actualizar el estado de la habitación a ocupada
        cursor.execute("""
            UPDATE habitaciones SET estado = 'ocupada' WHERE id_habitacion = %s
        """, (habitacion_id,))

        conexion.commit()
    except Exception as e:
        print(f"Error al guardar la reserva: {e}")
        if conexion:
            conexion.rollback()
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

if __name__ == '__main__':
    connection = create_connection()
    if connection:
        create_database_and_tables(connection)
        poblar_base_datos(connection)
        connection.close()


