import pygame
import random
import sys
import os

# ========= RUTAS PORTABLES =========
# BASE apunta a la carpeta temporal del .exe (cuando está empacado);
# si corres como .py, apunta al folder real del archivo.
BASE = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

def asset(nombre_relativo: str) -> str:
    """Devuelve la ruta al recurso dentro de la carpeta 'assets' del bundle."""
    return os.path.join(BASE, "assets", nombre_relativo)

# Carpeta segura para GUARDAR archivos del usuario (no dentro del bundle).
SAVE_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "InvasoresMatematicos")
os.makedirs(SAVE_DIR, exist_ok=True)
PUNTAJES_PATH = os.path.join(SAVE_DIR, "puntajes.txt")

# ========= INIT =========
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    print("Aviso: No se pudo inicializar el audio. El juego correrá sin sonidos.")

# ========= CONST =========
ANCHO, ALTO = 800, 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO  = (0, 0, 0)
ROJO   = (255, 50, 50)
VERDE  = (0, 255, 0)
AZUL   = (0, 0, 255)
GRIS   = (200, 200, 200)
AMARILLO = (255, 255, 0)

# ========= WINDOW =========
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Invasores Matemáticos")

# ========= LOAD ASSETS =========
def cargar_imagen(nombre, size=None):
    try:
        img = pygame.image.load(asset(nombre)).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        # Fallback visual si falta imagen
        w, h = size if size else (200, 200)
        surf = pygame.Surface((w, h))
        surf.fill((30, 30, 30))
        pygame.draw.rect(surf, (80, 80, 80), surf.get_rect(), 4)
        # Debug opcional:
        # print("No se pudo cargar:", nombre, "->", e)
        return surf

def cargar_sonido(nombre):
    try:
        return pygame.mixer.Sound(asset(nombre))
    except Exception:
        return None

# Fondos
fondo_menu  = cargar_imagen("fondo_menu.jpg", (ANCHO, ALTO))
fondo_juego = cargar_imagen("fondo_juego.jpg", (ANCHO, ALTO))

# Sprites por operación
sprite_plus  = cargar_imagen("alien_plus.png",  (100, 100))
sprite_minus = cargar_imagen("alien_minus.png", (100, 100))
sprite_mul   = cargar_imagen("alien_mul.png",   (100, 100))

SPRITE_POR_OP = {
    "+": sprite_plus,
    "-": sprite_minus,
    "*": sprite_mul,
}

# Sonidos
sonido_correcto   = cargar_sonido("correcto.wav")
sonido_incorrecto = cargar_sonido("incorrecto.wav")
sonido_tiempo     = cargar_sonido("tiempo.wav")
sonido_gameover   = cargar_sonido("gameover.wav")
sonido_tecla      = cargar_sonido("tecla.wav")

# ========= FONTS =========
fuente        = pygame.font.SysFont("consolas", 32)
fuente_grande = pygame.font.SysFont("consolas", 60)

# ========= STATE =========
nombre_jugador  = ""
en_menu         = True
puntaje         = 0
vidas           = 3
nivel           = 1
velocidad       = 1.5
entrada_usuario = ""
enemigo_actual  = None

# ========= UTILS =========
def play(snd):
    if snd:
        snd.play()

def reset_juego():
    global puntaje, vidas, nivel, velocidad, entrada_usuario
    puntaje = 0
    vidas = 3
    nivel = 1
    velocidad = 1.5
    entrada_usuario = ""

def guardar_puntaje():
    try:
        with open(PUNTAJES_PATH, "a", encoding="utf-8") as f:
            f.write(f"{nombre_jugador}: Puntaje: {puntaje}, Nivel: {nivel}\n")
    except Exception:
        pass

# ========= ENEMY =========
class Enemigo:
    def __init__(self, pregunta, respuesta, op, velocidad_caida):
        self.pregunta  = pregunta
        self.respuesta = respuesta
        self.op = op
        self.x = ANCHO // 2 - 50
        self.y = 50
        self.velocidad = velocidad_caida
        self.sprite = SPRITE_POR_OP.get(op)

    def mover(self):
        self.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.sprite, (self.x, self.y))
        color = BLANCO  # podrías variar por operación si quieres
        texto = fuente.render(self.pregunta, True, color)
        pantalla.blit(texto, (self.x + 10, self.y + 100))

# ========= GAME LOGIC =========
def generar_pregunta():
    a = random.randint(1, 10 + nivel)
    b = random.randint(1, 10 + nivel)
    op = random.choice(["+", "-", "*"])
    pregunta = f"{a} {op} {b}"
    respuesta = eval(pregunta)
    return pregunta, respuesta, op

def nueva_ronda():
    global enemigo_actual
    preg, res, op = generar_pregunta()
    enemigo_actual = Enemigo(preg, res, op, velocidad)

# ========= SCREENS =========
def mostrar_menu():
    pantalla.blit(fondo_menu, (0, 0))
    # Título
    sombra = fuente_grande.render("Invasores Matemáticos", True, NEGRO)
    pantalla.blit(sombra, (ANCHO//2 - sombra.get_width()//2 + 2, 152))
    titulo = fuente_grande.render("Invasores Matemáticos", True, ROJO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))

    # Caja de nombre
    rect = pygame.Rect(ANCHO//2 - 200, 340, 400, 50)
    pygame.draw.rect(pantalla, (255, 255, 255), rect, border_radius=10)
    pygame.draw.rect(pantalla, NEGRO, rect, 2, border_radius=10)
    nombre_texto = fuente.render("Nombre: " + nombre_jugador, True, NEGRO)
    pantalla.blit(nombre_texto, (ANCHO//2 - nombre_texto.get_width()//2, 350))

    sombra_sub = fuente.render("ENTER = Jugar    ESC = Salir", True, BLANCO)
    pantalla.blit(sombra_sub, (ANCHO//2 - sombra_sub.get_width()//2 + 2, 422))
    instruccion = fuente.render("ENTER = Jugar    ESC = Salir", True, NEGRO)
    pantalla.blit(instruccion, (ANCHO//2 - instruccion.get_width()//2, 420))

    pygame.display.flip()

def dibujar_juego():
    pantalla.blit(fondo_juego, (0, 0))
    enemigo_actual.dibujar()

    # Input
    caja = pygame.Rect(50, ALTO - 100, 700, 50)
    pygame.draw.rect(pantalla, BLANCO, caja, border_radius=10)
    pygame.draw.rect(pantalla, NEGRO, caja, 2, border_radius=10)
    texto_entrada = fuente.render("Tu respuesta: " + entrada_usuario, True, NEGRO)
    pantalla.blit(texto_entrada, (60, ALTO - 90))

    # HUD
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    texto_vidas   = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    texto_nivel   = fuente.render(f"Nivel: {nivel}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))
    pantalla.blit(texto_nivel,   (ANCHO//2 - texto_nivel.get_width()//2, 10))
    pantalla.blit(texto_vidas,   (ANCHO - 150, 10))

    pygame.display.flip()

def mostrar_game_over():
    global en_menu
    play(sonido_gameover)
    pantalla.fill(NEGRO)
    titulo = fuente_grande.render("¡GAME OVER!", True, ROJO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 110))

    resumen = fuente.render(f"{nombre_jugador} - Puntaje final: {puntaje}", True, BLANCO)
    pantalla.blit(resumen, (ANCHO//2 - resumen.get_width()//2, ALTO//2 - 35))

    instruccion = fuente.render("R = Reintentar   M = Menú   ESC = Salir", True, GRIS)
    pantalla.blit(instruccion, (ANCHO//2 - instruccion.get_width()//2, ALTO//2 + 40))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    play(sonido_tecla)
                    reset_juego()
                    nueva_ronda()
                    esperando = False
                elif evento.key == pygame.K_m:
                    play(sonido_tecla)
                    reset_juego()
                    en_menu = True
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    play(sonido_tecla)
                    pygame.quit(); sys.exit()

# ========= MAIN LOOP =========
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    reloj.tick(FPS)

    if en_menu:
        mostrar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre_jugador.strip():
                        play(sonido_tecla)
                        reset_juego()
                        en_menu = False
                        nueva_ronda()
                elif evento.key == pygame.K_ESCAPE:
                    play(sonido_tecla)
                    ejecutando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                else:
                    if evento.unicode.isalnum() and len(nombre_jugador) < 15:
                        nombre_jugador += evento.unicode
        continue

    if enemigo_actual is None:
        nueva_ronda()

    # Eventos en juego
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            guardar_puntaje()
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                play(sonido_tecla)
                try:
                    if int(entrada_usuario) == enemigo_actual.respuesta:
                        play(sonido_correcto)
                        puntaje += 10
                        nivel += 1
                        velocidad += 0.25
                    else:
                        play(sonido_incorrecto)
                        vidas -= 1
                    entrada_usuario = ""
                    nueva_ronda()
                except Exception:
                    entrada_usuario = ""
                    nueva_ronda()
            elif evento.key == pygame.K_BACKSPACE:
                entrada_usuario = entrada_usuario[:-1]
            else:
                if evento.unicode.isdigit() or (evento.unicode == '-' and entrada_usuario == ''):
                    entrada_usuario += evento.unicode

    # Lógica de caída / timeout
    enemigo_actual.mover()
    if enemigo_actual.y > ALTO - 150:
        play(sonido_tiempo)
        vidas -= 1
        entrada_usuario = ""
        nueva_ronda()

    # Game Over
    if vidas <= 0:
        guardar_puntaje()
        mostrar_game_over()
        if en_menu:
            continue

    # Render
    dibujar_juego()

pygame.quit()
sys.exit()
