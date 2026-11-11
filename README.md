# SCC - Algoritmo de Tarjan (Visualización)

## Integrantes

- Curso: CS2023
- Integrantes: Javier Pariansullca, Alba Cabrera, Sebastián Falvy

## Descripción

Este proyecto visualiza el algoritmo de Tarjan para encontrar componentes fuertemente conexas (SCC) en un grafo dirigido. Usa una arquitectura **Trace-Driven**. Primero, un programa en C++ ejecuta Tarjan y genera una traza en formato JSON; luego, las escenas de Manim escritas en Python leen esa traza para construir la animación paso a paso. De esta forma, la visualización representa los eventos producidos por la ejecución del algoritmo.

## Estructura del Proyecto

```text
SCC-Strongly-Connected-Components-/
├── algorithm/              # Implementación C++ de Tarjan y ejecutable generado
│   └── tarjan.cpp
├── animation/              # Escenas de Manim y utilidades para grafos
│   ├── scene_00_title.py
│   ├── scene_01_concept.py
│   ├── scene_02_demo.py
│   └── utils/
│       └── graph.py
├── inputs/                 # Grafos de entrada en formato .txt
│   └── demo.txt
├── media/                  # Archivos temporales generados por Manim
├── output/                 # Traza JSON, partes y video final generados
├── .gitignore
├── README.md
└── run.sh                  # Compila, renderiza y une las escenas
```

## Requisitos e Instalación (Multi-SO)

Se necesita un compilador de C++ con soporte para C++17, Python, Manim Community, Cairo, Pango y FFmpeg. 
Sigue las instrucciones correspondientes a tu sistema operativo.

### Arch Linux y distribuciones basadas en Arch

Instala los paquetes del sistema con:

```bash
sudo pacman -S base-devel python python-pip cairo pango pkgconf ffmpeg
```

### Windows

La opción recomendada es ejecutar el proyecto dentro de **WSL (Windows Subsystem for Linux)** y seguir allí las instrucciones de Linux. Alternativamente, instala Python y FFmpeg manualmente, por ejemplo, con Chocolatey o Scoop. Para ejecutar el flujo completo sin WSL, abre Git Bash o ejecuta manualmente los comandos de compilación, generación de traza, renderizado de escenas y concatenación que aparecen en `run.sh`; también necesitarás un compilador C++ compatible y las dependencias de Manim.

### macOS

Instala las dependencias con Homebrew:

```bash
brew install cairo pango ffmpeg python
```

También necesitas un compilador de C++17, disponible con las herramientas de línea de comandos de Xcode.

## Entorno de Python

Desde la raíz del repositorio, crea el entorno virtual:

```bash
python -m venv .venv
```

Actívalo según tu sistema:

```bash
# Linux y macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bat
:: Windows Command Prompt
.venv\Scripts\activate.bat
```

Con el entorno activado, instala Manim:

```bash
pip install manim
```

## Uso / Renderizado

En Linux o macOS, ejecuta desde la raíz del proyecto:

```bash
./run.sh
```

El script compila `algorithm/tarjan.cpp`, genera la traza en `output/traza.json`, renderiza las escenas y concatena los videos. En Windows sin WSL, ejecuta manualmente los comandos del script o usa Git Bash con las dependencias necesarias instaladas.

El video final se guarda en `output/final.mp4`.

> [!NOTE]
> Las carpetas `media/` y `output/` se generan automáticamente durante el renderizado. Están incluidas en `.gitignore` porque contienen videos y otros archivos generados que pueden ocupar mucho espacio y no deben subirse al repositorio.
