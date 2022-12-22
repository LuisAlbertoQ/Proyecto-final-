import sqlite3
from sqlite3 import Error

class QueriesSQLite:
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Coneccion con SQLite DB aceptada")
        except Error as e:
            print(f"El error '{e}' ocurrio")

        return connection

    
    def execute_query(connection, query, data_tuple):
        cursor = connection.cursor()
        try:
            cursor.execute(query, data_tuple)
            connection.commit()
            print("Consulta Ejecutada con Exito")
            return cursor.lastrowid
        except Error as e:
            print(f"El error '{e}' ocurrio")

    
    def execute_read_query(connection, query, data_tuple=()):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query, data_tuple)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    
    def create_tables():
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")

        tabla_productos = """
        CREATE TABLE IF NOT EXISTS productos(
         codigo TEXT PRIMARY KEY, 
         nombre TEXT NOT NULL, 
         precio REAL NOT NULL, 
         cantidad INTEGER NOT NULL
        );
        """

        tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios(
         username TEXT PRIMARY KEY, 
         nombre TEXT NOT NULL, 
         password TEXT NOT NULL,
         tipo TEXT NOT NULL
        );
        """

        tabla_ventas = """
        CREATE TABLE IF NOT EXISTS ventas(
         id INTEGER PRIMARY KEY, 
         total REAL NOT NULL, 
         fecha TIMESTAMP,
         username TEXT  NOT NULL, 
         FOREIGN KEY(username) REFERENCES usuarios(username)
        );
        """

        tabla_ventas_detalle = """
        CREATE TABLE IF NOT EXISTS ventas_detalle(
         id INTEGER PRIMARY KEY, 
         id_venta TEXT NOT NULL, 
         precio REAL NOT NULL,
         producto TEXT NOT NULL,
         cantidad INTEGER NOT NULL,
         FOREIGN KEY(id_venta) REFERENCES ventas(id),
         FOREIGN KEY(producto) REFERENCES productos(codigo)
        );
        """

        QueriesSQLite.execute_query(connection, tabla_productos, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_usuarios, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_ventas, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_ventas_detalle, tuple()) 



if __name__=="__main__":
    from datetime import datetime, timedelta
    connection = QueriesSQLite.create_connection("pdvDB.sqlite")


    fecha1= datetime.today()-timedelta(days=5)
    neuva_data=(fecha1, 4)
    actualizar = """
    UPDATE
      ventas
    SET
      fecha=?
    WHERE
      id = ?
    """

    QueriesSQLite.execute_query(connection, actualizar, neuva_data)

    select_ventas = "SELECT * from ventas"
    ventas = QueriesSQLite.execute_read_query(connection, select_ventas)
    if ventas:
        for venta in ventas:
            print("type:", type(venta), "venta:",venta)


    select_ventas_detalle = "SELECT * from ventas_detalle"
    ventas_detalle = QueriesSQLite.execute_read_query(connection, select_ventas_detalle)
    if ventas_detalle:
        for venta in ventas_detalle:
            print("type:", type(venta), "venta:",venta)
