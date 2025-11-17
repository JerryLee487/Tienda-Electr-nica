# Tienda-Electrónica
Este proyecto es una aplicación de escritorio desarrollada en Python que permite gestionar una base de datos de una tienda de electrónica mediante una interfaz gráfica intuitiva. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las principales entidades del negocio: Productos, Clientes, Empleados, Órdenes y Detalles de Órdenes.

Requisitos necesarios.
Lenguaje: Python 3.x
Interfaz Gráfica: tkinter y ttk (biblioteca estándar de Python)
Selector de Fechas: tkcalendar (para elegir fechas de forma visual)
Conector a Base de Datos: mysql-connector-python (conexión oficial a MySQL)
Base de Datos: MySQL
IDE Recomendado: PyCharm, VS Code

Instrucciones de Instalación y Uso 
1. Requisitos Previos
Tener Python instalado.
Tener MySQL corriendo en tu máquina (localhost:3306)
Tener XAMPP instalado para poder encender los servicios Apache y MySQL para que funcione correctamente la base de datos.
Tener la base de datos TiendaElectronica creada y poblada.

2.  Instalación de Dependencias
Ejecuta en tu terminal:
pip install mysql-connector-python tkcalendar

Funciones procedimientos almacenados
-Productos
sp_InsertProducto,
sp_UpdateProducto,
sp_DeleteProducto,

Gestiona productos (nombre, categoría, precio, stock).

-Clientes
sp_InsertCliente,
sp_UpdateCliente,
sp_DeleteCliente,

Gestiona clientes (nombre, email, teléfono, ciudad)

-Empleados
sp_InsertEmpleado,
sp_UpdateEmpleado,
sp_DeleteEmpleado,

Gestiona empleados (nombre, apellido, cargo, fecha de contratación).

-Ordenes
sp_InsertOrden,
sp_UpdateOrden,
sp_DeleteOrden,

Gestiona órdenes (cliente, empleado, fecha, estado).

-DetallesOrden
sp_InsertDetalleOrden,
sp_UpdateDetalleOrden,
sp_DeleteDetalleOrden,

Gestiona órdenes (cliente, empleado, fecha, estado).

-DetallesOrden
sp_InsertDetalleOrden,
sp_UpdateDetalleOrden,
sp_DeleteDetalleOrden,

Gestiona los productos dentro de una orden (cantidad, precio unitario).

https://github.com/JerryLee487/TiendaElectronicaMVC/tree/main)
