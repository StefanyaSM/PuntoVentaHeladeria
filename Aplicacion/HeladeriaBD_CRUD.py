import oracledb #pip install oracledb
import pandas as pd #python -m pip install pandas

def conectar():
    try:
        #Abre la conexion que se usara en las operaciones siguientes
        conexion = oracledb.connect(
            user="HR",
            password="DbPass_2024?",
            dsn="oracleHr_high",
            config_dir=r"C:\Users\stefy\Documents\Wallet_OracleHr",
            wallet_location=r"C:\Users\stefy\Documents\Wallet_OracleHr",
            wallet_password="Diana2110.2110"
        )

        #Muestra en consola el resultado de la operacion
        print("Conexion exitosa")
        return conexion

    except oracledb.DatabaseError as e: #en caso de error
        print(f"Error de conexion: {e}")
        return None


# Funciones CRUD de la tabla STORE
def crear_store(store_id, store_name, postal_code, city, address):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            #Guarda la consulta SQL que se ejecutara en Oracle
            sql = """
            INSERT INTO STORE
            (StoreID, StoreName, PostalCode, City, Address)
            VALUES (:1, :2, :3, :4, :5)
            """
            # Ejecuta la sentencia SQL con sus parametros.
            cursor.execute(sql, (store_id, store_name, postal_code, city, address))
            conexion.commit()
            print(f"\nTienda {store_id} {store_name} creada exitosamente")  #Muestra en consola el resultado de la operacion
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()          #cierra el cursor abierto 
            conexion.close()        #cierra la conexion


def leer_stores(mostrar=True):
    conexion = conectar()
    cursor = None
    stores = [] #crear un array vacio para guardar los datos de las tiendas
    if conexion:
        try:
            cursor = conexion.cursor()
            #Guarda la consulta SQL
            sql = """
            SELECT StoreID, StoreName, PostalCode, City, Address
            FROM STORE
            ORDER BY StoreID
            """
            cursor.execute(sql)
            stores = cursor.fetchall() #guarda el resultado de la consulta 

            if mostrar:
                # Muestra en consola el resultado de la operacion.
                print("\n--- Tiendas ---")
                print(f"\n{'ID':<10} {'NOMBRE':<25} {'CP':<12} {'CIUDAD':<20} {'DIRECCION':<35}")
                print("-" * 105) #muestra una linea de separacion para formato nomas

                for row in stores: #con un for recorre cada fila de la consulta y muestra los datos en formato de tabla
                    print(f"{row[0]:<10} {row[1]:<25} {str(row[2]):<12} {str(row[3]):<20} {str(row[4]):<35}")

        except oracledb.DatabaseError as e: #si hay error
            print(f"Error de Base de Datos: {e}")
        finally: #libera recursos
            if cursor:
                cursor.close()
            conexion.close()

    # Devuelve el arreglo para que otra parte del programa lo use
    return stores


def leer_store_por_id(store_id, mostrar=True):
    conexion = conectar()
    cursor = None
    row = None #define row como None para guardar el resultado de la consulta y usarlo despues
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT StoreID, StoreName, PostalCode, City, Address
            FROM STORE
            WHERE StoreID = :1
            """
            cursor.execute(sql, (store_id,))
            row = cursor.fetchone()

            if mostrar:
                if row:
                    #Si encontro la teinda con ese ID muestra sus datos
                    print(f"\nTienda {store_id} encontrada:")
                    print(f"ID: {row[0]}")
                    print(f"Nombre: {row[1]}")
                    print(f"Codigo postal: {row[2]}")
                    print(f"Ciudad: {row[3]}")
                    print(f"Direccion: {row[4]}")
                else:
                    print(f"No se encontro la tienda {store_id}") #si no pudo encontrar la teinda con ese ID

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()
    return row


def actualizar_store(store_id, nuevo_store_name, nuevo_postal_code, nueva_city, nuevo_address):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE STORE
            SET StoreName = :1, PostalCode = :2, City = :3, Address = :4
            WHERE StoreID = :5
            """
            cursor.execute(sql, (nuevo_store_name, nuevo_postal_code, nueva_city, nuevo_address, store_id))

            # Revisa si la consulta afecto registros antes de confirmar
            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nTienda {store_id} actualizada exitosamente") #muestra en consola
            else:
                print(f"\nNo se encontro la tienda {store_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar tienda: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_store(store_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM STORE WHERE StoreID = :1"
            cursor.execute(sql, (store_id,))

            if cursor.rowcount > 0: #checa si la consulta borro algun registro antes de confirmar
                conexion.commit() #sisi hace commit
                print(f"\nTienda {store_id} eliminada exitosamente") 
            else:
                print(f"\nNo se encontro tienda con ID {store_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar tienda: {e}")
        finally:
            cursor.close()
            conexion.close()


# Funciones CRUD de la tabla CUSTOMERS
def crear_customer(customer_id, name):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO CUSTOMERS
            (CustomerID, Name)
            VALUES (:1, :2)
            """
            cursor.execute(sql, (customer_id, name))
            conexion.commit()
            print(f"\nCliente {customer_id} {name} creado exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_customers():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT CustomerID, Name
            FROM CUSTOMERS
            ORDER BY CustomerID
            """
            cursor.execute(sql)

            print("\n--- Clientes ---")
            print(f"\n{'ID':<10} {'NOMBRE':<30}")
            print("-" * 50)

            for row in cursor.fetchall(): #recorre las filas de la consulta y con fetchall saca el renglon completo
                print(f"{row[0]:<10} {row[1]:<30}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_customer_por_id(customer_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT CustomerID, Name
            FROM CUSTOMERS
            WHERE CustomerID = :1
            """
            cursor.execute(sql, (customer_id,))
            row = cursor.fetchone()

            if row: #si encontro el cliente con ese ID muestra sus datos
                print(f"\nCliente {customer_id} encontrado:")
                print(f"ID: {row[0]}")
                print(f"Nombre: {row[1]}")
            else:
                print(f"No se encontro el cliente {customer_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def actualizar_customer(customer_id, nuevo_name):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE CUSTOMERS
            SET Name = :1
            WHERE CustomerID = :2
            """
            cursor.execute(sql, (nuevo_name, customer_id))

            if cursor.rowcount > 0:
                #Confirma los cambios para que queden guardados en la BD
                conexion.commit()
                print(f"\nCliente {customer_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el cliente {customer_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar cliente: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_customer(customer_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM CUSTOMERS WHERE CustomerID = :1"
            cursor.execute(sql, (customer_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nCliente {customer_id} eliminado exitosamente")
            else:
                print(f"\nNo se encontro cliente con ID {customer_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar cliente: {e}")
        finally:
            cursor.close()
            conexion.close()


def crear_employee(employee_id, name, job_position, store_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO EMPLOYEE
            (EmployeeID, Name, JobPosition, StoreID)
            VALUES (:1, :2, :3, :4)
            """
            cursor.execute(sql, (employee_id, name, job_position, store_id))
            conexion.commit()
            print(f"\nEmpleado {employee_id} {name} creado exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_employees(mostrar=True):
    conexion = conectar()
    cursor = None
    empleados = []
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT EmployeeID, Name, JobPosition, StoreID
            FROM EMPLOYEE
            ORDER BY EmployeeID
            """
            cursor.execute(sql)
            empleados = cursor.fetchall()

            if mostrar: #si pudo ejecutar la consulta muestra los datos
                print("\n--- Empleados ---")
                print(f"\n{'ID':<10} {'NOMBRE':<25} {'PUESTO':<20} {'TIENDA':<10}")
                print("-" * 80)

                for row in empleados: #recorre cada fila de la consulta
                    print(f"{row[0]:<10} {row[1]:<25} {str(row[2]):<20} {str(row[3]):<10}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()
    return empleados


def leer_employee_por_id(employee_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT EmployeeID, Name, JobPosition, StoreID
            FROM EMPLOYEE
            WHERE EmployeeID = :1
            """
            cursor.execute(sql, (employee_id,))
            row = cursor.fetchone()

            if row:
                print(f"\nEmpleado {employee_id} encontrado:")
                print(f"ID: {row[0]}")
                print(f"Nombre: {row[1]}")
                print(f"Puesto: {row[2]}")
                print(f"Store ID: {row[3]}")
            else:
                print(f"No se encontro el empleado {employee_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def obtener_id_gerente():
    conexion = conectar()
    cursor = None
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT EmployeeID
            FROM (
                SELECT EmployeeID
                FROM EMPLOYEE
                WHERE UPPER(JobPosition) LIKE '%MANAGER%'
                   OR UPPER(JobPosition) LIKE '%GERENTE%'
                ORDER BY EmployeeID
            )
            WHERE ROWNUM = 1
            """
            cursor.execute(sql)
            fila = cursor.fetchone()

            if fila:
                return int(fila[0])

            print("No se encontro un gerente en EMPLOYEE")
        except oracledb.DatabaseError as e:
            print(f"No se pudo consultar el gerente: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    return None


def actualizar_employee(employee_id, nuevo_name, nuevo_job_position, nuevo_store_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE EMPLOYEE
            SET Name = :1, JobPosition = :2, StoreID = :3
            WHERE EmployeeID = :4
            """
            cursor.execute(sql, (nuevo_name, nuevo_job_position, nuevo_store_id, employee_id))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nEmpleado {employee_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el empleado {employee_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar empleado: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_employee(employee_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM EMPLOYEE WHERE EmployeeID = :1"
            cursor.execute(sql, (employee_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nEmpleado {employee_id} eliminado exitosamente")
            else:
                print(f"\nNo se encontro empleado con ID {employee_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar empleado: {e}")
        finally:
            cursor.close()
            conexion.close()


# Funciones CRUD de la tabla PAYMENT
def crear_payment(payment_id, is_cash, amount, received=None, payment_change=None, card=None):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO PAYMENT
            (PaymentID, Is_Cash, Amount)
            VALUES (:1, :2, :3)
            """
            cursor.execute(sql, (payment_id, is_cash, amount))

            if int(is_cash) == 1:
                sql = """
                INSERT INTO CASH
                (PaymentID, Received, Change)
                VALUES (:1, :2, :3)
                """
                cursor.execute(sql, (payment_id, received, payment_change))
            else:
                sql = """
                INSERT INTO CARD
                (PaymentID, CardNum)
                VALUES (:1, :2)
                """
                cursor.execute(sql, (payment_id, card))

            conexion.commit()
            print(f"\nPago {payment_id} creado exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_payments():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT PaymentID, Is_Cash, Amount
            FROM PAYMENT
            ORDER BY PaymentID
            """
            cursor.execute(sql)
            payments = cursor.fetchall()

            print("\n--- Pagos ---")
            print(f"\n{'ID':<10} {'EFECTIVO':<12} {'MONTO':<12} {'RECIBIDO':<12} {'CAMBIO':<12} {'CARD':<12}")
            print("-" * 78)

            for row in payments:
                received = None
                payment_change = None
                card = None

                if int(row[1]) == 1:
                    cursor.execute("SELECT Received, Change FROM CASH WHERE PaymentID = :1", (row[0],))
                    cash = cursor.fetchone()
                    if cash:
                        received = cash[0]
                        payment_change = cash[1]
                else:
                    cursor.execute("SELECT CardNum FROM CARD WHERE PaymentID = :1", (row[0],))
                    card_row = cursor.fetchone()
                    if card_row:
                        card = card_row[0]

                print(f"{row[0]:<10} {str(row[1]):<12} {str(row[2]):<12} {str(received):<12} {str(payment_change):<12} {str(card):<12}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_payment_por_id(payment_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT PaymentID, Is_Cash, Amount
            FROM PAYMENT
            WHERE PaymentID = :1
            """
            cursor.execute(sql, (payment_id,))
            row = cursor.fetchone()

            if row:
                received = None
                payment_change = None
                card = None

                if int(row[1]) == 1:
                    cursor.execute("SELECT Received, Change FROM CASH WHERE PaymentID = :1", (payment_id,))
                    cash = cursor.fetchone()
                    if cash:
                        received = cash[0]
                        payment_change = cash[1]
                else:
                    cursor.execute("SELECT CardNum FROM CARD WHERE PaymentID = :1", (payment_id,))
                    card_row = cursor.fetchone()
                    if card_row:
                        card = card_row[0]

                print(f"\nPago {payment_id} encontrado:")
                print(f"ID: {row[0]}")
                print(f"Es efectivo: {row[1]}")
                print(f"Monto: {row[2]}")
                print(f"Recibido: {received}")
                print(f"Cambio: {payment_change}")
                print(f"Card: {card}")
            else:
                print(f"No se encontro el pago {payment_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def actualizar_payment(
    payment_id,
    nuevo_is_cash,
    nuevo_amount,
    nuevo_received=None,
    nuevo_payment_change=None,
    nuevo_card=None
):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE PAYMENT
            SET Is_Cash = :1, Amount = :2
            WHERE PaymentID = :3
            """
            cursor.execute(
                sql,
                (
                    nuevo_is_cash,
                    nuevo_amount,
                    payment_id
                )
            )

            if cursor.rowcount > 0:
                cursor.execute("DELETE FROM CASH WHERE PaymentID = :1", (payment_id,))
                cursor.execute("DELETE FROM CARD WHERE PaymentID = :1", (payment_id,))

                if int(nuevo_is_cash) == 1:
                    sql = """
                    INSERT INTO CASH
                    (PaymentID, Received, Change)
                    VALUES (:1, :2, :3)
                    """
                    cursor.execute(sql, (payment_id, nuevo_received, nuevo_payment_change))
                else:
                    sql = """
                    INSERT INTO CARD
                    (PaymentID, CardNum)
                    VALUES (:1, :2)
                    """
                    cursor.execute(sql, (payment_id, nuevo_card))

                conexion.commit()
                print(f"\nPago {payment_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el pago {payment_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar pago: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_payment(payment_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM PAYMENT WHERE PaymentID = :1"
            cursor.execute(sql, (payment_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nPago {payment_id} eliminado exitosamente")
            else:
                print(f"\nNo se encontro pago con ID {payment_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar pago: {e}")
        finally:
            cursor.close()
            conexion.close()


# Funciones CRUD de la tabla MENU_ITEM
def crear_menu_item(menu_item_id, name, price, description):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO MENU_ITEM
            (MenuItemID, Name, Price, Description)
            VALUES (:1, :2, :3, :4)
            """
            cursor.execute(sql, (menu_item_id, name, price, description))
            conexion.commit()
            print(f"\nProducto {menu_item_id} {name} creado exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_menu_items(mostrar=True):
    conexion = conectar()
    cursor = None
    menu_items = []
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT MenuItemID, Name, Price, Description
            FROM MENU_ITEM
            ORDER BY MenuItemID
            """
            cursor.execute(sql)
            menu_items = cursor.fetchall()

            if mostrar:
                print("\n--- Menu ---")
                print(f"\n{'ID':<10} {'NOMBRE':<25} {'PRECIO':<12} {'DESCRIPCION':<40}")
                print("-" * 95)

                for row in menu_items:
                    print(f"{row[0]:<10} {row[1]:<25} {str(row[2]):<12} {str(row[3]):<40}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    return menu_items


def leer_menu_item_por_id(menu_item_id, mostrar=True):
    conexion = conectar()
    cursor = None
    row = None
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT MenuItemID, Name, Price, Description
            FROM MENU_ITEM
            WHERE MenuItemID = :1
            """
            cursor.execute(sql, (menu_item_id,))
            row = cursor.fetchone()

            if mostrar:
                if row:
                    print(f"\nProducto {menu_item_id} encontrado:")
                    print(f"ID: {row[0]}")
                    print(f"Nombre: {row[1]}")
                    print(f"Precio: {row[2]}")
                    print(f"Descripcion: {row[3]}")
                else:
                    print(f"No se encontro el producto {menu_item_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    return row


def actualizar_menu_item(menu_item_id, nuevo_name, nuevo_price, nueva_description):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE MENU_ITEM
            SET Name = :1, Price = :2, Description = :3
            WHERE MenuItemID = :4
            """
            cursor.execute(sql, (nuevo_name, nuevo_price, nueva_description, menu_item_id))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nProducto {menu_item_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el producto {menu_item_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar producto: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_menu_item(menu_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM MENU_ITEM WHERE MenuItemID = :1"
            cursor.execute(sql, (menu_item_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nProducto {menu_item_id} eliminado exitosamente")
            else:
                print(f"\nNo se encontro producto con ID {menu_item_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar producto: {e}")
        finally:
            cursor.close()
            conexion.close()


# Funciones CRUD de la tabla TICKET
def crear_ticket(ticket_id, order_date, store_id, employee_id, customer_id, payment_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            order_date = str(order_date).strip()
            if " " not in order_date:
                order_date = order_date + " 00:00"

            sql = """
            INSERT INTO TICKET
            (TicketID, OrderDate, StoreID, EmployeeID, CustomerID, PaymentID)
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD HH24:MI'), :3, :4, :5, :6)
            """
            cursor.execute(sql, (ticket_id, order_date, store_id, employee_id, customer_id, payment_id))
            conexion.commit()
            print(f"\nTicket {ticket_id} creado exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_tickets():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT TicketID, TO_CHAR(OrderDate, 'YYYY-MM-DD HH24:MI'), StoreID, EmployeeID, CustomerID, PaymentID
            FROM TICKET
            ORDER BY TicketID
            """
            cursor.execute(sql)

            print("\n--- Tickets ---")
            print(f"\n{'ID':<10} {'FECHA':<15} {'TIENDA':<10} {'EMPLEADO':<12} {'CLIENTE':<10} {'PAGO':<10}")
            print("-" * 75)

            for row in cursor.fetchall():
                print(f"{row[0]:<10} {str(row[1]):<15} {str(row[2]):<10} {str(row[3]):<12} {str(row[4]):<10} {str(row[5]):<10}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_ticket_por_id(ticket_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT TicketID, TO_CHAR(OrderDate, 'YYYY-MM-DD HH24:MI'), StoreID, EmployeeID, CustomerID, PaymentID
            FROM TICKET
            WHERE TicketID = :1
            """
            cursor.execute(sql, (ticket_id,))
            row = cursor.fetchone()

            if row:
                print(f"\nTicket {ticket_id} encontrado:")
                print(f"ID: {row[0]}")
                print(f"Fecha: {row[1]}")
                print(f"Store ID: {row[2]}")
                print(f"Employee ID: {row[3]}")
                print(f"Customer ID: {row[4]}")
                print(f"Payment ID: {row[5]}")
            else:
                print(f"No se encontro el ticket {ticket_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def actualizar_ticket(ticket_id, nueva_order_date, nuevo_store_id, nuevo_employee_id, nuevo_customer_id, nuevo_payment_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            nueva_order_date = str(nueva_order_date).strip()
            if " " not in nueva_order_date:
                nueva_order_date = nueva_order_date + " 00:00"

            sql = """
            UPDATE TICKET
            SET OrderDate = TO_DATE(:1, 'YYYY-MM-DD HH24:MI'), StoreID = :2, EmployeeID = :3, CustomerID = :4, PaymentID = :5
            WHERE TicketID = :6
            """
            cursor.execute(sql, (nueva_order_date, nuevo_store_id, nuevo_employee_id, nuevo_customer_id, nuevo_payment_id, ticket_id))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nTicket {ticket_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el ticket {ticket_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar ticket: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_ticket(ticket_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT PaymentID FROM TICKET WHERE TicketID = :1", (ticket_id,))
            fila = cursor.fetchone()
            payment_id = fila[0] if fila else None

            cursor.execute("DELETE FROM ORDER_ITEM WHERE TicketID = :1", (ticket_id,))

            sql = "DELETE FROM TICKET WHERE TicketID = :1"
            cursor.execute(sql, (ticket_id,))

            if cursor.rowcount > 0:
                if payment_id is not None:
                    cursor.execute("DELETE FROM PAYMENT WHERE PaymentID = :1", (payment_id,))

                conexion.commit()
                print(f"\nTicket {ticket_id} eliminado exitosamente")
                return True
            else:
                print(f"\nNo se encontro ticket con ID {ticket_id}")
                return False

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar ticket: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    return False


# Funciones CRUD de la tabla ORDER_ITEM
def crear_order_item(order_item_id, quantity, comments, ticket_id, menu_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO ORDER_ITEM
            (OrderItemID, Quantity, Comments, TicketID, MenuItemID)
            VALUES (:1, :2, :3, :4, :5)
            """
            cursor.execute(sql, (order_item_id, quantity, comments, ticket_id, menu_item_id))
            conexion.commit()
            print(f"\nOrden item {order_item_id} creada exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_order_items():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT OrderItemID, Quantity, Comments, TicketID, MenuItemID
            FROM ORDER_ITEM
            ORDER BY OrderItemID
            """
            cursor.execute(sql)

            print("\n--- Detalle de ordenes ---")
            print(f"\n{'ID':<10} {'CANTIDAD':<12} {'COMENTARIOS':<30} {'TICKET':<10} {'MENU':<10}")
            print("-" * 85)

            for row in cursor.fetchall():
                print(f"{row[0]:<10} {str(row[1]):<12} {str(row[2]):<30} {str(row[3]):<10} {str(row[4]):<10}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_order_item_por_id(order_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT OrderItemID, Quantity, Comments, TicketID, MenuItemID
            FROM ORDER_ITEM
            WHERE OrderItemID = :1
            """
            cursor.execute(sql, (order_item_id,))
            row = cursor.fetchone()

            if row:
                print(f"\nOrder item {order_item_id} encontrado:")
                print(f"ID: {row[0]}")
                print(f"Cantidad: {row[1]}")
                print(f"Comentarios: {row[2]}")
                print(f"Ticket ID: {row[3]}")
                print(f"Menu Item ID: {row[4]}")
            else:
                print(f"No se encontro el order item {order_item_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def actualizar_order_item(order_item_id, nueva_quantity, nuevos_comments, nuevo_ticket_id, nuevo_menu_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE ORDER_ITEM
            SET Quantity = :1, Comments = :2, TicketID = :3, MenuItemID = :4
            WHERE OrderItemID = :5
            """
            cursor.execute(sql, (nueva_quantity, nuevos_comments, nuevo_ticket_id, nuevo_menu_item_id, order_item_id))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nOrder item {order_item_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el order item {order_item_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar order item: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_order_item(order_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM ORDER_ITEM WHERE OrderItemID = :1"
            cursor.execute(sql, (order_item_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nOrder item {order_item_id} eliminado exitosamente")
            else:
                print(f"\nNo se encontro order item con ID {order_item_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar order item: {e}")
        finally:
            cursor.close()
            conexion.close()


# Funciones CRUD de la tabla SUNDAE
def crear_sundae(custom_id, syrup, whipped_cream, mixeable, sauce_topping, placeable_topping, pourable_topping, menu_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO SUNDAE
            (CustomID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping, MenuItemID)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """
            cursor.execute(sql, (custom_id, syrup, whipped_cream, mixeable, sauce_topping, placeable_topping, pourable_topping, menu_item_id))
            conexion.commit()
            print(f"\nSundae {custom_id} creado exitosamente")
        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            cursor.close()
            conexion.close()


def leer_sundaes(mostrar=True, menu_item_id=None):
    conexion = conectar()
    cursor = None
    sundaes = []
    if conexion:
        try:
            cursor = conexion.cursor()
            if menu_item_id is None:
                sql = """
                SELECT CustomID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping, MenuItemID
                FROM SUNDAE
                ORDER BY CustomID
                """
                cursor.execute(sql)
            else:
                sql = """
                SELECT CustomID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping, MenuItemID
                FROM SUNDAE
                WHERE MenuItemID = :1
                ORDER BY CustomID
                """
                cursor.execute(sql, (menu_item_id,))

            sundaes = cursor.fetchall()

            if mostrar:
                print("\n--- Sundaes ---")
                print(f"\n{'ID':<8} {'SYRUP':<18} {'CREMA':<8} {'MIXEABLE':<18} {'SAUCE':<18} {'PLACEABLE':<18} {'POURABLE':<18} {'MENU':<8}")
                print("-" * 125)

                for row in sundaes:
                    print(f"{row[0]:<8} {str(row[1]):<18} {str(row[2]):<8} {str(row[3]):<18} {str(row[4]):<18} {str(row[5]):<18} {str(row[6]):<18} {str(row[7]):<8}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    return sundaes


def leer_sundae_por_id(custom_id, mostrar=True):
    conexion = conectar()
    cursor = None
    row = None
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT CustomID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping, MenuItemID
            FROM SUNDAE
            WHERE CustomID = :1
            """
            cursor.execute(sql, (custom_id,))
            row = cursor.fetchone()

            if mostrar:
                if row:
                    print(f"\nSundae {custom_id} encontrado:")
                    print(f"ID: {row[0]}")
                    print(f"Syrup: {row[1]}")
                    print(f"Whipped Cream: {row[2]}")
                    print(f"Mixeable: {row[3]}")
                    print(f"Sauce Topping: {row[4]}")
                    print(f"Placeable Topping: {row[5]}")
                    print(f"Pourable Topping: {row[6]}")
                    print(f"Menu Item ID: {row[7]}")
                else:
                    print(f"No se encontro el sundae {custom_id}")

        except oracledb.DatabaseError as e:
            print(f"Error de Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    return row


def actualizar_sundae(custom_id, nuevo_syrup, nuevo_whipped_cream, nuevo_mixeable, nuevo_sauce_topping, nuevo_placeable_topping, nuevo_pourable_topping, nuevo_menu_item_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE SUNDAE
            SET Syrup = :1, WhippedCream = :2, Mixeable = :3, SauceTopping = :4, PlaceableTopping = :5, PourableTopping = :6, MenuItemID = :7
            WHERE CustomID = :8
            """
            cursor.execute(sql, (nuevo_syrup, nuevo_whipped_cream, nuevo_mixeable, nuevo_sauce_topping, nuevo_placeable_topping, nuevo_pourable_topping, nuevo_menu_item_id, custom_id))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nSundae {custom_id} actualizado exitosamente")
            else:
                print(f"\nNo se encontro el sundae {custom_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al actualizar sundae: {e}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_sundae(custom_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM SUNDAE WHERE CustomID = :1"
            cursor.execute(sql, (custom_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\nSundae {custom_id} eliminado exitosamente")
            else:
                print(f"\nNo se encontro sundae con ID {custom_id}")

        except oracledb.DatabaseError as e:
            print(f"Error al eliminar sundae: {e}")
        finally:
            cursor.close()
            conexion.close()
