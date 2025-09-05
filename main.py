import pygame
import os
import sys
import pyttsx3
import random

# Inicializar pygame y pyttsx3
pygame.init()
engine = pyttsx3.init()

# Música de fondo
ruta_musica = os.path.join(os.path.dirname(__file__), "assets", "sonidos", "musica_fondo.mp3")
if os.path.exists(ruta_musica):
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.05)  # Volumen de 0.0 a 1.0
    pygame.mixer.music.play(-1)  # 🔁 -1 para repetir infinitamente


# Cargar sonidos
ruta_sonidos = os.path.join(os.path.dirname(__file__), "assets", "sonidos")
sonido_correcto = pygame.mixer.Sound(os.path.join(ruta_sonidos, "correcto.wav"))
sonido_error = pygame.mixer.Sound(os.path.join(ruta_sonidos, "error.wav"))

# Ajustar volumen (opcional)
sonido_correcto.set_volume(0.7)
sonido_error.set_volume(0.7)

# Canal específico para efectos
canal_efectos = pygame.mixer.Channel(1)

# Pantalla completa
info = pygame.display.Info()
ANCHO, ALTO = info.current_w, info.current_h
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Juego del Abecedario")

# Colores y lista de colores para letras
COLORES_LETRAS = [
    (255, 0, 0),     # Rojo
    (0, 153, 0),     # Verde
    (0, 102, 204),   # Azul
    (255, 102, 0),   # Naranja
    (153, 0, 153),   # Morado
    (255, 204, 0)    # Amarillo
]

# Variable global para mostrar la palabra correcta solo cuando aciertas
palabra_mostrada = ""

# Fuentes
fuente_texto = pygame.font.SysFont("Comic Sans MS", 60, bold=True)

# Ruta imágenes y fondo
ruta_img = os.path.join(os.path.dirname(__file__), "assets", "imagenes")
ruta_fondo = os.path.join(ruta_img, "Fondo.png")
fondo = pygame.image.load(ruta_fondo).convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Palomita y tachita
ruta_palomita = os.path.join(ruta_img, "palomita.png")
palomita_img = pygame.image.load(ruta_palomita).convert_alpha()

ruta_tachita = os.path.join(ruta_img, "tachita.png")
tachita_img = pygame.image.load(ruta_tachita).convert_alpha()

# Corazón
ruta_corazon = os.path.join(ruta_img, "corazon.png")
corazon_img = pygame.image.load(ruta_corazon).convert_alpha()
corazon_img = pygame.transform.scale(corazon_img, (50, 50))  # Tamaño del corazón

# Tamaño base para todos los avatares
TAM_AVATAR = (250, 250)

# Primero define la función de escalar
def escalar_imagen_con_proporcion(imagen, max_ancho, max_alto):
    ancho_original, alto_original = imagen.get_size()
    proporcion = min(max_ancho / ancho_original, max_alto / alto_original)
    nuevo_ancho = int(ancho_original * proporcion)
    nuevo_alto = int(alto_original * proporcion)
    return pygame.transform.smoothscale(imagen, (nuevo_ancho, nuevo_alto))

# Función para cargar avatar con centrado automático
def cargar_avatar(ruta):
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        img_escalada = escalar_imagen_con_proporcion(img, TAM_AVATAR[0], TAM_AVATAR[1])

        # Crear lienzo fijo del tamaño base
        lienzo = pygame.Surface(TAM_AVATAR, pygame.SRCALPHA)

        # Centrar imagen escalada dentro del lienzo
        rect = img_escalada.get_rect(center=(TAM_AVATAR[0]//2, TAM_AVATAR[1]//2))
        lienzo.blit(img_escalada, rect)

        return lienzo
    return None

# Avatar / Mascota
ruta_avatar_feliz = os.path.join(ruta_img, "avatar_feliz.png")
ruta_avatar_triste = os.path.join(ruta_img, "avatar_triste.png")
ruta_avatar_animo = os.path.join(ruta_img, "avatar_animo.png")

avatar_feliz = cargar_avatar(ruta_avatar_feliz)
avatar_triste = cargar_avatar(ruta_avatar_triste)
avatar_animo = cargar_avatar(ruta_avatar_animo)


def pantalla_inicio():
    fuente_titulo = pygame.font.SysFont("Comic Sans MS", 120, bold=True)
    fuente_subtitulo = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
    fuente_boton = pygame.font.SysFont("Comic Sans MS", 60, bold=True)

    # Colores de botones
    # color_jugar = (0, 102, 204)   # Azul fuerte
    color_jugar = (255, 255, 0)
    color_salir = (204, 0, 0)     # Rojo fuerte

    # Rectángulos botones
    boton_jugar = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 120, 300, 80)
    boton_salir = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 230, 300, 80)

    # Logo
    ruta_logo = os.path.join(ruta_img, "Logo.png")
    if os.path.exists(ruta_logo):
        logo_img = pygame.image.load(ruta_logo).convert_alpha()
        logo_img = pygame.transform.scale(logo_img, (500, 350))
    else:
        logo_img = None

    while True:
        # ⬇️ Dibuja tu fondo.png como fondo de pantalla
        pantalla.blit(fondo, (0, 0))

        # Logo ARRIBA
        if logo_img:
            pantalla.blit(logo_img, (ANCHO // 2 - logo_img.get_width() // 2, 50))

        # Subtítulo DEBAJO del logo
        subtitulo = fuente_subtitulo.render("Aprende el abecedario", True, (0, 0, 0))
        pantalla.blit(subtitulo, (
            ANCHO // 2 - subtitulo.get_width() // 2,
            10 + logo_img.get_height() + 5 if logo_img else 380
        ))

        # Botón Jugar - Azul y redondeado
        pygame.draw.rect(pantalla, color_jugar, boton_jugar, border_radius=25)
        texto_jugar = fuente_boton.render("Jugar", True, (0, 0, 0))  # Texto NEGRO
        pantalla.blit(texto_jugar, (
            boton_jugar.centerx - texto_jugar.get_width() // 2,
            boton_jugar.centery - texto_jugar.get_height() // 2
        ))

        # Botón Salir - Rojo y redondeado
        pygame.draw.rect(pantalla, color_salir, boton_salir, border_radius=25)
        texto_salir = fuente_boton.render("Salir", True, (0, 0, 0))  # Texto NEGRO
        pantalla.blit(texto_salir, (
            boton_salir.centerx - texto_salir.get_width() // 2,
            boton_salir.centery - texto_salir.get_height() // 2
        ))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    return  # Empieza juego
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

datos = [
    {
        "letra": "Aa",
        "correctas": [
            {"imagen": "A_abeja.png", "palabra": "abeja"},
            {"imagen": "A_avion.png", "palabra": "avión"},
            {"imagen": "A_arbol.png", "palabra": "árbol"}
        ],
        "otras": []
    },
    {
        "letra": "Bb",
        "correctas": [
            {"imagen": "B_ballena.png", "palabra": "ballena"},
            {"imagen": "B_bicicleta.png", "palabra": "bicicleta"},
            {"imagen": "B_botas.png", "palabra": "botas"}
        ],
        "otras": []
    },
    {
        "letra": "Cc",
        "correctas": [
            {"imagen": "C_conejo.png", "palabra": "conejo"},
            {"imagen": "C_casa.png", "palabra": "casa"},
            {"imagen": "C_carro.png", "palabra": "carro"}
        ],
        "otras": []
    },
    {
        "letra": "Dd",
        "correctas": [
            {"imagen": "D_delfin.png", "palabra": "delfín"},
            {"imagen": "D_dado.png", "palabra": "dado"},
            {"imagen": "D_dona.png", "palabra": "dona"}
        ],
        "otras": []
    },
    {
        "letra": "Ee",
        "correctas": [
            {"imagen": "E_escalera.png", "palabra": "escalera"},
            {"imagen": "E_elefante.png", "palabra": "elefante"},
            {"imagen": "E_estrella.png", "palabra": "estrella"}
        ],
        "otras": []
    },
    {
        "letra": "Ff",
        "correctas": [
            {"imagen": "F_foca.png", "palabra": "foca"},
            {"imagen": "F_foco.png", "palabra": "foco"},
            {"imagen": "F_fresa.png", "palabra": "fresa"}
        ],
        "otras": []
    },
    {
        "letra": "Gg",
        "correctas": [
            {"imagen": "G_gato.png", "palabra": "gato"},
            {"imagen": "G_globo.png", "palabra": "globo"},
            {"imagen": "G_guitarra.png", "palabra": "guitarra"}
        ],
        "otras": []
    },
    {
        "letra": "Hh",
        "correctas": [
            {"imagen": "H_hilo.png", "palabra": "hilo"},
            {"imagen": "H_huevo.png", "palabra": "huevo"},
            {"imagen": "H_hoja.png", "palabra": "hoja"}
        ],
        "otras": []
    },
    {
        "letra": "Ii",
        "correctas": [
            {"imagen": "I_iguana.png", "palabra": "iguana"},
            {"imagen": "I_isla.png", "palabra": "isla"},
            {"imagen": "I_iman.png", "palabra": "imán"}
        ],
        "otras": []
    },
    {
        "letra": "Jj",
        "correctas": [
            {"imagen": "J_jirafa.png", "palabra": "jirafa"},
            {"imagen": "J_jaula.png", "palabra": "jaula"},
            {"imagen": "J_jarron.png", "palabra": "jarrón"}
        ],
        "otras": []
    },
    {
        "letra": "Kk",
        "correctas": [
            {"imagen": "K_kiosco.png", "palabra": "kiosco"},
            {"imagen": "K_koala.png", "palabra": "koala"},
            {"imagen": "K_kiwi.png", "palabra": "kiwi"}
        ],
        "otras": []
    },
    {
        "letra": "Ll",
        "correctas": [
            {"imagen": "L_leon.png", "palabra": "león"},
            {"imagen": "L_lapiz.png", "palabra": "lápiz"},
            {"imagen": "L_lampara.png", "palabra": "lámpara"}
        ],
        "otras": []
    },
    {
        "letra": "Mm",
        "correctas": [
            {"imagen": "M_mesa.png", "palabra": "mesa"},
            {"imagen": "M_mariposa.png", "palabra": "mariposa"},
            {"imagen": "M_manzana.png", "palabra": "manzana"}
        ],
        "otras": []
    },
    {
        "letra": "Nn",
        "correctas": [
            {"imagen": "N_nube.png", "palabra": "nube"},
            {"imagen": "N_nido.png", "palabra": "nido"},
            {"imagen": "N_naranja.png", "palabra": "naranja"}
        ],
        "otras": []
    },
    {
        "letra": "Ññ",
        "correctas": [
            {"imagen": "Ñ_ñu.png", "palabra": "ñu"},
            {"imagen": "Ñ_ñame.png", "palabra": "ñame"},
            {"imagen": "Ñ_ñandu.png", "palabra": "ñandú"}
        ],
        "otras": []
    },
    {
        "letra": "Oo",
        "correctas": [
            {"imagen": "O_oveja.png", "palabra": "oveja"},
            {"imagen": "O_ojo.png", "palabra": "ojo"},
            {"imagen": "O_olla.png", "palabra": "olla"}
        ],
        "otras": []
    },
    {
        "letra": "Pp",
        "correctas": [
            {"imagen": "P_perro.png", "palabra": "perro"},
            {"imagen": "P_pera.png", "palabra": "pera"},
            {"imagen": "P_peine.png", "palabra": "peine"}
        ],
        "otras": []
    },
    {
        "letra": "Qq",
        "correctas": [
            {"imagen": "Q_querubin.png", "palabra": "querubín"},
            {"imagen": "Q_queso.png", "palabra": "queso"},
            {"imagen": "Q_quirofano.png", "palabra": "quirófano"}
        ],
        "otras": []
    },
    {
        "letra": "Rr",
        "correctas": [
            {"imagen": "R_rosa.png", "palabra": "rosa"},
            {"imagen": "R_raton.png", "palabra": "ratón"},
            {"imagen": "R_reloj.png", "palabra": "reloj"}
        ],
        "otras": []
    },
    {
        "letra": "Ss",
        "correctas": [
            {"imagen": "S_sol.png", "palabra": "sol"},
            {"imagen": "S_serpiente.png", "palabra": "serpiente"},
            {"imagen": "S_silla.png", "palabra": "silla"}
        ],
        "otras": []
    },
    {
        "letra": "Tt",
        "correctas": [
            {"imagen": "T_taco.png", "palabra": "taco"},
            {"imagen": "T_tigre.png", "palabra": "tigre"},
            {"imagen": "T_tambor.png", "palabra": "tambor"}
        ],
        "otras": []
    },
    {
        "letra": "Uu",
        "correctas": [
            {"imagen": "U_uña.png", "palabra": "uña"},
            {"imagen": "U_universo.png", "palabra": "universo"},
            {"imagen": "U_uva.png", "palabra": "uva"}
        ],
        "otras": []
    },
    {
        "letra": "Vv",
        "correctas": [
            {"imagen": "V_vaca.png", "palabra": "vaca"},
            {"imagen": "V_vela.png", "palabra": "vela"},
            {"imagen": "V_ventana.png", "palabra": "ventana"}
        ],
        "otras": []
    },
    {
        "letra": "Ww",
        "correctas": [
            {"imagen": "W_wifi.png", "palabra": "wifi"},
            {"imagen": "W_waffle.png", "palabra": "waffle"}
        ],
        "otras": []
    },
    {
        "letra": "Xx",
        "correctas": [
            {"imagen": "X_xilofono.png", "palabra": "xilófono"}
        ],
        "otras": []
    },
    {
        "letra": "Yy",
        "correctas": [
            {"imagen": "Y_yoyo.png", "palabra": "yoyo"},
            {"imagen": "Y_yegua.png", "palabra": "yegua"},
            {"imagen": "Y_yema.png", "palabra": "yema"}
        ],
        "otras": []
    },
    {
        "letra": "Zz",
        "correctas": [
            {"imagen": "Z_zapato.png", "palabra": "zapato"},
            {"imagen": "Z_zorro.png", "palabra": "zorro"},
            {"imagen": "Z_zanahoria.png", "palabra": "zanahoria"}
        ],
        "otras": []
    }
 
]

# Distractores automáticos: NO empiezan con prefijo y excluyen imágenes de sistema
prefijos = tuple(f"{chr(i)}_" for i in range(ord("A"), ord("Z")+1))
EXCLUIR_IMAGENES = ["Fondo.png", "palomita.png", "tachita.png", "Logo.png", "corazon.png", "avatar_feliz.png", "avatar_triste.png", "avatar_animo.png"]

todas_imagenes = os.listdir(ruta_img)
IMAGENES_DISTRACCION = [
    img for img in todas_imagenes
    if not img.startswith(prefijos)
    and img.endswith(".png")
    and img not in EXCLUIR_IMAGENES
]
def wrap_text(texto, fuente, max_ancho):
    """Devuelve una lista de líneas ajustadas al ancho dado."""
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = (linea_actual + " " + palabra).strip()
        if fuente.size(prueba)[0] <= max_ancho:
            linea_actual = prueba
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return lineas

def dibujar_panel_con_texto(pantalla, rect, lineas, fuente, color_texto=(0,0,0),
                            color_fondo=(255,255,255,235), color_borde=(0,0,0),
                            grosor_borde=4, radio=25, padding=24, interlineado=10):
    """
    Dibuja un panel semitransparente y el texto dentro con padding y borde.
    - rect: pygame.Rect con posición y tamaño del panel
    - lineas: lista de cadenas ya envueltas (sin saltos '\n')
    """
    # Panel con alpha
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, color_fondo, panel.get_rect(), border_radius=radio)
    pygame.draw.rect(panel, color_borde, panel.get_rect(), grosor_borde, border_radius=radio)

    # Renderizar texto dentro del panel
    x_texto = padding
    y_texto = padding
    max_ancho_texto = rect.width - 2*padding

    for linea in lineas:
        # Si alguna línea ya viene muy larga, se vuelve a ajustar
        for sublinea in wrap_text(linea, fuente, max_ancho_texto):
            superficie = fuente.render(sublinea, True, color_texto)
            panel.blit(superficie, (x_texto, y_texto))
            y_texto += superficie.get_height() + interlineado

    # Blit del panel a pantalla
    pantalla.blit(panel, (rect.x, rect.y))


def pantalla_instrucciones():
    # Fuentes
    fuente_titulo = pygame.font.SysFont("Comic Sans MS", 100, bold=True)
    fuente_texto  = pygame.font.SysFont("Comic Sans MS", 40)   # 🔹 más pequeña
    fuente_boton  = pygame.font.SysFont("Comic Sans MS", 60, bold=True)

    # Dimensiones del panel
    panel_ancho = int(ANCHO * 0.78)
    panel_alto  = int(ALTO * 0.55)
    panel_rect  = pygame.Rect(
        (ANCHO - panel_ancho)//2,
        (ALTO - panel_alto)//2 + 40,
        panel_ancho,
        panel_alto
    )

    # Botón azul debajo del panel
    boton_ancho = 420
    boton_alto  = 100
    boton_rect = pygame.Rect(
        ANCHO // 2 - boton_ancho // 2,
        panel_rect.bottom + 20,   # 🔹 justo debajo del panel
        boton_ancho,
        boton_alto
    )

    # Texto de instrucciones (los 5 pasos completos)
    instrucciones = [
        "1. Mira la letra que aparece arriba.",
        "2. Haz clic en la imagen que EMPIECE con esa letra.",
        "3. Si aciertas, escucharás la palabra y sigues avanzando.",
        "4. Si fallas, perderás un corazón.",
        "¡Diviértete aprendiendo!"
    ]

    padding_panel = 24
    max_ancho_texto = panel_rect.width - 2*padding_panel
    lineas_envueltas = []
    for linea in instrucciones:
        lineas_envueltas.extend(wrap_text(linea, fuente_texto, max_ancho_texto))

    while True:
        pantalla.blit(fondo, (0, 0))

        # Título arriba
        titulo = fuente_titulo.render("Instrucciones", True, (0, 0, 0))
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width() // 2,
                               panel_rect.top - titulo.get_height() - 20))

        # Panel con texto
        dibujar_panel_con_texto(
            pantalla, panel_rect, lineas_envueltas, fuente_texto,
            color_texto=(0, 0, 0),
            color_fondo=(255, 255, 255, 240),
            color_borde=(0, 0, 0),
            grosor_borde=4,
            radio=30,
            padding=padding_panel,
            interlineado=8
        )

        # Botón azul (con hover)
        mouse_pos = pygame.mouse.get_pos()
        azul = (0, 102, 204)
        azul_hover = (30, 140, 255)
        color_boton = azul_hover if boton_rect.collidepoint(mouse_pos) else azul

        pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=25)
        texto_boton = fuente_boton.render("¡Iniciar!", True, (0, 0, 0))
        pantalla.blit(texto_boton, (
            boton_rect.centerx - texto_boton.get_width() // 2,
            boton_rect.centery - texto_boton.get_height() // 2
        ))

        pygame.display.flip()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    return
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return

# Voz
def hablar(texto):
    try:
        nombre_audio = None

        # Buscar audios por patrones comunes
        if texto.startswith("¿Cuál imagen empieza con la letra "):
            letra = texto.split("letra ")[1].replace("?", "")
            nombre_audio = f"pregunta_{letra}.mp3"

        elif texto.startswith("¡Correcto!"):
            partes = texto.replace("¡Correcto! ", "").split(" de ")
            if len(partes) == 2:
                letra = partes[0].strip()
                palabra = partes[1].strip()
                nombre_audio = f"correcto_{letra}_{palabra}.mp3"

        elif texto.lower() == "intenta otra vez":
            nombre_audio = "intenta_otra_vez.mp3"

        elif "se acabaron tus vidas" in texto.lower():
            nombre_audio = "vidas_terminadas.mp3"

        elif "felicidades" in texto.lower():
            nombre_audio = "felicidades.mp3"

        elif texto.strip().isalnum():  # solo palabra suelta
            nombre_audio = texto.strip() + ".mp3"

        if nombre_audio:
            ruta = os.path.join("assets", "audios", nombre_audio)
            if os.path.exists(ruta):
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(100)
                return  # termina si usó el audio

        # Si no se encuentra audio, usar pyttsx3 como respaldo
        engine.say(texto)
        engine.runAndWait()

    except Exception as e:
        print(f"Error al reproducir voz: {e}")
        engine.say(texto)
        engine.runAndWait()

# Imagen con marco circular grande y fondo blanco
def cargar_imagen(nombre, tamaño=(300, 300)):
    ruta = os.path.join(ruta_img, nombre)
    try:
        imagen = pygame.image.load(ruta).convert_alpha()

        # Escalar proporcionalmente
        imagen = escalar_imagen_con_proporcion(imagen, tamaño[0] - 50, tamaño[1] - 50)

        # Crear superficie circular
        imagen_redonda = pygame.Surface(tamaño, pygame.SRCALPHA)
        centro = (tamaño[0] // 2, tamaño[1] // 2)
        radio = tamaño[0] // 2
        pygame.draw.circle(imagen_redonda, (255, 255, 255, 255), centro, radio)

        # Centrar imagen escalada dentro del círculo
        rect_imagen = imagen.get_rect(center=centro)
        imagen_redonda.blit(imagen, rect_imagen)

        # Aplicar máscara circular
        mascara = pygame.Surface(tamaño, pygame.SRCALPHA)
        pygame.draw.circle(mascara, (255, 255, 255, 255), centro, radio)
        imagen_redonda.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return imagen_redonda

    except Exception as e:
        print(f"Error cargando imagen {ruta}: {e}")
        return None

def dibujar_burbuja(texto, x, y, ancho_max=300):
    fuente = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    texto_render = fuente.render(texto, True, (0, 0, 0))
    
    padding = 20
    ancho = texto_render.get_width() + padding * 2
    alto = texto_render.get_height() + padding * 2

    burbuja_rect = pygame.Rect(x, y, ancho, alto)
    
    # Dibuja fondo blanco con borde negro
    pygame.draw.rect(pantalla, (255, 255, 255), burbuja_rect, border_radius=15)
    pygame.draw.rect(pantalla, (0, 0, 0), burbuja_rect, 3, border_radius=15)
    
    # Dibuja triangulito (punta de burbuja)
    punta = [
        (x + 30, y + alto),  # vértice inferior
        (x + 50, y + alto + 20),
        (x + 70, y + alto)
    ]
    pygame.draw.polygon(pantalla, (255, 255, 255), punta)
    pygame.draw.polygon(pantalla, (0, 0, 0), punta, 3)

    # Dibuja texto encima
    pantalla.blit(texto_render, (x + padding, y + padding))

def minijuego_arrastrar_letra_opciones(letras_aprendidas, imagen_correcta, palabra):
    letra_objetivo = imagen_correcta.split("_")[0]  # Por ejemplo: A_abeja.png → "A"

    # Si hay menos de 3 letras aprendidas, usa todas
    if len(letras_aprendidas) < 3:
        letras_disponibles = letras_aprendidas.copy()
    else:
        letras_disponibles = random.sample(letras_aprendidas, k=3)

    # Asegurar que la letra correcta esté en las opciones
    if letra_objetivo not in letras_disponibles:
        letras_disponibles[random.randint(0, len(letras_disponibles)-1)] = letra_objetivo
    if letra_objetivo not in letras_disponibles:
        letras_disponibles[random.randint(0, 2)] = letra_objetivo  # asegurar que esté

    letras_disponibles.sort()  # opcional: ordenadas

    # Cargar imagen
    imagen = cargar_imagen(imagen_correcta, tamaño=(200, 200))
    if not imagen:
        return

    rect_imagen = imagen.get_rect(topleft=(100, ALTO // 2))
    arrastrando = False

# Posiciones letras
# Posiciones posibles centradas a la derecha
    posiciones_letras = [
        (ANCHO // 2 + 100, ALTO // 2 - 150),
        (ANCHO // 2 + 300, ALTO // 2),
        (ANCHO // 2 + 500, ALTO // 2 + 150)
    ]
    random.shuffle(posiciones_letras)

    # Barajar las letras también
    random.shuffle(letras_disponibles)

    # Renderizar letras y asociarlas a su posición
    rects_letras = []
    fuente = pygame.font.SysFont("Comic Sans MS", 180, bold=True)

    for letra, (x, y) in zip(letras_disponibles, posiciones_letras):
        texto = fuente.render(letra, True, (0, 0, 0))
        rect = texto.get_rect(center=(x, y))
        rects_letras.append((letra, texto, rect))

    # Mostrar fondo y letras ANTES de hablar
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(imagen, rect_imagen)

    for _, texto, rect in rects_letras:
        pygame.draw.rect(pantalla, (255, 255, 255), rect.inflate(30, 30))  # fondo blanco
        pygame.draw.rect(pantalla, (0, 0, 0), rect.inflate(30, 30), 4)
        pantalla.blit(texto, rect)

    pygame.display.flip()

    # Espera medio segundo antes de hablar
    pygame.time.delay(500)

    nombre_audio = f"minijuego_{imagen_correcta.split('_')[0]}_{palabra}.mp3"
    ruta_audio = os.path.join("assets", "audios", nombre_audio)
    if os.path.exists(ruta_audio):
        pygame.mixer.music.load(ruta_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
    else:
        hablar(f"¿A qué letra corresponde {palabra}? Arrástrala")

    terminado = False
    while not terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_imagen.collidepoint(evento.pos):
                    arrastrando = True
            elif evento.type == pygame.MOUSEBUTTONUP:
                arrastrando = False
                for letra, texto, rect in rects_letras:
                    if rect_imagen.colliderect(rect):
                        if letra == letra_objetivo:
                            ruta_muy_bien = os.path.join("assets", "audios", "muy_bien.mp3")
                            if os.path.exists(ruta_muy_bien):
                                pygame.mixer.music.load(ruta_muy_bien)
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy():
                                    pygame.time.delay(100)
                            else:
                                hablar("¡Muy bien!")
                            terminado = True
                        else:
                            hablar("Intenta otra vez")
            elif evento.type == pygame.MOUSEMOTION and arrastrando:
                rect_imagen.center = evento.pos

        pantalla.blit(fondo, (0, 0))
        
        for _, texto, rect in rects_letras:
            pygame.draw.rect(pantalla, (255, 255, 255), rect.inflate(30, 30))  # fondo blanco
            pygame.draw.rect(pantalla, (0, 0, 0), rect.inflate(30, 30), 4)
            pantalla.blit(texto, rect)

        pantalla.blit(imagen, rect_imagen)
        pygame.display.flip()

# Mostrar pantalla con palomita o tachita
def mostrar_pantalla(
    letra, opciones, imagen_correcta, color_letra, posiciones,
    mostrar_palomita=False, rect_palomita=None,
    mostrar_tachita=False, rect_tachita=None,
    estado_avatar="normal"  # nuevo parámetro
):
    global vidas

    pantalla.blit(fondo, (0, 0))

    fuente_letra = pygame.font.SysFont("Comic Sans MS", 200, bold=True)
    fuente_palabra = pygame.font.SysFont("Comic Sans MS", 90, bold=True)

    sombra = fuente_letra.render(letra, True, (0, 0, 0))
    pantalla.blit(sombra, (55, 55))

    texto = fuente_letra.render(letra, True, color_letra)
    pantalla.blit(texto, (50, 50))

    if palabra_mostrada != "":
        color_palabra = random.choice(COLORES_LETRAS)
        texto_palabra = fuente_palabra.render(palabra_mostrada, True, color_palabra)
        sombra_palabra = fuente_palabra.render(palabra_mostrada, True, (0, 0, 0))

        x_palabra = (ANCHO // 2) - (texto_palabra.get_width() // 2)
        y_palabra = 250

        pantalla.blit(sombra_palabra, (x_palabra + 3, y_palabra + 3))
        pantalla.blit(texto_palabra, (x_palabra, y_palabra))

    botones = []
    rect_correcto = None

    for img_nombre, pos in zip(opciones, posiciones):
        imagen = cargar_imagen(img_nombre)
        if imagen:
            rect = imagen.get_rect(topleft=pos)
            pantalla.blit(imagen, pos)
            es_correcta = (img_nombre == imagen_correcta)
            botones.append((rect, es_correcta))
            if es_correcta:
                rect_correcto = rect

    if mostrar_palomita and rect_palomita:
        palomita_escalada = pygame.transform.smoothscale(palomita_img, (250, 250))
        palomita_rect = palomita_escalada.get_rect(center=rect_palomita.center)
        pantalla.blit(palomita_escalada, palomita_rect)

    if mostrar_tachita and rect_tachita:
        tachita_escalada = pygame.transform.smoothscale(tachita_img, (250, 250))
        tachita_rect = tachita_escalada.get_rect(center=rect_tachita.center)
        pantalla.blit(tachita_escalada, tachita_rect)

    # Mostrar avatar centrado arriba del texto de la palabra (si hay)
    avatar_a_usar = None
    if estado_avatar == "feliz":
        avatar_a_usar = avatar_feliz
    elif estado_avatar == "triste":
        avatar_a_usar = avatar_triste
    elif estado_avatar == "animo":
        avatar_a_usar = avatar_animo

    if avatar_a_usar:
        x_avatar = ANCHO // 2 - avatar_a_usar.get_width() // 2
        y_avatar = 20
        pantalla.blit(avatar_a_usar, (x_avatar, y_avatar))

    # Si es un avatar de ánimo, muestra burbuja Y reproduce el audio correspondiente
    if estado_avatar == "animo":
        frases_y_audios = [
            ("¡Vamos, tú puedes!", "animo_tu_puedes.mp3"),
            ("No te rindas", "animo_no_te_rindas.mp3"),
            ("Inténtalo otra vez", "animo_intentalo_otra_vez.mp3")
        ]
        frase, audio_file = random.choice(frases_y_audios)

        # Reproducir audio si existe
        ruta_audio = os.path.join("assets", "audios", audio_file)
        if os.path.exists(ruta_audio):
            pygame.mixer.music.load(ruta_audio)
            pygame.mixer.music.play()

        # Dibuja la burbuja de texto
        burbuja_x = x_avatar + avatar_a_usar.get_width() + 10
        burbuja_y = y_avatar + 80
        dibujar_burbuja(frase, burbuja_x, burbuja_y)

    # Corazones
    radio_marco = 30
    tamaño_corazon = 40
    corazon_escalado = pygame.transform.smoothscale(corazon_img, (tamaño_corazon, tamaño_corazon))

    for i in range(vidas):
        x = ANCHO - (i + 1) * (2 * radio_marco + 10)
        y = 20
        centro_x = x + radio_marco
        centro_y = y + radio_marco

        pygame.draw.circle(pantalla, (255, 255, 255), (centro_x, centro_y), radio_marco)
        corazon_rect = corazon_escalado.get_rect(center=(centro_x, centro_y))
        pantalla.blit(corazon_escalado, corazon_rect)

    pygame.display.flip()
    return botones, rect_correcto

def juego_letra(info):
    global palabra_mostrada
    palabra_mostrada = ""

    correcta = random.choice(info["correctas"])
    imagen_correcta = correcta["imagen"]
    palabra_correcta = correcta["palabra"]

    num_distractores = 2
    distraccion = info["otras"].copy()

    # Evitar distractores que empiecen con la misma letra
    letra_actual = info["letra"].lower()
    disponibles = [
        img for img in IMAGENES_DISTRACCION
        if img not in distraccion
        and img != imagen_correcta
        and not img.lower().startswith(letra_actual)
    ]
    random.shuffle(disponibles)
    distraccion += disponibles[:num_distractores - len(distraccion)]

    opciones = distraccion + [imagen_correcta]
    random.shuffle(opciones)

    color_letra = random.choice(COLORES_LETRAS)

    desplazamiento_vertical = 180
    posiciones = [
        (ANCHO // 4 - 150, ALTO // 2 - 150 + desplazamiento_vertical),
        (ANCHO // 2 - 150, ALTO // 2 - 150 + desplazamiento_vertical),
        (3 * ANCHO // 4 - 150, ALTO // 2 - 150 + desplazamiento_vertical)
    ]
    random.shuffle(posiciones)

    botones, rect_correcto = mostrar_pantalla(info["letra"], opciones, imagen_correcta, color_letra, posiciones)
    hablar(f"¿Cuál imagen empieza con la letra {info['letra']}?")
    return botones, palabra_correcta, imagen_correcta, color_letra, opciones, posiciones

# Bucle principal
while True:
    pantalla_inicio()
    pantalla_instrucciones()   # ← ahora aparece la ventanita legible
    vidas = 5
    indice = 0
    botones, palabra_actual, imagen_correcta, color_letra, opciones_actuales, posiciones_actuales = juego_letra(datos[indice])
    ...

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for rect, es_correcta in botones:
                    if rect.collidepoint(evento.pos):
                        if es_correcta:
                            canal_efectos.play(sonido_correcto)
                            hablar(f"¡Correcto! {datos[indice]['letra']} de {palabra_actual}")
                            palabra_mostrada = palabra_actual

                            botones, rect_correcto = mostrar_pantalla(
                                datos[indice]['letra'],
                                opciones_actuales,
                                imagen_correcta,
                                color_letra,
                                posiciones_actuales,
                                mostrar_palomita=True,
                                rect_palomita=rect,
                                estado_avatar="feliz"
                            )
                            pygame.time.delay(3000)

                            indice += 1
                            # Guardar letras ya aprendidas
                            letras_aprendidas = [d["letra"] for d in datos[:indice]]

                            # Activar minijuego de repaso cada 5 letras
                            if indice % 5 == 0 and indice < len(datos):
                                letras_aprendidas = [d["letra"] for d in datos[:indice]]
                                letras_5 = letras_aprendidas[-5:]

                                # Elegir aleatoriamente una letra entre las últimas 5
                                letra_aleatoria = random.choice(letras_5)
                                info = next(d for d in datos if d["letra"] == letra_aleatoria)
                                objeto = random.choice(info["correctas"])

                                imagen_aleatoria = objeto["imagen"]
                                palabra_aleatoria = objeto["palabra"]


                                minijuego_arrastrar_letra_opciones(
                                    letras_aprendidas,
                                    imagen_aleatoria,
                                    palabra_aleatoria
                                )

                            if indice < len(datos):
                                botones, palabra_actual, imagen_correcta, color_letra, opciones_actuales, posiciones_actuales = juego_letra(datos[indice])
                            else:
                                hablar("¡Felicidades! Has terminado el abecedario.")
                                mostrar_pantalla(
                                    letra="",
                                    opciones=[],
                                    imagen_correcta="",
                                    color_letra=(0,0,0),
                                    posiciones=[],
                                    estado_avatar="feliz"
                                )
                                pygame.time.delay(2500)
                                corriendo = False

                        else:
                            canal_efectos.play(sonido_error)
                            hablar("Intenta otra vez")
                            vidas -= 1
                            if vidas <= 0:
                                hablar("¡Se acabaron tus vidas!")
                                mostrar_pantalla(
                                    letra=datos[indice]['letra'],
                                    opciones=opciones_actuales,
                                    imagen_correcta=imagen_correcta,
                                    color_letra=color_letra,
                                    posiciones=posiciones_actuales,
                                    estado_avatar="triste"
                                )
                                pygame.time.delay(2500)
                                corriendo = False
                                break

                            botones, _ = mostrar_pantalla(
                                datos[indice]['letra'],
                                opciones_actuales,
                                imagen_correcta,
                                color_letra,
                                posiciones_actuales,
                                mostrar_tachita=True,
                                rect_tachita=rect,
                                estado_avatar="triste"
                            )
                            pygame.time.delay(2000)

                            botones, _ = mostrar_pantalla(
                                datos[indice]['letra'],
                                opciones_actuales,
                                imagen_correcta,
                                color_letra,
                                posiciones_actuales,
                                estado_avatar="animo"
                            )
                            pygame.time.delay(1500)

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

