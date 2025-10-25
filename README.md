# Invasores Matemáticos (Math Invaders)

Juego educativo tipo *Space Invaders* para practicar operaciones básicas (suma, resta, multiplicación, división) mientras te diviertes.

## Características
- Aliens temáticos por operación (plus, minus, mul, etc.).
- Sonidos para aciertos/errores, pantalla de game over y puntajes.
- Código en **Python** (recomendado Python 3.10+). Funciona con `pygame`.

> **Nota:** Este README es una plantilla. Ajusta comandos, controles y dependencias exactas según tu código (`main.py`).

## Requisitos
- Python 3.10 o superior
- pip (gestor de paquetes)
- Recomendado: entorno virtual (`venv`)

## Instalación (Windows/Mac/Linux)

```bash
# 1) Clonar el repo
git clone https://github.com/<TU_USUARIO>/<TU_REPO>.git
cd <TU_REPO>

# 2) (Opcional) Crear entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar
```bash
python main.py
```
> Si tu archivo de entrada tiene otro nombre, cámbialo en el comando.

## Estructura sugerida
```
.
├─ main.py
├─ assets/
│  ├─ img/
│  └─ sfx/
├─ README.md
├─ requirements.txt
├─ .gitignore
└─ LICENSE
```
> Si ya tienes los recursos (imágenes/sonidos) en la raíz, puedes dejarlos tal cual o moverlos a `assets/` y actualizar las rutas en el código.

## Dependencias
- `pygame` (mínimo para correr el juego). Genera `requirements.txt` exacto con:
```bash
pip install pipreqs
pipreqs . --force
```

## Controles (edita según tu juego)
- Flechas izquierda/derecha para moverse
- Barra espaciadora para disparar
- ESC para salir

## Empaquetado (opcional)
Para generar un ejecutable con **PyInstaller**:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```
Si ya usas un `*.spec`, puedes compilar con:
```bash
pyinstaller InvasoresMatematicos.spec
```

## Licencia
MIT. ¡Úsalo, modifícalo y compártelo!