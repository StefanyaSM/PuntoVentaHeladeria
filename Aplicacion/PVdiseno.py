import os
import math
import tkinter as tk
import unicodedata
import winsound

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

COLOR_FONDO = "#f3e8dc"
COLOR_TEXTO = "#341c0f"
COLOR_TITULO = "#ea6f9a"
COLOR_BOTON = "#fcd8c0"
COLOR_BORDE = "#A68C6D"

FUENTE_TITULO = ("Comic Sans MS", 32, "bold")
FUENTE_SUBTITULO = ("Comic Sans MS", 18, "bold")
FUENTE_NORMAL = ("Comic Sans MS", 13)
FUENTE_BOTON = ("Comic Sans MS", 12)

RUTA_SONIDO_BOTON = os.path.join(
    os.path.dirname(__file__),
    "Sounds",
    "SonidoBoton.wav"
)

RUTA_SONIDO_TICKET = os.path.join(
    os.path.dirname(__file__),
    "Sounds",
    "STicket.wav"
)

RUTA_IMAGENES = os.path.join(
    os.path.dirname(__file__),
    "Images"
)

EXTENSIONES_IMAGEN = (".png", ".gif", ".ppm", ".pgm")

ALIAS_IMAGEN_PRODUCTO = {
    "makeyourown": "Make your own.png",
    "makeyourownsundae": "Make your own.png"
}


def normalizar_nombre_imagen(nombre):
    # Comentario: Esta funcion limpia un nombre de producto o archivo para compararlo sin espacios, acentos ni mayusculas.
    texto = unicodedata.normalize("NFKD", str(nombre).strip().casefold())
    texto = "".join(letra for letra in texto if not unicodedata.combining(letra))
    return "".join(letra for letra in texto if letra.isalnum())


def obtener_ruta_imagen_producto(nombre_producto):
    #busca la imagen de un producto usando alias y nombres normalizados dentro de la carpeta Images.
    if not os.path.isdir(RUTA_IMAGENES):
        return None

    nombre_normalizado = normalizar_nombre_imagen(nombre_producto)
    alias = ALIAS_IMAGEN_PRODUCTO.get(nombre_normalizado)

    if alias:
        ruta_alias = os.path.join(RUTA_IMAGENES, alias)
        if os.path.exists(ruta_alias):
            return ruta_alias

    # Recorre carpeta, _, archivos para procesar cada dato de la coleccion.
    for carpeta, _, archivos in os.walk(RUTA_IMAGENES):
        for archivo in archivos:
            nombre_archivo, extension = os.path.splitext(archivo)

            if extension.lower() not in EXTENSIONES_IMAGEN:
                # Salta esta iteracion y pasa al siguiente elemento del ciclo.
                continue

            if normalizar_nombre_imagen(nombre_archivo) == nombre_normalizado:
                return os.path.join(carpeta, archivo)
    return None


def obtener_ruta_imagen_alias(nombre_archivo):
    #Localiza una imagen por su nombre exacto dentro de la carpeta Images.
    for carpeta, _, archivos in os.walk(RUTA_IMAGENES):
        for archivo in archivos:
            _, extension = os.path.splitext(archivo)

            if extension.lower() not in EXTENSIONES_IMAGEN:
                continue

            if archivo == nombre_archivo:
                return os.path.join(carpeta, archivo)
    return None


def cargar_imagen_desde_ruta(ruta_imagen, max_ancho, max_alto):
    #Carga una imagen desde disco y la ajusta al tamano maximo indicado para usarla en Tkinter.
    if not ruta_imagen:
        return None

    try:
        if Image and ImageTk:
            filtro = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
            with Image.open(ruta_imagen) as archivo_imagen:
                imagen_pil = archivo_imagen.convert("RGBA")

            imagen_pil.thumbnail((max_ancho, max_alto), filtro)

            lienzo = Image.new("RGBA", (max_ancho, max_alto), (0, 0, 0, 0))
            x = (max_ancho - imagen_pil.width) // 2
            y = (max_alto - imagen_pil.height) // 2
            lienzo.paste(imagen_pil, (x, y), imagen_pil)
            return ImageTk.PhotoImage(lienzo)

        imagen = tk.PhotoImage(file=ruta_imagen)
        factor = max(
            math.ceil(imagen.width() / max_ancho),
            math.ceil(imagen.height() / max_alto),
            1
        )

        if factor > 1: #Si la imagen es mas grande que el maximo permitido, se reduce usando subsample.
            imagen = imagen.subsample(factor, factor)

        return imagen
    except (OSError, tk.TclError):
        return None


def cargar_imagen_producto(nombre_producto, max_ancho=170, max_alto=125):
    # obtiene la ruta de un producto y devuelve su imagen lista para la interfaz.
    return cargar_imagen_desde_ruta(
        obtener_ruta_imagen_producto(nombre_producto),
        max_ancho,
        max_alto
    )


def cargar_imagen_alias(nombre_archivo, max_ancho=170, max_alto=125):
    #obtiene una imagen conocida por nombre de archivo y la prepara para la interfaz.
    return cargar_imagen_desde_ruta(
        obtener_ruta_imagen_alias(nombre_archivo),
        max_ancho,
        max_alto
    )


def reproducir_sonido_boton():
    try:
        if os.path.exists(RUTA_SONIDO_BOTON):
            winsound.PlaySound(
                RUTA_SONIDO_BOTON,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
    except RuntimeError:
        pass


def reproducir_sonido_ticket():
    try:
        if os.path.exists(RUTA_SONIDO_TICKET):
            winsound.PlaySound(
                RUTA_SONIDO_TICKET,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
    except RuntimeError:
        pass


def comando_con_sonido(comando):
    def ejecutar():
        reproducir_sonido_boton()
        return comando()
    return ejecutar


class DisenoHeladeria:
    def boton(self, padre, texto, comando, ancho=14, alto=1):
        #crea un boton con el estilo visual del sistema y cn sonido
        return tk.Button(
            padre,
            text=texto,
            command=comando_con_sonido(comando),
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            bg=COLOR_BOTON,
            activebackground=COLOR_BOTON,
            width=ancho,
            height=alto,
            relief="flat",
            bd=0,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE,
            highlightthickness=1
        )

    def titulo(self, padre):
        #Dibuja el titulo principal de la heladeria
        tk.Label(
            padre,
            text="Besitos de\nNuez",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(pady=(20, 0))

        tk.Label(
            padre,
            text="Heladeria",
            font=FUENTE_SUBTITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(pady=(0, 25))

    def marco_centrado(self):
        #Crea un frame centrado que sirve como base para pantallas simples
        frame = tk.Frame(self.root, bg=COLOR_FONDO)
        frame.pack(expand=True)
        return frame

    def borde_suave(self):
        return {
            "relief": "flat",
            "bd": 0,
            "highlightbackground": COLOR_BORDE,
            "highlightcolor": COLOR_BORDE,
            "highlightthickness": 1
        }

    def centrar_ventana(self, ventana, ancho, alto):
        #calcula la posicion para centrar una ventana emergente 
        self.root.update_idletasks()
        ventana.update_idletasks()

        root_ancho = self.root.winfo_width()
        root_alto = self.root.winfo_height()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        if root_ancho <= 1 or root_alto <= 1:
            root_ancho = self.root.winfo_screenwidth()
            root_alto = self.root.winfo_screenheight()
            root_x = 0
            root_y = 0

        x = root_x + (root_ancho - ancho) // 2
        y = root_y + (root_alto - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def configurar_icono_ventana(self, ventana, predeterminado=False):
        #pone el icono de la aplicacion en una ventana de Tkinter (la nuez mini)
        if not hasattr(self, "icono_app"):
            self.icono_app = cargar_imagen_alias("AppLogo.png", 32, 32)

        if self.icono_app:
            try:
                ventana.iconphoto(predeterminado, self.icono_app)
            except tk.TclError:
                pass

    def crear_modal(self, titulo, ancho=430, alto=310, cerrar=None): #crear ventanas emergentes y su estilo
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_FONDO)
        self.configurar_icono_ventana(ventana)
        ventana.transient(self.root)
        self.centrar_ventana(ventana, ancho, alto)
        ventana.grab_set()

        if cerrar: #cierra ventana emergente, devuelve atencion a la principal
            ventana.protocol("WM_DELETE_WINDOW", cerrar)

        self.logo_modal = cargar_imagen_alias("Logo.png", 170, 135)
        if self.logo_modal:
            tk.Label(
                ventana,
                image=self.logo_modal,
                bg=COLOR_FONDO
            ).pack(pady=(8, 0))
        else:
            tk.Label(
                ventana,
                text="Besitos de Nuez",
                font=FUENTE_SUBTITULO,
                fg=COLOR_TEXTO,
                bg=COLOR_FONDO
            ).pack(pady=(18, 4))
        return ventana

    def crear_ticket_visual(self, padre, atributo_imagen): #lo visual del ticket y asi
        ancho_ticket = 500
        alto_ticket = 780
        imagen_ticket = cargar_imagen_alias("Ticket.png", ancho_ticket, alto_ticket)

        canvas = tk.Canvas(
            padre,
            width=ancho_ticket,
            height=alto_ticket,
            bg=COLOR_FONDO,
            highlightthickness=0,
            bd=0
        )

        if imagen_ticket:
            setattr(self, atributo_imagen, imagen_ticket)
            canvas.create_image(
                ancho_ticket // 2,
                alto_ticket // 2,
                image=imagen_ticket
            )
        canvas.pack(pady=5)
        return canvas

    def escribir_ticket_visual(self, canvas, texto):
        if hasattr(canvas, "texto_ticket_id"): #escribe en el ticket
            canvas.delete(canvas.texto_ticket_id)

        canvas.texto_ticket_id = canvas.create_text(
            75,
            80,
            anchor="nw",
            text=texto,
            font=("Courier New", 11),
            fill=COLOR_TEXTO,
            width=355
        )

    def crear_buffer_texto_ticket(self):
        #Crea un buffer compatible con metodos de texto para armar tickets antes de dibujarlos.
        class TicketBuffer:
            def __init__(self):
                self.partes = []

            def insert(self, _, texto_insertado):#agrega texto al buffer interno del ticket.
                self.partes.append(texto_insertado)

            def delete(self, *_): #Limpia el buffer
                self.partes = []

            def config(self, **_):
                #Manteien compatibilidad con widgets de texto aunque no necesite cambiar estado real.
                pass

            def obtener_texto(self):
                #Une todas las partes del buffer y devuelve el texto completo.
                return "".join(self.partes)

        # Devuelve el valor calculado para que otra parte del programa lo use.
        return TicketBuffer()
