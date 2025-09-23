-- --------------------------------------------------------
-- Paso 1: Crear la base de datos y las tablas
-- --------------------------------------------------------

DROP DATABASE IF EXISTS TiendaElectronica;
CREATE DATABASE IF NOT EXISTS TiendaElectronica;
USE TiendaElectronica;

-- Tabla: Productos
CREATE TABLE Productos (
    ProductoID INT AUTO_INCREMENT PRIMARY KEY,
    NombreProducto VARCHAR(100) NOT NULL,
    Categoria VARCHAR(50),
    Precio DECIMAL(10, 2) NOT NULL,
    Stock INT DEFAULT 0
);

-- Tabla: Clientes
CREATE TABLE Clientes (
    ClienteID INT AUTO_INCREMENT PRIMARY KEY,
    NombreCliente VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Telefono VARCHAR(20),
    Ciudad VARCHAR(50)
);

-- Tabla: Empleados
CREATE TABLE Empleados (
    EmpleadoID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Cargo VARCHAR(50),
    FechaContratacion DATE
);

-- Tabla: Ordenes
CREATE TABLE Ordenes (
    OrdenID INT AUTO_INCREMENT PRIMARY KEY,
    ClienteID INT NOT NULL,
    EmpleadoID INT NOT NULL,
    FechaOrden DATE NOT NULL,
    Estado VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID) ON DELETE CASCADE,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleados(EmpleadoID) ON DELETE CASCADE
);

-- Tabla: DetallesOrden
CREATE TABLE DetallesOrden (
    DetalleID INT AUTO_INCREMENT PRIMARY KEY,
    OrdenID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    PrecioUnitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (OrdenID) REFERENCES Ordenes(OrdenID) ON DELETE CASCADE,
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- Paso 2: Insertar Datos Aleatorios en Clientes
-- --------------------------------------------------------

INSERT INTO Clientes (NombreCliente, Email, Telefono, Ciudad) VALUES
('Carlos Méndez', 'carlos.mendez@email.com', '555-0101', 'Madrid'),
('Ana López', 'ana.lopez@email.com', '555-0102', 'Barcelona'),
('Luis Fernández', 'luis.fernandez@email.com', '555-0103', 'Valencia'),
('María Gómez', 'maria.gomez@email.com', '555-0104', 'Sevilla'),
('Javier Ruiz', 'javier.ruiz@email.com', '555-0105', 'Zaragoza'),
('Laura Sánchez', 'laura.sanchez@email.com', '555-0106', 'Málaga'),
('Pedro Torres', 'pedro.torres@email.com', '555-0107', 'Murcia'),
('Sofía Ramírez', 'sofia.ramirez@email.com', '555-0108', 'Palma de Mallorca'),
('Diego Morales', 'diego.morales@email.com', '555-0109', 'Las Palmas'),
('Elena Castro', 'elena.castro@email.com', '555-0110', 'Bilbao'),
('Miguel Ángel', 'miguel.angel@email.com', '555-0111', 'Alicante'),
('Carmen Díaz', 'carmen.diaz@email.com', '555-0112', 'Córdoba'),
('Francisco Vargas', 'francisco.vargas@email.com', '555-0113', 'Valladolid'),
('Isabel Romero', 'isabel.romero@email.com', '555-0114', 'Vigo'),
('Antonio Jiménez', 'antonio.jimenez@email.com', '555-0115', 'Gijón');

-- --------------------------------------------------------
-- Paso 3: Insertar Datos Aleatorios en Empleados
-- --------------------------------------------------------

INSERT INTO Empleados (Nombre, Apellido, Cargo, FechaContratacion) VALUES
('Roberto', 'García', 'Vendedor', '2023-01-15'),
('Patricia', 'Martín', 'Gerente', '2022-03-22'),
('José', 'Hernández', 'Técnico', '2023-06-10'),
('Lucía', 'González', 'Vendedor', '2023-09-05'),
('Manuel', 'Pérez', 'Soporte', '2022-11-30'),
('Clara', 'Sánchez', 'Vendedor', '2024-02-18'),
('Alberto', 'López', 'Logística', '2023-07-12'),
('Natalia', 'Ruiz', 'Cajera', '2024-01-08');

-- --------------------------------------------------------
-- Paso 4: Insertar Datos Aleatorios en Productos
-- --------------------------------------------------------

INSERT INTO Productos (NombreProducto, Categoria, Precio, Stock) VALUES
('Laptop Gamer X1', 'Computadoras', 1200.00, 15),
('Smartphone Z20', 'Teléfonos', 699.99, 30),
('Tablet Pro 10"', 'Tablets', 349.50, 25),
('Auriculares Bluetooth', 'Accesorios', 79.90, 50),
('Cámara DSLR 24MP', 'Fotografía', 899.00, 8),
('Monitor 27" 4K', 'Periféricos', 450.00, 12),
('Teclado Mecánico RGB', 'Periféricos', 120.00, 40),
('Ratón Inalámbrico', 'Periféricos', 45.00, 60),
('Impresora Multifunción', 'Oficina', 199.99, 10),
('Disco Duro 1TB SSD', 'Almacenamiento', 129.99, 35),
('Router Wi-Fi 6', 'Redes', 159.99, 20),
('Altavoz Inteligente', 'Audio', 89.99, 28),
('Cargador Rápido 65W', 'Accesorios', 39.99, 75),
('Batería Externa 20000mAh', 'Accesorios', 59.99, 45),
('Webcam Full HD', 'Periféricos', 69.99, 33);

-- --------------------------------------------------------
-- Paso 5: Insertar Datos Aleatorios en Ordenes
-- --------------------------------------------------------

INSERT INTO Ordenes (ClienteID, EmpleadoID, FechaOrden, Estado) VALUES
(1, 1, '2024-05-10', 'Completado'),
(2, 2, '2024-05-11', 'Pendiente'),
(3, 3, '2024-05-12', 'Completado'),
(4, 1, '2024-05-13', 'Cancelado'),
(5, 4, '2024-05-14', 'Completado'),
(6, 5, '2024-05-15', 'Pendiente'),
(7, 2, '2024-05-16', 'Completado'),
(8, 6, '2024-05-17', 'Completado'),
(9, 3, '2024-05-18', 'Pendiente'),
(10, 7, '2024-05-19', 'Completado'),
(11, 4, '2024-05-20', 'Cancelado'),
(12, 1, '2024-05-21', 'Completado'),
(13, 5, '2024-05-22', 'Pendiente'),
(14, 8, '2024-05-23', 'Completado'),
(15, 6, '2024-05-24', 'Completado');

-- --------------------------------------------------------
-- Paso 6: Insertar Datos Aleatorios en DetallesOrden
-- --------------------------------------------------------

INSERT INTO DetallesOrden (OrdenID, ProductoID, Cantidad, PrecioUnitario) VALUES
-- Orden 1
(1, 1, 1, 1200.00), -- 1 Laptop
(1, 7, 1, 120.00),  -- 1 Teclado
-- Orden 2
(2, 2, 1, 699.99),  -- 1 Smartphone
-- Orden 3
(3, 3, 1, 349.50),  -- 1 Tablet
(3, 14, 1, 59.99),  -- 1 Batería Externa
-- Orden 4
(4, 5, 1, 899.00),  -- 1 Cámara
-- Orden 5
(5, 6, 1, 450.00),  -- 1 Monitor
(5, 8, 1, 45.00),   -- 1 Ratón
-- Orden 6
(6, 12, 2, 89.99),  -- 2 Altavoces
-- Orden 7
(7, 10, 1, 129.99), -- 1 Disco Duro
-- Orden 8
(8, 11, 1, 159.99), -- 1 Router
(8, 13, 1, 39.99),  -- 1 Cargador
-- Orden 9
(9, 4, 1, 79.90),   -- 1 Auriculares
-- Orden 10
(10, 9, 1, 199.99), -- 1 Impresora
-- Orden 11
(11, 15, 1, 69.99), -- 1 Webcam
-- Orden 12
(12, 1, 1, 1200.00), -- 1 Laptop
(12, 2, 1, 699.99),  -- 1 Smartphone
-- Orden 13
(13, 3, 1, 349.50),  -- 1 Tablet
-- Orden 14
(14, 7, 2, 120.00),  -- 2 Teclados
(14, 8, 2, 45.00),   -- 2 Ratones
-- Orden 15
(15, 4, 1, 79.90),   -- 1 Auriculares
(15, 14, 1, 59.99);  -- 1 Batería Externa

-- --------------------------------------------------------
-- Paso 7: PROCEDIMIENTOS ALMACENADOS (CRUD)
-- --------------------------------------------------------

DELIMITER $$

-- ================ TABLA: PRODUCTOS ================

-- INSERT
CREATE PROCEDURE sp_InsertProducto(
    IN p_NombreProducto VARCHAR(100),
    IN p_Categoria VARCHAR(50),
    IN p_Precio DECIMAL(10, 2),
    IN p_Stock INT
)
BEGIN
    INSERT INTO Productos (NombreProducto, Categoria, Precio, Stock)
    VALUES (p_NombreProducto, p_Categoria, p_Precio, p_Stock);
END$$

-- UPDATE
CREATE PROCEDURE sp_UpdateProducto(
    IN p_ProductoID INT,
    IN p_NombreProducto VARCHAR(100),
    IN p_Categoria VARCHAR(50),
    IN p_Precio DECIMAL(10, 2),
    IN p_Stock INT
)
BEGIN
    UPDATE Productos
    SET
        NombreProducto = p_NombreProducto,
        Categoria = p_Categoria,
        Precio = p_Precio,
        Stock = p_Stock
    WHERE ProductoID = p_ProductoID;
END$$

-- DELETE
CREATE PROCEDURE sp_DeleteProducto(
    IN p_ProductoID INT
)
BEGIN
    DELETE FROM Productos WHERE ProductoID = p_ProductoID;
END$$

-- ================ TABLA: CLIENTES ================

-- INSERT
CREATE PROCEDURE sp_InsertCliente(
    IN p_NombreCliente VARCHAR(100),
    IN p_Email VARCHAR(100),
    IN p_Telefono VARCHAR(20),
    IN p_Ciudad VARCHAR(50)
)
BEGIN
    INSERT INTO Clientes (NombreCliente, Email, Telefono, Ciudad)
    VALUES (p_NombreCliente, p_Email, p_Telefono, p_Ciudad);
END$$

-- UPDATE
CREATE PROCEDURE sp_UpdateCliente(
    IN p_ClienteID INT,
    IN p_NombreCliente VARCHAR(100),
    IN p_Email VARCHAR(100),
    IN p_Telefono VARCHAR(20),
    IN p_Ciudad VARCHAR(50)
)
BEGIN
    UPDATE Clientes
    SET
        NombreCliente = p_NombreCliente,
        Email = p_Email,
        Telefono = p_Telefono,
        Ciudad = p_Ciudad
    WHERE ClienteID = p_ClienteID;
END$$

-- DELETE
CREATE PROCEDURE sp_DeleteCliente(
    IN p_ClienteID INT
)
BEGIN
    DELETE FROM Clientes WHERE ClienteID = p_ClienteID;
END$$

-- ================ TABLA: EMPLEADOS ================

-- INSERT
CREATE PROCEDURE sp_InsertEmpleado(
    IN p_Nombre VARCHAR(50),
    IN p_Apellido VARCHAR(50),
    IN p_Cargo VARCHAR(50),
    IN p_FechaContratacion DATE
)
BEGIN
    INSERT INTO Empleados (Nombre, Apellido, Cargo, FechaContratacion)
    VALUES (p_Nombre, p_Apellido, p_Cargo, p_FechaContratacion);
END$$

-- UPDATE
CREATE PROCEDURE sp_UpdateEmpleado(
    IN p_EmpleadoID INT,
    IN p_Nombre VARCHAR(50),
    IN p_Apellido VARCHAR(50),
    IN p_Cargo VARCHAR(50),
    IN p_FechaContratacion DATE
)
BEGIN
    UPDATE Empleados
    SET
        Nombre = p_Nombre,
        Apellido = p_Apellido,
        Cargo = p_Cargo,
        FechaContratacion = p_FechaContratacion
    WHERE EmpleadoID = p_EmpleadoID;
END$$

-- DELETE
CREATE PROCEDURE sp_DeleteEmpleado(
    IN p_EmpleadoID INT
)
BEGIN
    DELETE FROM Empleados WHERE EmpleadoID = p_EmpleadoID;
END$$

-- ================ TABLA: ORDENES ================

-- INSERT
CREATE PROCEDURE sp_InsertOrden(
    IN p_ClienteID INT,
    IN p_EmpleadoID INT,
    IN p_FechaOrden DATE,
    IN p_Estado VARCHAR(20)
)
BEGIN
    INSERT INTO Ordenes (ClienteID, EmpleadoID, FechaOrden, Estado)
    VALUES (p_ClienteID, p_EmpleadoID, p_FechaOrden, p_Estado);
END$$

-- UPDATE
CREATE PROCEDURE sp_UpdateOrden(
    IN p_OrdenID INT,
    IN p_ClienteID INT,
    IN p_EmpleadoID INT,
    IN p_FechaOrden DATE,
    IN p_Estado VARCHAR(20)
)
BEGIN
    UPDATE Ordenes
    SET
        ClienteID = p_ClienteID,
        EmpleadoID = p_EmpleadoID,
        FechaOrden = p_FechaOrden,
        Estado = p_Estado
    WHERE OrdenID = p_OrdenID;
END$$

-- DELETE
CREATE PROCEDURE sp_DeleteOrden(
    IN p_OrdenID INT
)
BEGIN
    DELETE FROM Ordenes WHERE OrdenID = p_OrdenID;
END$$

-- ================ TABLA: DETALLESORDEN ================

-- INSERT
CREATE PROCEDURE sp_InsertDetalleOrden(
    IN p_OrdenID INT,
    IN p_ProductoID INT,
    IN p_Cantidad INT,
    IN p_PrecioUnitario DECIMAL(10, 2)
)
BEGIN
    INSERT INTO DetallesOrden (OrdenID, ProductoID, Cantidad, PrecioUnitario)
    VALUES (p_OrdenID, p_ProductoID, p_Cantidad, p_PrecioUnitario);
END$$

-- UPDATE
CREATE PROCEDURE sp_UpdateDetalleOrden(
    IN p_DetalleID INT,
    IN p_Cantidad INT,
    IN p_PrecioUnitario DECIMAL(10, 2)
)
BEGIN
    UPDATE DetallesOrden
    SET
        Cantidad = p_Cantidad,
        PrecioUnitario = p_PrecioUnitario
    WHERE DetalleID = p_DetalleID;
END$$

-- DELETE
CREATE PROCEDURE sp_DeleteDetalleOrden(
    IN p_DetalleID INT
)
BEGIN
    DELETE FROM DetallesOrden WHERE DetalleID = p_DetalleID;
END$$

DELIMITER ;

-- --------------------------------------------------------
-- Paso 8: Mensaje de Confirmación
-- --------------------------------------------------------

SELECT '¡Base de datos TiendaElectronica creada, poblada y con procedimientos almacenados listos!' AS Mensaje;

SHOW TABLES;
SELECT * FROM clientes LIMIT 5;