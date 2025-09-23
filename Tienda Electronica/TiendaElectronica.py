import tkinter as tk
from tkinter import ttk
import datetime
from tkcalendar import DateEntry
from tkinter import messagebox
import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="TiendaElectronica",
                user="root",
                password="",
                port=3306,
                autocommit=False
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as error:
            if error.errno == 2003:
                messagebox.showerror("Error de Conexión", "No se puede conectar al servidor MySQL.\nVerifica que MySQL esté corriendo y que el puerto 3306 esté disponible.")
            elif error.errno == 1045:
                messagebox.showerror("Error de Autenticación", "Nombre de usuario o contraseña incorrectos.")
            else:
                messagebox.showerror("Error de Conexión", f"Error desconocido: {error}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def call_procedure(self, procedure_name, parameters=None):
        try:
            if parameters:
                self.cursor.callproc(procedure_name, parameters)
            else:
                self.cursor.callproc(procedure_name)
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            return True, results
        except mysql.connector.Error as error:
            self.connection.rollback()
            return False, str(error)

# Inicializar la conexión
db = DatabaseConnection()

# ---- Funciones para la tabla Productos ----
def limpiar_producto():
    producto_ProductoID.delete(0, tk.END)
    producto_NombreProducto.delete(0, tk.END)
    producto_Categoria.delete(0, tk.END)
    producto_Precio.delete(0, tk.END)
    producto_Stock.delete(0, tk.END)
    messagebox.showinfo("Limpieza", "Formulario de Productos limpiado.")

def guardar_producto():
    if not db.connection:
        if not db.connect():
            return
    nombre_producto = producto_NombreProducto.get().strip()
    precio = producto_Precio.get().strip()
    stock = producto_Stock.get().strip()

    if not nombre_producto:
        messagebox.showerror("Error", "El campo NombreProducto es obligatorio.")
        return
    if not precio or not precio.replace('.', '', 1).isdigit():
        messagebox.showerror("Error", "El campo Precio debe ser un número válido.")
        return
    if not stock or not stock.isdigit():
        messagebox.showerror("Error", "El campo Stock debe ser un número entero válido.")
        return

    parameters = (
        nombre_producto,
        producto_Categoria.get().strip() or None,
        float(precio),
        int(stock)
    )
    success, results = db.call_procedure("sp_InsertProducto", parameters)
    if success:
        messagebox.showinfo("Guardar", f"Producto '{nombre_producto}' guardado con éxito.")
        limpiar_producto()
    else:
        messagebox.showerror("Error", f"Error al guardar: {results}")

def actualizar_producto():
    if not db.connection:
        if not db.connect():
            return
    producto_id = producto_ProductoID.get().strip()
    nombre_producto = producto_NombreProducto.get().strip()
    precio = producto_Precio.get().strip()
    stock = producto_Stock.get().strip()

    if not producto_id or not producto_id.isdigit():
        messagebox.showerror("Error", "El campo ProductoID es obligatorio para actualizar.")
        return
    if not nombre_producto:
        messagebox.showerror("Error", "El campo NombreProducto es obligatorio.")
        return
    if not precio or not precio.replace('.', '', 1).isdigit():
        messagebox.showerror("Error", "El campo Precio debe ser un número válido.")
        return
    if not stock or not stock.isdigit():
        messagebox.showerror("Error", "El campo Stock debe ser un número entero válido.")
        return

    parameters = (
        int(producto_id),
        nombre_producto,
        producto_Categoria.get().strip() or None,
        float(precio),
        int(stock)
    )
    success, results = db.call_procedure("sp_UpdateProducto", parameters)
    if success:
        messagebox.showinfo("Actualizar", f"Producto con ID '{producto_id}' actualizado con éxito.")
    else:
        messagebox.showerror("Error", f"Error al actualizar: {results}")

def eliminar_producto():
    if not db.connection:
        if not db.connect():
            return
    producto_id = producto_ProductoID.get().strip()
    if not producto_id or not producto_id.isdigit():
        messagebox.showerror("Error", "El campo ProductoID es obligatorio para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el producto ID '{producto_id}'?"):
        return
    success, results = db.call_procedure("sp_DeleteProducto", (int(producto_id),))
    if success:
        messagebox.showinfo("Eliminar", f"Producto con ID '{producto_id}' eliminado con éxito.")
        limpiar_producto()
    else:
        messagebox.showerror("Error", f"Error al eliminar: {results}")

# ---- Funciones para la tabla Clientes ----
def limpiar_cliente():
    cliente_ClienteID.delete(0, tk.END)
    cliente_NombreCliente.delete(0, tk.END)
    cliente_Email.delete(0, tk.END)
    cliente_Telefono.delete(0, tk.END)
    cliente_Ciudad.delete(0, tk.END)
    messagebox.showinfo("Limpieza", "Formulario de Clientes limpiado.")

def guardar_cliente():
    if not db.connection:
        if not db.connect():
            return
    nombre_cliente = cliente_NombreCliente.get().strip()
    email = cliente_Email.get().strip()
    telefono = cliente_Telefono.get().strip()
    ciudad = cliente_Ciudad.get().strip()

    if not nombre_cliente:
        messagebox.showerror("Error", "El campo NombreCliente es obligatorio.")
        return

    parameters = (
        nombre_cliente,
        email or None,
        telefono or None,
        ciudad or None
    )
    success, results = db.call_procedure("sp_InsertCliente", parameters)
    if success:
        messagebox.showinfo("Guardar", f"Cliente '{nombre_cliente}' guardado con éxito.")
        limpiar_cliente()
    else:
        messagebox.showerror("Error", f"Error al guardar: {results}")

def actualizar_cliente():
    if not db.connection:
        if not db.connect():
            return
    cliente_id = cliente_ClienteID.get().strip()
    nombre_cliente = cliente_NombreCliente.get().strip()

    if not cliente_id or not cliente_id.isdigit():
        messagebox.showerror("Error", "El campo ClienteID es obligatorio para actualizar.")
        return
    if not nombre_cliente:
        messagebox.showerror("Error", "El campo NombreCliente es obligatorio.")
        return

    parameters = (
        int(cliente_id),
        nombre_cliente,
        cliente_Email.get().strip() or None,
        cliente_Telefono.get().strip() or None,
        cliente_Ciudad.get().strip() or None
    )
    success, results = db.call_procedure("sp_UpdateCliente", parameters)
    if success:
        messagebox.showinfo("Actualizar", f"Cliente con ID '{cliente_id}' actualizado con éxito.")
    else:
        messagebox.showerror("Error", f"Error al actualizar: {results}")

def eliminar_cliente():
    if not db.connection:
        if not db.connect():
            return
    cliente_id = cliente_ClienteID.get().strip()
    if not cliente_id or not cliente_id.isdigit():
        messagebox.showerror("Error", "El campo ClienteID es obligatorio para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el cliente ID '{cliente_id}'?"):
        return
    success, results = db.call_procedure("sp_DeleteCliente", (int(cliente_id),))
    if success:
        messagebox.showinfo("Eliminar", f"Cliente con ID '{cliente_id}' eliminado con éxito.")
        limpiar_cliente()
    else:
        messagebox.showerror("Error", f"Error al eliminar: {results}")

# ---- Funciones para la tabla Empleados ----
def limpiar_empleado():
    empleado_EmpleadoID.delete(0, tk.END)
    empleado_Nombre.delete(0, tk.END)
    empleado_Apellido.delete(0, tk.END)
    empleado_Cargo.delete(0, tk.END)
    empleado_FechaContratacion.set_date(datetime.date.today())
    messagebox.showinfo("Limpieza", "Formulario de Empleados limpiado.")

def guardar_empleado():
    if not db.connection:
        if not db.connect():
            return
    nombre = empleado_Nombre.get().strip()
    apellido = empleado_Apellido.get().strip()
    cargo = empleado_Cargo.get().strip()
    fecha_contratacion = empleado_FechaContratacion.get_date()

    if not nombre or not apellido:
        messagebox.showerror("Error", "Los campos Nombre y Apellido son obligatorios.")
        return

    parameters = (
        nombre,
        apellido,
        cargo or None,
        fecha_contratacion
    )
    success, results = db.call_procedure("sp_InsertEmpleado", parameters)
    if success:
        messagebox.showinfo("Guardar", f"Empleado '{nombre} {apellido}' guardado con éxito.")
        limpiar_empleado()
    else:
        messagebox.showerror("Error", f"Error al guardar: {results}")

def actualizar_empleado():
    if not db.connection:
        if not db.connect():
            return
    empleado_id = empleado_EmpleadoID.get().strip()
    nombre = empleado_Nombre.get().strip()
    apellido = empleado_Apellido.get().strip()

    if not empleado_id or not empleado_id.isdigit():
        messagebox.showerror("Error", "El campo EmpleadoID es obligatorio para actualizar.")
        return
    if not nombre or not apellido:
        messagebox.showerror("Error", "Los campos Nombre y Apellido son obligatorios.")
        return

    parameters = (
        int(empleado_id),
        nombre,
        apellido,
        empleado_Cargo.get().strip() or None,
        empleado_FechaContratacion.get_date()
    )
    success, results = db.call_procedure("sp_UpdateEmpleado", parameters)
    if success:
        messagebox.showinfo("Actualizar", f"Empleado con ID '{empleado_id}' actualizado con éxito.")
    else:
        messagebox.showerror("Error", f"Error al actualizar: {results}")

def eliminar_empleado():
    if not db.connection:
        if not db.connect():
            return
    empleado_id = empleado_EmpleadoID.get().strip()
    if not empleado_id or not empleado_id.isdigit():
        messagebox.showerror("Error", "El campo EmpleadoID es obligatorio para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el empleado ID '{empleado_id}'?"):
        return
    success, results = db.call_procedure("sp_DeleteEmpleado", (int(empleado_id),))
    if success:
        messagebox.showinfo("Eliminar", f"Empleado con ID '{empleado_id}' eliminado con éxito.")
        limpiar_empleado()
    else:
        messagebox.showerror("Error", f"Error al eliminar: {results}")

# ---- Funciones para la tabla Ordenes ----
def limpiar_orden():
    orden_OrdenID.delete(0, tk.END)
    orden_ClienteID.delete(0, tk.END)
    orden_EmpleadoID.delete(0, tk.END)
    orden_FechaOrden.set_date(datetime.date.today())
    orden_Estado.delete(0, tk.END)
    messagebox.showinfo("Limpieza", "Formulario de Ordenes limpiado.")

def guardar_orden():
    if not db.connection:
        if not db.connect():
            return
    cliente_id = orden_ClienteID.get().strip()
    empleado_id = orden_EmpleadoID.get().strip()
    fecha_orden = orden_FechaOrden.get_date()
    estado = orden_Estado.get().strip()

    if not cliente_id or not cliente_id.isdigit():
        messagebox.showerror("Error", "El campo ClienteID es obligatorio y debe ser numérico.")
        return
    if not empleado_id or not empleado_id.isdigit():
        messagebox.showerror("Error", "El campo EmpleadoID es obligatorio y debe ser numérico.")
        return
    if not fecha_orden:
        messagebox.showerror("Error", "El campo FechaOrden es obligatorio.")
        return

    parameters = (
        int(cliente_id),
        int(empleado_id),
        fecha_orden,
        estado or 'Pendiente'
    )
    success, results = db.call_procedure("sp_InsertOrden", parameters)
    if success:
        messagebox.showinfo("Guardar", f"Orden para ClienteID '{cliente_id}' guardada con éxito.")
        limpiar_orden()
    else:
        messagebox.showerror("Error", f"Error al guardar: {results}")

def actualizar_orden():
    if not db.connection:
        if not db.connect():
            return
    orden_id = orden_OrdenID.get().strip()
    cliente_id = orden_ClienteID.get().strip()
    empleado_id = orden_EmpleadoID.get().strip()
    fecha_orden = orden_FechaOrden.get_date()
    estado = orden_Estado.get().strip()

    if not orden_id or not orden_id.isdigit():
        messagebox.showerror("Error", "El campo OrdenID es obligatorio para actualizar.")
        return
    if not cliente_id or not cliente_id.isdigit():
        messagebox.showerror("Error", "El campo ClienteID es obligatorio y debe ser numérico.")
        return
    if not empleado_id or not empleado_id.isdigit():
        messagebox.showerror("Error", "El campo EmpleadoID es obligatorio y debe ser numérico.")
        return

    parameters = (
        int(orden_id),
        int(cliente_id),
        int(empleado_id),
        fecha_orden,
        estado or 'Pendiente'
    )
    success, results = db.call_procedure("sp_UpdateOrden", parameters)
    if success:
        messagebox.showinfo("Actualizar", f"Orden con ID '{orden_id}' actualizada con éxito.")
    else:
        messagebox.showerror("Error", f"Error al actualizar: {results}")

def eliminar_orden():
    if not db.connection:
        if not db.connect():
            return
    orden_id = orden_OrdenID.get().strip()
    if not orden_id or not orden_id.isdigit():
        messagebox.showerror("Error", "El campo OrdenID es obligatorio para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar la orden ID '{orden_id}'?"):
        return
    success, results = db.call_procedure("sp_DeleteOrden", (int(orden_id),))
    if success:
        messagebox.showinfo("Eliminar", f"Orden con ID '{orden_id}' eliminada con éxito.")
        limpiar_orden()
    else:
        messagebox.showerror("Error", f"Error al eliminar: {results}")

# ---- Funciones para la tabla DetallesOrden ----
def limpiar_detalle():
    detalle_DetalleID.delete(0, tk.END)
    detalle_OrdenID.delete(0, tk.END)
    detalle_ProductoID.delete(0, tk.END)
    detalle_Cantidad.delete(0, tk.END)
    detalle_PrecioUnitario.delete(0, tk.END)
    messagebox.showinfo("Limpieza", "Formulario de DetallesOrden limpiado.")

def guardar_detalle():
    if not db.connection:
        if not db.connect():
            return
    orden_id = detalle_OrdenID.get().strip()
    producto_id = detalle_ProductoID.get().strip()
    cantidad = detalle_Cantidad.get().strip()
    precio_unitario = detalle_PrecioUnitario.get().strip()

    if not orden_id or not orden_id.isdigit():
        messagebox.showerror("Error", "El campo OrdenID es obligatorio y debe ser numérico.")
        return
    if not producto_id or not producto_id.isdigit():
        messagebox.showerror("Error", "El campo ProductoID es obligatorio y debe ser numérico.")
        return
    if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "El campo Cantidad es obligatorio, debe ser un número entero mayor que 0.")
        return
    if not precio_unitario or not precio_unitario.replace('.', '', 1).isdigit() or float(precio_unitario) <= 0:
        messagebox.showerror("Error", "El campo PrecioUnitario es obligatorio y debe ser un número válido mayor que 0.")
        return

    parameters = (
        int(orden_id),
        int(producto_id),
        int(cantidad),
        float(precio_unitario)
    )
    success, results = db.call_procedure("sp_InsertDetalleOrden", parameters)
    if success:
        messagebox.showinfo("Guardar", f"Detalle para OrdenID '{orden_id}' guardado con éxito.")
        limpiar_detalle()
    else:
        messagebox.showerror("Error", f"Error al guardar: {results}")

def actualizar_detalle():
    if not db.connection:
        if not db.connect():
            return
    detalle_id = detalle_DetalleID.get().strip()
    cantidad = detalle_Cantidad.get().strip()
    precio_unitario = detalle_PrecioUnitario.get().strip()

    if not detalle_id or not detalle_id.isdigit():
        messagebox.showerror("Error", "El campo DetalleID es obligatorio para actualizar.")
        return
    if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "El campo Cantidad es obligatorio, debe ser un número entero mayor que 0.")
        return
    if not precio_unitario or not precio_unitario.replace('.', '', 1).isdigit() or float(precio_unitario) <= 0:
        messagebox.showerror("Error", "El campo PrecioUnitario es obligatorio y debe ser un número válido mayor que 0.")
        return

    parameters = (
        int(detalle_id),
        int(cantidad),
        float(precio_unitario)
    )
    success, results = db.call_procedure("sp_UpdateDetalleOrden", parameters)
    if success:
        messagebox.showinfo("Actualizar", f"Detalle con ID '{detalle_id}' actualizado con éxito.")
    else:
        messagebox.showerror("Error", f"Error al actualizar: {results}")

def eliminar_detalle():
    if not db.connection:
        if not db.connect():
            return
    detalle_id = detalle_DetalleID.get().strip()
    if not detalle_id or not detalle_id.isdigit():
        messagebox.showerror("Error", "El campo DetalleID es obligatorio para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el detalle ID '{detalle_id}'?"):
        return
    success, results = db.call_procedure("sp_DeleteDetalleOrden", (int(detalle_id),))
    if success:
        messagebox.showinfo("Eliminar", f"Detalle con ID '{detalle_id}' eliminado con éxito.")
        limpiar_detalle()
    else:
        messagebox.showerror("Error", f"Error al eliminar: {results}")

# ---------- INTERFAZ -------------
root = tk.Tk()
root.geometry('800x800')
root.title("TiendaElectronica Management")

notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook) # Productos
tab2 = ttk.Frame(notebook) # Clientes
tab3 = ttk.Frame(notebook) # Empleados
tab4 = ttk.Frame(notebook) # Ordenes
tab5 = ttk.Frame(notebook) # DetallesOrden

notebook.add(tab1, text="Productos")
notebook.add(tab2, text="Clientes")
notebook.add(tab3, text="Empleados")
notebook.add(tab4, text="Ordenes")
notebook.add(tab5, text="DetallesOrden")

notebook.pack(expand=True, fill="both")

# PESTAÑA 1: Productos
tk.Label(tab1, text="FORMULARIO DE PRODUCTOS", font=("Arial", 16, "bold"), fg="blue").pack(pady=20)
form_frame = tk.Frame(tab1)
form_frame.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame, text="ProductoID:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
producto_ProductoID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
producto_ProductoID.grid(row=0, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="NombreProducto:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
producto_NombreProducto = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
producto_NombreProducto.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Categoria:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
producto_Categoria = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
producto_Categoria.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Precio:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
producto_Precio = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
producto_Precio.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Stock:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
producto_Stock = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
producto_Stock.grid(row=4, column=1, sticky="w", pady=10)

button_frame1 = tk.Frame(tab1)
button_frame1.pack(pady=20)

tk.Button(button_frame1, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10, command=guardar_producto).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame1, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10, command=actualizar_producto).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame1, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=eliminar_producto).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame1, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10, command=limpiar_producto).pack(side=tk.LEFT, padx=5)

# PESTAÑA 2: Clientes
tk.Label(tab2, text="GESTIÓN DE CLIENTES", font=("Arial", 16, "bold"), fg="green").pack(pady=20)
form_frame = tk.Frame(tab2)
form_frame.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame, text="ClienteID:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
cliente_ClienteID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
cliente_ClienteID.grid(row=0, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="NombreCliente:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
cliente_NombreCliente = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
cliente_NombreCliente.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
cliente_Email = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
cliente_Email.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Telefono:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
cliente_Telefono = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
cliente_Telefono.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Ciudad:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
cliente_Ciudad = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
cliente_Ciudad.grid(row=4, column=1, sticky="w", pady=10)

button_frame2 = tk.Frame(tab2)
button_frame2.pack(pady=20)

tk.Button(button_frame2, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10, command=guardar_cliente).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame2, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10, command=actualizar_cliente).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame2, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=eliminar_cliente).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame2, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10, command=limpiar_cliente).pack(side=tk.LEFT, padx=5)

# PESTAÑA 3: Empleados
tk.Label(tab3, text="GESTIÓN DE EMPLEADOS", font=("Arial", 16, "bold"), fg="red").pack(pady=20)
form_frame = tk.Frame(tab3)
form_frame.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame, text="EmpleadoID:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
empleado_EmpleadoID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
empleado_EmpleadoID.grid(row=0, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Nombre:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
empleado_Nombre = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
empleado_Nombre.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Apellido:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
empleado_Apellido = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
empleado_Apellido.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Cargo:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
empleado_Cargo = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
empleado_Cargo.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Fecha Contratación:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
empleado_FechaContratacion = DateEntry(form_frame, width=22, font=("Arial", 12), date_pattern="yyyy-mm-dd")
empleado_FechaContratacion.grid(row=4, column=1, sticky="w", pady=10)

button_frame3 = tk.Frame(tab3)
button_frame3.pack(pady=20)

tk.Button(button_frame3, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10, command=guardar_empleado).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame3, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10, command=actualizar_empleado).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame3, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=eliminar_empleado).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame3, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10, command=limpiar_empleado).pack(side=tk.LEFT, padx=5)

# PESTAÑA 4: Ordenes
tk.Label(tab4, text="GESTIÓN DE ORDENES", font=("Arial", 16, "bold"), fg="purple").pack(pady=20)
form_frame = tk.Frame(tab4)
form_frame.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame, text="OrdenID:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
orden_OrdenID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
orden_OrdenID.grid(row=0, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="ClienteID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
orden_ClienteID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
orden_ClienteID.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="EmpleadoID:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
orden_EmpleadoID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
orden_EmpleadoID.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Fecha Orden:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
orden_FechaOrden = DateEntry(form_frame, width=22, font=("Arial", 12), date_pattern="yyyy-mm-dd")
orden_FechaOrden.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Estado:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
orden_Estado = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
orden_Estado.grid(row=4, column=1, sticky="w", pady=10)
orden_Estado.insert(0, "Pendiente") # Valor por defecto

button_frame4 = tk.Frame(tab4)
button_frame4.pack(pady=20)

tk.Button(button_frame4, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10, command=guardar_orden).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame4, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10, command=actualizar_orden).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame4, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=eliminar_orden).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame4, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10, command=limpiar_orden).pack(side=tk.LEFT, padx=5)

# PESTAÑA 5: DetallesOrden
tk.Label(tab5, text="GESTIÓN DE DETALLES DE ORDEN", font=("Arial", 16, "bold"), fg="gray").pack(pady=20)
form_frame = tk.Frame(tab5)
form_frame.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame, text="DetalleID:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
detalle_DetalleID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
detalle_DetalleID.grid(row=0, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="OrdenID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
detalle_OrdenID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
detalle_OrdenID.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="ProductoID:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
detalle_ProductoID = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
detalle_ProductoID.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Cantidad:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
detalle_Cantidad = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
detalle_Cantidad.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame, text="Precio Unitario:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
detalle_PrecioUnitario = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
detalle_PrecioUnitario.grid(row=4, column=1, sticky="w", pady=10)

button_frame5 = tk.Frame(tab5)
button_frame5.pack(pady=20)

tk.Button(button_frame5, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10, command=guardar_detalle).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame5, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10, command=actualizar_detalle).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame5, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10, command=eliminar_detalle).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame5, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10, command=limpiar_detalle).pack(side=tk.LEFT, padx=5)

root.mainloop()
