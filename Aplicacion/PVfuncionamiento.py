import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import random

from HeladeriaBD_CRUD import (
    conectar,
    crear_customer,
    crear_payment,
    crear_ticket,
    crear_order_item,
    crear_sundae,
    eliminar_ticket,
    leer_employees,
    leer_menu_items,
    leer_store_por_id,
    leer_sundaes,
    obtener_id_gerente
)

from PVdiseno import (
    COLOR_BORDE,
    COLOR_BOTON,
    COLOR_FONDO,
    COLOR_TEXTO,
    COLOR_TITULO,
    DisenoHeladeria,
    FUENTE_NORMAL,
    FUENTE_SUBTITULO,
    FUENTE_TITULO,
    cargar_imagen_alias,
    cargar_imagen_producto,
    comando_con_sonido,
    reproducir_sonido_ticket,
)


class PuntoVentaHeladeria(DisenoHeladeria):
    def __init__(self, root):
        self.root = root
        self.root.title("Besitos de Nuez - Heladeria")
        self.root.state("zoomed")
        self.root.configure(bg=COLOR_FONDO)
        self.configurar_icono_ventana(self.root, predeterminado=True)

        self.empleado = None
        self.cliente_id = None
        self.cliente_nombre = ""
        self.ticket_id = None
        self.payment_id = None
        self.carrito = []
        self.comentarios_generales = ""
        self.venta_habilitada = False
        self.botones_bloqueados = []

        self.mostrar_inicio()

    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def obtener_siguiente_id(self, tabla, columna):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = f"SELECT NVL(MAX({columna}), 0) + 1 FROM {tabla}"
                cursor.execute(sql)
                return cursor.fetchone()[0]
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo obtener ID:\n{e}")
                return 1
            finally:
                cursor.close()
                conexion.close()
        return 1

    def obtener_ingredientes_producto(self, menu_item_id):
        ingredientes = []
        sundaes = leer_sundaes(mostrar=False, menu_item_id=menu_item_id)
        fila = sundaes[0][1:7] if sundaes else None

        if fila:
            campos = [
                ("Syrup", "Syrup"),
                ("WhippedCream", "Crema Batida"),
                ("Mixeable", "Mezclable"),
                ("SauceTopping", "Salsa"),
                ("PlaceableTopping", "Topping Solido"),
                ("PourableTopping", "Topping Liquido")
            ]

            for (campo_bd, campo_texto), valor in zip(campos, fila):
                if valor is not None and str(valor).strip() != "":
                    if campo_bd == "WhippedCream":
                        valor_texto = str(valor).strip()
                        if valor_texto in ["1", "1.0"]:
                            valor = "Si"
                        elif valor_texto in ["0", "0.0"]:
                            valor = "No"
                    ingredientes.append(f"{campo_texto}: {valor}")

        return ingredientes

    def mostrar_inicio(self):
        self.limpiar()
        frame = self.marco_centrado()

        self.logo_inicio = cargar_imagen_alias("Logo.png", 330, 265)
        if self.logo_inicio:
            tk.Label(
                frame,
                image=self.logo_inicio,
                bg=COLOR_FONDO
            ).pack(pady=(15, 10))
        else:
            self.titulo(frame)

        self.boton(frame, "Inicio", self.iniciar_venta, 15).pack(pady=10)
        self.boton(frame, "Mostrar Tickets", self.mostrar_tickets_bd, 18).pack(pady=5)

    def iniciar_venta(self): #inicia el proceso de venta, reseteando variables y mostrando el punto de venta
        self.empleado = None
        self.cliente_id = None
        self.cliente_nombre = ""
        self.ticket_id = None
        self.payment_id = None
        self.carrito = []
        self.comentarios_generales = ""
        self.venta_habilitada = False
        self.mostrar_punto_venta(abrir_cajeros=True)

    def nueva_orden_desde_menu(self): #
        if self.empleado is None:
            self.iniciar_venta()
            return

        self.cliente_id = None
        self.cliente_nombre = ""
        self.ticket_id = None
        self.payment_id = None
        self.carrito = []
        self.comentarios_generales = ""
        self.venta_habilitada = False
        self.mostrar_punto_venta()
        self.root.after(100, self.mostrar_cliente_popup)

    def venta_lista(self):
        return (
            self.venta_habilitada
            and self.empleado is not None
            and self.cliente_id is not None
            and self.cliente_nombre.strip() != ""
            and self.ticket_id is not None
        )

    def validar_venta_lista(self):
        if self.venta_lista():
            return True

        messagebox.showwarning(
            "Venta bloqueada",
            "Selecciona cajero, escribe la contrasena correcta y registra el nombre del cliente."
        )
        return False

    def registrar_boton_bloqueado(self, boton):
        self.botones_bloqueados.append(boton)
        return boton

    def actualizar_estado_trabajo(self):
        estado = "normal" if self.venta_lista() else "disabled"

        for boton in getattr(self, "botones_bloqueados", []):
            try:
                boton.config(state=estado)
            except tk.TclError:
                pass

        if hasattr(self, "txt_comentarios"):
            self.txt_comentarios.config(state=estado)

    def actualizar_encabezado_venta(self):
        cajero = self.empleado[1] if self.empleado else ""
        cliente = self.cliente_nombre if self.cliente_nombre else ""
        ticket = self.ticket_id if self.ticket_id is not None else ""

        if hasattr(self, "lbl_cajero"):
            self.lbl_cajero.config(text=f"Cajero: {cajero}")
        if hasattr(self, "lbl_cliente"):
            self.lbl_cliente.config(text=f"Cliente: {cliente}")
        if hasattr(self, "lbl_ticket"):
            self.lbl_ticket.config(text=f"Ticket #: {ticket}")

    def mostrar_cajeros_popup(self):
        empleados = leer_employees(mostrar=False)

        def cerrar():
            ventana.destroy()
            self.mostrar_inicio()

        ventana = self.crear_modal("Seleccionar cajero", 460, 390, cerrar)

        tk.Label(
            ventana,
            text="Seleccione cajero",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(pady=(4, 3))

        lista = tk.Listbox(
            ventana,
            width=32,
            height=6,
            font=FUENTE_NORMAL,
            **self.borde_suave()
        )
        lista.pack(pady=5)
        lista.focus_set()

        for emp in empleados:
            lista.insert(tk.END, emp[1])

        if not empleados:
            lista.insert(tk.END, "No se encontraron cajeros")

        def siguiente():
            seleccion = lista.curselection()
            if not empleados:
                messagebox.showwarning("Aviso", "No hay empleados cargados en la base de datos")
                return
            if not seleccion:
                messagebox.showwarning("Aviso", "Selecciona un cajero")
                return

            self.empleado = empleados[seleccion[0]]
            self.actualizar_encabezado_venta()
            ventana.destroy()
            self.mostrar_password_popup()

        ventana.bind("<Return>", lambda _evento: siguiente())

        botones = tk.Frame(ventana, bg=COLOR_FONDO)
        botones.pack(fill="x", padx=24, pady=12)
        self.boton(botones, "Regresar", cerrar, 10).pack(side="left")
        self.boton(botones, "Siguiente", siguiente, 10).pack(side="right")

    def mostrar_password_popup(self):
        def regresar():
            ventana.destroy()
            self.empleado = None
            self.actualizar_encabezado_venta()
            self.mostrar_cajeros_popup()

        ventana = self.crear_modal("Contrasena de cajero", 460, 320, regresar)

        tk.Label(
            ventana,
            text="Escriba la contraseña",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(pady=(12, 6))

        entrada = tk.Entry(
            ventana,
            font=FUENTE_NORMAL,
            width=26,
            justify="center",
            show="*",
            **self.borde_suave()
        )
        entrada.pack(pady=4)
        entrada.focus_set()

        def siguiente():
            if entrada.get().strip() == str(self.empleado[0]):
                ventana.destroy()
                self.mostrar_cliente_popup()
            else:
                messagebox.showerror("Error", "Contrasena incorrecta")
                entrada.delete(0, tk.END)
                entrada.focus_set()

        entrada.bind("<Return>", lambda _evento: siguiente())

        botones = tk.Frame(ventana, bg=COLOR_FONDO)
        botones.pack(fill="x", padx=24, pady=24)
        self.boton(botones, "Regresar", regresar, 10).pack(side="left")
        self.boton(botones, "Siguiente", siguiente, 10).pack(side="right")

    def mostrar_cliente_popup(self):
        def regresar():
            ventana.destroy()
            self.mostrar_password_popup()

        ventana = self.crear_modal("Nombre del cliente", 460, 320, regresar)

        tk.Label(
            ventana,
            text="Nombre del cliente",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(pady=(12, 6))

        entrada = tk.Entry(
            ventana,
            font=FUENTE_NORMAL,
            width=28,
            justify="center",
            **self.borde_suave()
        )
        entrada.pack(pady=4)
        entrada.focus_set()

        def siguiente():
            nombre = entrada.get().strip()
            if nombre == "":
                messagebox.showwarning("Aviso", "Escribe el nombre del cliente")
                entrada.focus_set()
                return

            self.cliente_nombre = nombre
            self.cliente_id = self.obtener_siguiente_id("CUSTOMERS", "CustomerID")
            self.ticket_id = self.obtener_siguiente_id("TICKET", "TicketID")
            self.carrito = []
            self.venta_habilitada = True
            self.actualizar_encabezado_venta()
            self.actualizar_carrito()
            self.actualizar_estado_trabajo()
            ventana.destroy()

        entrada.bind("<Return>", lambda _evento: siguiente())

        botones = tk.Frame(ventana, bg=COLOR_FONDO)
        botones.pack(fill="x", padx=24, pady=24)
        self.boton(botones, "Regresar", regresar, 10).pack(side="left")
        self.boton(botones, "Siguiente", siguiente, 10).pack(side="right")

        def validar():
            if entrada_id.get().strip() == str(self.empleado[0]):
                self.mostrar_nueva_orden()
            else:
                messagebox.showerror("Error", "ID incorrecto")

        self.boton(frame, "Entrar", validar, 10).pack(pady=8)
        self.boton(frame, "Regresar", self.mostrar_empleados, 10).pack()

    def mostrar_nueva_orden(self):
        self.nueva_orden_desde_menu()
        
        def crear_boton_producto(item, fila, columna, comando):
            imagen_producto = cargar_imagen_producto(
                item[1],
                ancho_imagen_menu,
                alto_imagen_menu
            )

            producto_frame = tk.Frame(
                menu_frame,
                bg=COLOR_FONDO,
                width=ancho_imagen_menu,
                height=150
            )
            producto_frame.grid_propagate(False)
            producto_frame.grid(row=fila, column=columna, padx=15, pady=(0, 10))

            if imagen_producto:
                self.imagenes_productos_menu.append(imagen_producto)
                btn = tk.Button(
                    producto_frame,
                    image=imagen_producto,
                    bg=COLOR_FONDO,
                    activebackground=COLOR_FONDO,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=0,
                    pady=0,
                    cursor="hand2",
                    command=comando
                )
            else:
                btn = tk.Button(
                    producto_frame,
                    text=str(item[1]),
                    font=("Comic Sans MS", 10),
                    fg=COLOR_TEXTO,
                    bg=COLOR_FONDO,
                    activebackground=COLOR_FONDO,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    wraplength=ancho_imagen_menu,
                    cursor="hand2",
                    command=comando
                )

            btn.pack()

            tk.Label(
                producto_frame,
                text=f"${float(item[2]):.2f}",
                font=("Comic Sans MS", 10),
                fg=COLOR_TEXTO,
                bg=COLOR_FONDO
            ).pack(pady=(2, 0))

        productos_menu = [
            item for item in menu
            if str(item[1]).strip().lower() not in ["make your own", "make your own sundae"]
        ]

        for i, item in enumerate(productos_menu[:15]):
            crear_boton_producto(
                item,
                i // 4,
                i % 4,
                comando_con_sonido(lambda p=item: self.seleccionar_producto_menu(p))
            )

        item_custom = None
        for item in menu:
            if str(item[1]).strip().lower() in ["make your own", "make your own sundae"]:
                item_custom = item
                break

        if item_custom:
            item_custom_boton = item_custom
        elif menu:
            item_custom_boton = (None, "Make your own", menu[-1][2], "")
        else:
            item_custom_boton = None

        if item_custom_boton:
            crear_boton_producto(
                item_custom_boton,
                3,
                3,
                comando_con_sonido(lambda: self.seleccionar_custom_menu(menu))
            )

        detalle_frame = tk.Frame(menu_frame, bg=COLOR_FONDO)
        detalle_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=15, pady=(8, 0))

        tk.Label(
            detalle_frame,
            text="Descripcion e ingredientes",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="w")

        self.txt_detalle_producto = tk.Text(
            detalle_frame,
            width=92,
            height=7,
            font=("Comic Sans MS", 10),
            wrap="word",
            **self.borde_suave()
        )
        self.txt_detalle_producto.pack(fill="x", pady=(4, 0))
        self.txt_detalle_producto.config(state="disabled")

        self.actualizar_carrito()

    def mostrar_punto_venta(self, abrir_cajeros=False):
        self.limpiar()
        self.botones_bloqueados = []

        frame = tk.Frame(self.root, bg=COLOR_FONDO, **self.borde_suave())
        frame.pack(fill="both", expand=True, padx=16, pady=12)

        encabezado = tk.Frame(frame, bg=COLOR_FONDO, **self.borde_suave())
        encabezado.place(relx=0.405, y=18, anchor="n", relwidth=0.72, height=58)

        self.lbl_cajero = tk.Label(
            encabezado,
            text="Cajero: ",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="w"
        )
        self.lbl_cajero.place(x=12, y=6, width=340, height=22)

        self.lbl_cliente = tk.Label(
            encabezado,
            text="Cliente: ",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="w"
        )
        self.lbl_cliente.place(x=12, y=29, width=340, height=22)

        self.lbl_ticket = tk.Label(
            encabezado,
            text="Ticket #: ",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="e"
        )
        self.lbl_ticket.place(relx=0.57, y=16, relwidth=0.4, height=24)

        self.boton(frame, "Nueva\norden", self.nueva_orden_desde_menu, 9, 2).place(relx=0.84, y=18, anchor="n")
        self.boton(frame, "Salir", self.mostrar_inicio, 8, 2).place(relx=0.92, y=18, anchor="n")

        panel = tk.Frame(frame, bg=COLOR_FONDO, **self.borde_suave())
        panel.place(relx=0.1775, y=90, anchor="n", relwidth=0.265, height=535)

        tk.Label(
            panel,
            text="PRODUCTOS",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="w", padx=12, pady=(10, 0))

        self.lista_carrito = tk.Listbox(
            panel,
            width=44,
            height=9,
            font=("Courier New", 10),
            **self.borde_suave()
        )
        self.lista_carrito.pack(fill="x", padx=14, pady=5)

        controles = tk.Frame(panel, bg=COLOR_FONDO)
        controles.pack(anchor="center", pady=(2, 8))

        self.registrar_boton_bloqueado(
            self.boton(controles, "Quitar", self.quitar_producto, 9)
        ).grid(row=0, column=0, padx=6)
        self.registrar_boton_bloqueado(
            self.boton(controles, "+", self.aumentar_producto, 3)
        ).grid(row=0, column=1, padx=6)
        self.registrar_boton_bloqueado(
            self.boton(controles, "-", self.disminuir_producto, 3)
        ).grid(row=0, column=2, padx=6)

        tk.Label(
            panel,
            text="Comentarios",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="w", padx=12)

        self.txt_comentarios = tk.Text(
            panel,
            width=40,
            height=3,
            font=("Comic Sans MS", 10),
            **self.borde_suave()
        )
        self.txt_comentarios.pack(fill="x", padx=14, pady=(0, 10))

        self.lbl_total = tk.Label(
            panel,
            text="Total: $0.00",
            font=("Comic Sans MS", 20, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        )
        self.lbl_total.pack(pady=(6, 6))

        pagos_contenido = tk.Frame(panel, bg=COLOR_FONDO)
        pagos_contenido.pack(anchor="center", pady=(10, 0))

        self.registrar_boton_bloqueado(
            self.boton(pagos_contenido, "Efectivo", self.pagar_cash, 10, 2)
        ).pack(side="left", padx=8)
        self.registrar_boton_bloqueado(
            self.boton(pagos_contenido, "Tarjeta", self.pagar_card, 10, 2)
        ).pack(side="left", padx=8)

        self.logo_venta = cargar_imagen_alias("Logo.png", 370, 250)
        if self.logo_venta:
            tk.Label(
                frame,
                image=self.logo_venta,
                bg=COLOR_FONDO,
                bd=0,
                highlightthickness=0
            ).place(relx=0.1775, y=640, anchor="n")

        color_panel_menu = "#fffdf8"
        menu_frame = tk.Frame(frame, bg=color_panel_menu, **self.borde_suave())
        menu_frame.place(relx=0.63, y=90, anchor="n", relwidth=0.61, height=535)

        for columna in range(4):
            menu_frame.grid_columnconfigure(columna, weight=1, uniform="productos")

        menu = leer_menu_items(mostrar=False)

        if not menu:
            messagebox.showwarning("Sin menu", "No se pudieron cargar productos desde MENU_ITEM")

        self.imagenes_productos_menu = []
        ancho_imagen_menu = 150
        alto_imagen_menu = 95

        def crear_boton_producto(item, fila, columna, comando):
            imagen_producto = cargar_imagen_producto(
                item[1],
                ancho_imagen_menu,
                alto_imagen_menu
            )

            producto_frame = tk.Frame(
                menu_frame,
                bg=color_panel_menu,
                width=ancho_imagen_menu,
                height=120
            )
            producto_frame.grid_propagate(False)
            producto_frame.grid(row=fila, column=columna, padx=42, pady=(6, 0))

            if imagen_producto:
                self.imagenes_productos_menu.append(imagen_producto)
                btn = tk.Button(
                    producto_frame,
                    image=imagen_producto,
                    bg=color_panel_menu,
                    activebackground=color_panel_menu,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=0,
                    pady=0,
                    cursor="hand2",
                    command=comando
                )
            else:
                btn = tk.Button(
                    producto_frame,
                    text=str(item[1]),
                    font=("Comic Sans MS", 10),
                    fg=COLOR_TEXTO,
                    bg=color_panel_menu,
                    activebackground=color_panel_menu,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    wraplength=ancho_imagen_menu,
                    cursor="hand2",
                    command=comando
                )

            self.registrar_boton_bloqueado(btn)
            btn.pack()

            tk.Label(
                producto_frame,
                text=f"${float(item[2]):.2f}",
                font=("Comic Sans MS", 10),
                fg=COLOR_TEXTO,
                bg=color_panel_menu
            ).pack(pady=(2, 0))

        productos_menu = [
            item for item in menu
            if str(item[1]).strip().lower() not in ["make your own", "make your own sundae"]
        ]

        for i, item in enumerate(productos_menu[:15]):
            crear_boton_producto(
                item,
                i // 4,
                i % 4,
                comando_con_sonido(lambda p=item: self.seleccionar_producto_menu(p))
            )

        item_custom = None
        for item in menu:
            if str(item[1]).strip().lower() in ["make your own", "make your own sundae"]:
                item_custom = item
                break

        if item_custom:
            item_custom_boton = item_custom
        elif menu:
            item_custom_boton = (None, "Make your own", menu[-1][2], "")
        else:
            item_custom_boton = None

        if item_custom_boton:
            crear_boton_producto(
                item_custom_boton,
                3,
                3,
                comando_con_sonido(lambda: self.seleccionar_custom_menu(menu))
            )

        detalle_frame = tk.Frame(frame, bg=COLOR_FONDO, **self.borde_suave())
        detalle_frame.place(relx=0.63, y=640, anchor="n", relwidth=0.61, height=235)

        tk.Label(
            detalle_frame,
            text="Descripcion e ingredientes:",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="center", pady=(8, 0))

        self.txt_detalle_producto = tk.Text(
            detalle_frame,
            width=84,
            height=6,
            font=("Comic Sans MS", 10),
            wrap="word",
            **self.borde_suave()
        )
        self.txt_detalle_producto.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        self.txt_detalle_producto.config(state="disabled")

        self.actualizar_encabezado_venta()
        self.actualizar_carrito()
        self.actualizar_estado_trabajo()

        if abrir_cajeros:
            self.root.after(100, self.mostrar_cajeros_popup)

    def seleccionar_producto_menu(self, item):
        if not self.validar_venta_lista():
            return

        self.mostrar_detalle_producto(item)
        self.agregar_producto(item)

    def seleccionar_custom_menu(self, menu):
        if not self.validar_venta_lista():
            return

        item_custom = None

        for item in menu:
            if str(item[1]).strip().lower() in ["make your own", "make your own sundae"]:
                item_custom = item
                break

        if item_custom:
            self.mostrar_detalle_producto(item_custom)

        self.mostrar_custom()

    def mostrar_detalle_producto(self, item):
        if not hasattr(self, "txt_detalle_producto"):
            return

        descripcion = ""
        if len(item) > 3 and item[3]:
            descripcion = str(item[3])

        ingredientes = self.obtener_ingredientes_producto(item[0])

        texto = f"{item[1]}\n\n"
        texto += "Descripcion:\n"
        texto += f"{descripcion if descripcion else 'Sin descripcion registrada'}\n\n"
        texto += "Ingredientes:\n"

        if ingredientes:
            for ingrediente in ingredientes:
                texto += f"- {ingrediente}\n"
        else:
            texto += "Sin ingredientes registrados"

        self.txt_detalle_producto.config(state="normal")
        self.txt_detalle_producto.delete("1.0", tk.END)
        self.txt_detalle_producto.insert(tk.END, texto)
        self.txt_detalle_producto.config(state="disabled")

    def agregar_producto(self, item):
        if not self.validar_venta_lista():
            return

        menu_item_id = item[0]
        nombre = item[1]
        precio = float(item[2])

        for producto in self.carrito:
            if producto["menu_item_id"] == menu_item_id and producto["comments"] == "":
                producto["cantidad"] += 1
                self.actualizar_carrito()
                return

        self.carrito.append({
            "menu_item_id": menu_item_id,
            "nombre": nombre,
            "precio": precio,
            "cantidad": 1,
            "comments": "",
            "custom": False,
            "custom_data": None
        })

        self.actualizar_carrito()

    def mostrar_custom(self):
        if not self.validar_venta_lista():
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Make your own")
        ventana.geometry("430x620")
        ventana.minsize(430, 620)
        ventana.configure(bg=COLOR_FONDO)
        self.configurar_icono_ventana(ventana)

        tk.Label(
            ventana,
            text="Make your own",
            font=FUENTE_SUBTITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(pady=15)

        opciones = {
            "Syrup": ["Fresa", "Chocolate", "Vainilla", "Caramelo"],
            "WhippedCream": ["Si", "No"],
            "Mixeable": ["Moras", "Brownie", "Galleta", "Chispas"],
            "SauceTopping": ["Cajeta", "Nutella", "Chocolate", "Fresa"],
            "PlaceableTopping": ["Chispas", "Gomitas", "Nuez", "Cereal"],
            "PourableTopping": ["Caramelo", "Chocolate", "Lechera", "Miel"]
        }

        campos = {}

        for nombre, valores in opciones.items():
            tk.Label(
                ventana,
                text=nombre,
                font=FUENTE_NORMAL,
                bg=COLOR_FONDO
            ).pack()

            var = tk.StringVar()
            var.set(valores[0])
            campos[nombre] = var

            opcion = tk.OptionMenu(ventana, var, *valores)
            opcion.config(
                font=FUENTE_NORMAL,
                fg=COLOR_TEXTO,
                bg=COLOR_BOTON,
                activebackground=COLOR_BOTON,
                relief="flat",
                bd=0,
                highlightbackground=COLOR_BORDE,
                highlightcolor=COLOR_BORDE,
                highlightthickness=1
            )
            opcion["menu"].config(
                fg=COLOR_TEXTO,
                bg=COLOR_FONDO,
                activebackground=COLOR_BOTON,
                bd=0
            )
            opcion.pack(fill="x", padx=70, pady=3)

        def agregar_custom():
            if not self.validar_venta_lista():
                return

            menu = leer_menu_items(mostrar=False)

            if not menu:
                messagebox.showerror("Error", "No hay productos cargados en MENU_ITEM")
                return

            item_custom = None

            for item in menu:
                if str(item[1]).strip().lower() in ["make your own", "make your own sundae"]:
                    item_custom = item
                    break

            if item_custom is None:
                item_custom = menu[-1]

            menu_item_id = item_custom[0]
            precio = float(item_custom[2])

            custom_data = {
                "Syrup": campos["Syrup"].get(),
                "WhippedCream": campos["WhippedCream"].get(),
                "Mixeable": campos["Mixeable"].get(),
                "SauceTopping": campos["SauceTopping"].get(),
                "PlaceableTopping": campos["PlaceableTopping"].get(),
                "PourableTopping": campos["PourableTopping"].get()
            }

            comentarios = (
                f"Syrup: {custom_data['Syrup']}\n"
                f"WhippedCream: {custom_data['WhippedCream']}\n"
                f"Mixeable: {custom_data['Mixeable']}\n"
                f"SauceTopping: {custom_data['SauceTopping']}\n"
                f"PlaceableTopping: {custom_data['PlaceableTopping']}\n"
                f"PourableTopping: {custom_data['PourableTopping']}"
            )

            self.carrito.append({
                "menu_item_id": menu_item_id,
                "nombre": "Make your own",
                "precio": precio,
                "cantidad": 1,
                "comments": comentarios,
                "custom": True,
                "custom_data": custom_data
            })

            self.actualizar_carrito()
            ventana.destroy()

        self.boton(ventana, "Agregar", agregar_custom, 16).pack(pady=18)

    def actualizar_carrito(self):
        self.lista_carrito.delete(0, tk.END)

        total = 0

        for producto in self.carrito:
            subtotal = producto["precio"] * producto["cantidad"]
            total += subtotal
            texto = f"{producto['cantidad']} x {producto['nombre'][:20]:20} ${subtotal:7.2f}"
            self.lista_carrito.insert(tk.END, texto)

        self.lbl_total.config(text=f"Total: ${total:.2f}")

    def producto_seleccionado(self):
        seleccion = self.lista_carrito.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return None
        return seleccion[0]

    def quitar_producto(self):
        if not self.validar_venta_lista():
            return

        indice = self.producto_seleccionado()
        if indice is not None:
            self.carrito.pop(indice)
            self.actualizar_carrito()

    def aumentar_producto(self):
        if not self.validar_venta_lista():
            return

        indice = self.producto_seleccionado()
        if indice is not None:
            self.carrito[indice]["cantidad"] += 1
            self.actualizar_carrito()

    def disminuir_producto(self):
        if not self.validar_venta_lista():
            return

        indice = self.producto_seleccionado()
        if indice is not None:
            if self.carrito[indice]["cantidad"] > 1:
                self.carrito[indice]["cantidad"] -= 1
            else:
                self.carrito.pop(indice)
            self.actualizar_carrito()

    def calcular_total(self):
        total = 0
        for producto in self.carrito:
            total += producto["precio"] * producto["cantidad"]
        return total

    def pagar_cash(self):
        if not self.validar_venta_lista():
            return

        if not self.carrito:
            messagebox.showwarning("Aviso", "Agrega productos primero")
            return

        total = self.calcular_total()

        pagado = simpledialog.askfloat("Payment - Cash", f"Total: ${total:.2f}\nPaid:")
        if pagado is None:
            return

        if pagado < total:
            messagebox.showerror("Error", "El pago es menor al total")
            return

        cambio = pagado - total

        self.guardar_venta(1, total, pagado, cambio)
        self.mostrar_ticket("Cash", total, pagado=pagado, cambio=cambio)

    def pagar_card(self):
        if not self.validar_venta_lista():
            return

        if not self.carrito:
            messagebox.showwarning("Aviso", "Agrega productos primero")
            return

        total = self.calcular_total()
        tarjeta = str(random.randint(1000, 9999))

        self.guardar_venta(0, total, tarjeta=tarjeta)
        self.mostrar_ticket("Card", total, tarjeta=tarjeta)

    def guardar_venta(self, is_cash, total, recibido=None, cambio=None, tarjeta=None):
        self.payment_id = self.obtener_siguiente_id("PAYMENT", "PaymentID")

        crear_customer(self.cliente_id, self.cliente_nombre)
        crear_payment(self.payment_id, is_cash, total, recibido, cambio, tarjeta)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        store_id = self.empleado[3] if self.empleado[3] is not None else 1

        crear_ticket(
            self.ticket_id,
            fecha,
            store_id,
            self.empleado[0],
            self.cliente_id,
            self.payment_id
        )

        comentarios_generales = ""

        if hasattr(self, "txt_comentarios"):
            comentarios_generales = self.txt_comentarios.get("1.0", "end").strip()

        self.comentarios_generales = comentarios_generales

        for producto in self.carrito:
            order_item_id = self.obtener_siguiente_id("ORDER_ITEM", "OrderItemID")

            comentarios_producto = producto["comments"]

            if comentarios_generales:
                if comentarios_producto:
                    comentarios_producto = comentarios_producto + "\nComentarios: " + comentarios_generales
                else:
                    comentarios_producto = comentarios_generales

            crear_order_item(
                order_item_id,
                producto["cantidad"],
                comentarios_producto,
                self.ticket_id,
                producto["menu_item_id"]
            )

            if producto["custom"] and producto["custom_data"]:
                custom_id = self.obtener_siguiente_id("SUNDAE", "CustomID")
                data = producto["custom_data"]

                crear_sundae(
                    custom_id,
                    data["Syrup"],
                    data["WhippedCream"],
                    data["Mixeable"],
                    data["SauceTopping"],
                    data["PlaceableTopping"],
                    data["PourableTopping"],
                    producto["menu_item_id"]
                )

    def mostrar_ticket(self, metodo, total, pagado=None, cambio=None, tarjeta=None):
        self.limpiar()

        frame = tk.Frame(self.root, bg=COLOR_FONDO)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Ticket",
            font=FUENTE_TITULO,
            fg=COLOR_TITULO,
            bg=COLOR_FONDO
        ).pack(pady=(10, 10))

        canvas_ticket = self.crear_ticket_visual(frame, "ticket_impresion_imagen")

        texto = self.crear_buffer_texto_ticket()
        texto.insert(tk.END, "BESITOS DE NUEZ\n")
        texto.insert(tk.END, "Heladeria\n")
        texto.insert(tk.END, "-" * 42 + "\n")
        texto.insert(tk.END, f"Ticket: {self.ticket_id}\n")
        texto.insert(tk.END, f"Empleado: {self.empleado[1]}\n")
        store_id = self.empleado[3] if self.empleado[3] is not None else 1
        tienda = leer_store_por_id(store_id, mostrar=False)
        nombre_tienda = tienda[1] if tienda and tienda[1] else f"Tienda {store_id}"
        texto.insert(tk.END, f"Tienda: {nombre_tienda}\n")
        texto.insert(tk.END, f"Cliente: {self.cliente_nombre}\n")
        texto.insert(tk.END, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        texto.insert(tk.END, "-" * 42 + "\n")

        for producto in self.carrito:
            subtotal = producto["precio"] * producto["cantidad"]
            texto.insert(tk.END, f"{producto['cantidad']} x {producto['nombre'][:20]:20} ${subtotal:7.2f}\n")

            if producto["custom"] and producto["custom_data"]:
                data = producto["custom_data"]
                texto.insert(tk.END, f"   Syrup: {data['Syrup']}\n")
                texto.insert(tk.END, f"   WhippedCream: {data['WhippedCream']}\n")
                texto.insert(tk.END, f"   Mixeable: {data['Mixeable']}\n")
                texto.insert(tk.END, f"   SauceTopping: {data['SauceTopping']}\n")
                texto.insert(tk.END, f"   PlaceableTopping: {data['PlaceableTopping']}\n")
                texto.insert(tk.END, f"   PourableTopping: {data['PourableTopping']}\n")

        if self.comentarios_generales:
            texto.insert(tk.END, "-" * 42 + "\n")
            texto.insert(tk.END, "Comentarios:\n")
            texto.insert(tk.END, f"{self.comentarios_generales}\n")

        texto.insert(tk.END, "-" * 42 + "\n")
        texto.insert(tk.END, f"Metodo: {metodo}\n")
        texto.insert(tk.END, f"TOTAL: ${total:.2f}\n")

        if metodo == "Cash":
            texto.insert(tk.END, f"Recibido: ${pagado:.2f}\n")
            texto.insert(tk.END, f"Cambio: ${cambio:.2f}\n")
        else:
            texto.insert(tk.END, f"Card: **** **** **** {tarjeta}\n")

        texto.insert(tk.END, "\nGracias por su compra :)\n")
        texto.config(state="disabled")
        self.escribir_ticket_visual(
            canvas_ticket,
            texto.obtener_texto()
        )
        reproducir_sonido_ticket()

        botones = tk.Frame(frame, bg=COLOR_FONDO)
        botones.pack(pady=15)

        self.boton(botones, "Nueva orden", self.mostrar_nueva_orden, 14).grid(row=0, column=0, padx=10)
        self.boton(botones, "Inicio", self.mostrar_inicio, 14).grid(row=0, column=1, padx=10)

    def obtener_tickets_bd(self):
        conexion = conectar()
        tickets = []

        if conexion:
            try:
                cursor = conexion.cursor()

                sql_tickets = """
                SELECT 
                    T.TicketID,
                    T.OrderDate,
                    E.Name,
                    C.Name,
                    S.StoreName,
                    P.Is_Cash,
                    P.Amount,
                    T.PaymentID
                FROM TICKET T
                LEFT JOIN EMPLOYEE E ON T.EmployeeID = E.EmployeeID
                LEFT JOIN CUSTOMERS C ON T.CustomerID = C.CustomerID
                LEFT JOIN PAYMENT P ON T.PaymentID = P.PaymentID
                LEFT JOIN STORE S ON T.StoreID = S.StoreID
                ORDER BY T.TicketID
                """

                cursor.execute(sql_tickets)
                filas_tickets = cursor.fetchall()

                for fila in filas_tickets:
                    ticket_id = fila[0]
                    payment_id = fila[7]
                    received = None
                    payment_change = None
                    card = None

                    if payment_id is not None and fila[5] is not None:
                        if int(fila[5]) == 1:
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

                    sql_productos = """
                    SELECT 
                        OI.Quantity,
                        M.Name,
                        M.Price,
                        OI.Comments
                    FROM ORDER_ITEM OI
                    LEFT JOIN MENU_ITEM M ON OI.MenuItemID = M.MenuItemID
                    WHERE OI.TicketID = :1
                    ORDER BY OI.OrderItemID
                    """

                    cursor.execute(sql_productos, (ticket_id,))
                    productos = cursor.fetchall()

                    tickets.append({
                        "ticket_id": fila[0],
                        "fecha": fila[1],
                        "empleado": fila[2],
                        "cliente": fila[3],
                        "store_name": fila[4] if fila[4] else "Desconocida",
                        "is_cash": fila[5],
                        "total": float(fila[6]) if fila[6] is not None else 0,
                        "received": float(received) if received is not None else None,
                        "payment_change": float(payment_change) if payment_change is not None else None,
                        "card": str(card).split(".")[0] if card is not None else None,
                        "productos": productos
                    })

            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar los tickets:\n{e}")

            finally:
                cursor.close()
                conexion.close()

        return tickets

    def mostrar_tickets_bd(self):
        self.limpiar()
        self.tickets_bd = self.obtener_tickets_bd()
        self.ticket_actual_indice = 0

        frame = tk.Frame(self.root, bg=COLOR_FONDO)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Tickets",
            font=FUENTE_TITULO,
            fg=COLOR_TITULO,
            bg=COLOR_FONDO
        ).pack(pady=(10, 10))

        contenido_tickets = tk.Frame(frame, bg=COLOR_FONDO)
        contenido_tickets.pack(anchor="center", padx=(110, 0))

        ticket_columna = tk.Frame(contenido_tickets, bg=COLOR_FONDO)
        ticket_columna.pack(side="left")

        acciones_tickets = tk.Frame(contenido_tickets, bg=COLOR_FONDO)
        acciones_tickets.pack(side="left", padx=(24, 0), pady=(40, 0), anchor="n")

        self.canvas_tickets = self.crear_ticket_visual(ticket_columna, "ticket_consulta_imagen")
        self.texto_tickets = self.crear_buffer_texto_ticket()
        self.boton(acciones_tickets, "Borrar Ticket", self.borrar_ticket_actual, 14).pack()

        botones_nav = tk.Frame(ticket_columna, bg=COLOR_FONDO)
        botones_nav.pack(pady=8)

        self.boton(botones_nav, "Anterior", self.ticket_anterior, 12).grid(row=0, column=0, padx=8)
        self.lbl_contador_tickets = tk.Label(
            botones_nav,
            text="",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            width=18
        )
        self.lbl_contador_tickets.grid(row=0, column=1, padx=8)
        self.boton(botones_nav, "Siguiente", self.ticket_siguiente, 12).grid(row=0, column=2, padx=8)

        self.boton(ticket_columna, "Inicio", self.mostrar_inicio, 14).pack(pady=10)
        self.imprimir_ticket_bd()

    def borrar_ticket_actual(self):
        if not self.tickets_bd:
            messagebox.showwarning("Aviso", "No hay tickets para borrar")
            return

        id_gerente = obtener_id_gerente()
        if id_gerente is None:
            messagebox.showerror("Error", "No se encontro un gerente en EMPLOYEE")
            return

        id_ingresado = simpledialog.askstring(
            "Contraseña del empleado",
            "Ingrese ID del gerente:",
            show="*"
        )

        if id_ingresado is None:
            return

        try:
            id_ingresado = int(id_ingresado.strip())
        except ValueError:
            messagebox.showerror("Error", "ID de gerente incorrecto")
            return

        if id_ingresado != id_gerente:
            messagebox.showerror("Error", "ID de gerente incorrecto")
            return

        ticket_id = self.tickets_bd[self.ticket_actual_indice]["ticket_id"]

        if eliminar_ticket(ticket_id):
            messagebox.showinfo("Aviso", "Ticket borrado correctamente")
            self.tickets_bd = self.obtener_tickets_bd()

            if self.ticket_actual_indice >= len(self.tickets_bd):
                self.ticket_actual_indice = max(len(self.tickets_bd) - 1, 0)

            self.imprimir_ticket_bd()
        else:
            messagebox.showerror("Error", "No se pudo borrar el ticket")

    def imprimir_ticket_bd(self):
        self.texto_tickets.config(state="normal")
        self.texto_tickets.delete("1.0", tk.END)

        if not self.tickets_bd:
            self.texto_tickets.insert(tk.END, "No hay tickets guardados en la base de datos.")
            self.texto_tickets.config(state="disabled")
            self.escribir_ticket_visual(
                self.canvas_tickets,
                self.texto_tickets.obtener_texto()
            )
            self.lbl_contador_tickets.config(text="0 de 0")
            return

        ticket = self.tickets_bd[self.ticket_actual_indice]
        metodo = "Cash" if int(ticket["is_cash"]) == 1 else "Card"

        fecha = ticket["fecha"]
        if hasattr(fecha, "strftime"):
            fecha = fecha.strftime("%Y-%m-%d %H:%M")

        self.texto_tickets.insert(tk.END, "BESITOS DE NUEZ\n")
        self.texto_tickets.insert(tk.END, "Heladeria\n")
        self.texto_tickets.insert(tk.END, "-" * 48 + "\n")
        self.texto_tickets.insert(tk.END, f"Ticket: {ticket['ticket_id']}\n")
        self.texto_tickets.insert(tk.END, f"Empleado: {ticket['empleado']}\n")
        self.texto_tickets.insert(tk.END, f"Tienda: {ticket.get('store_name', 'Desconocida')}\n")
        self.texto_tickets.insert(tk.END, f"Cliente: {ticket['cliente']}\n")
        self.texto_tickets.insert(tk.END, f"Fecha: {fecha}\n")
        self.texto_tickets.insert(tk.END, "-" * 48 + "\n")

        comentarios_generales = []
        comentarios_vistos = set()

        for producto in ticket["productos"]:
            cantidad = int(producto[0])
            nombre = str(producto[1])
            precio = float(producto[2])
            comentarios = producto[3]
            subtotal = cantidad * precio

            self.texto_tickets.insert(tk.END, f"{cantidad} x {nombre[:22]:22} $ {subtotal:7.2f}\n")

            if comentarios:
                lineas = str(comentarios).splitlines()
                for linea in lineas:
                    texto_linea = linea.strip()
                    if not texto_linea:
                        continue

                    if texto_linea.lower().startswith("comentarios:"):
                        comentario = texto_linea[len("Comentarios:"):].strip()
                        if comentario and comentario not in comentarios_vistos:
                            comentarios_generales.append(comentario)
                            comentarios_vistos.add(comentario)
                    elif ":" in texto_linea:
                        self.texto_tickets.insert(tk.END, f"   {texto_linea}\n")
                    else:
                        if texto_linea not in comentarios_vistos:
                            comentarios_generales.append(texto_linea)
                            comentarios_vistos.add(texto_linea)

        if comentarios_generales:
            self.texto_tickets.insert(tk.END, "-" * 48 + "\n")
            self.texto_tickets.insert(tk.END, "Comentarios:\n")
            for comentario in comentarios_generales:
                self.texto_tickets.insert(tk.END, f"{comentario}\n")

        self.texto_tickets.insert(tk.END, "-" * 48 + "\n")
        self.texto_tickets.insert(tk.END, f"Metodo: {metodo}\n")
        self.texto_tickets.insert(tk.END, f"TOTAL: ${ticket['total']:.2f}\n")
        if metodo == "Cash":
            if ticket.get("received") is not None:
                self.texto_tickets.insert(tk.END, f"Paid: ${ticket['received']:.2f}\n")
            if ticket.get("payment_change") is not None:
                self.texto_tickets.insert(tk.END, f"Change: ${ticket['payment_change']:.2f}\n")
        elif ticket.get("card"):
            self.texto_tickets.insert(tk.END, f"Card: **** **** **** {ticket['card']}\n")
        self.texto_tickets.insert(tk.END, "\nGracias por su compra :)\n")

        self.texto_tickets.config(state="disabled")
        self.escribir_ticket_visual(
            self.canvas_tickets,
            self.texto_tickets.obtener_texto()
        )
        self.lbl_contador_tickets.config(
            text=f"{self.ticket_actual_indice + 1} de {len(self.tickets_bd)}"
        )

    def ticket_siguiente(self):
        if not self.tickets_bd:
            return

        if self.ticket_actual_indice < len(self.tickets_bd) - 1:
            self.ticket_actual_indice += 1
            self.imprimir_ticket_bd()

    def ticket_anterior(self):
        if not self.tickets_bd:
            return

        if self.ticket_actual_indice > 0:
            self.ticket_actual_indice -= 1
            self.imprimir_ticket_bd()


if __name__ == "__main__":
    root = tk.Tk()
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    app = PuntoVentaHeladeria(root)
    root.mainloop()
