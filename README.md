# SCC Strongly Connected Components

Este repositorio se prepara para producir un video educativo animado sobre SCC (Strongly Connected Components) usando un enfoque trace-driven:

- Implementación real del algoritmo de Tarjan en C++.
- Emisión de trazas JSONL como fuente de verdad para la animación.
- Render en Python + Manim Community por escenas.
- Concat de clips finales en `out/final.mp4`.

## Estado inicial

Este repositorio está en la fase de infraestructura y bootstrap del proyecto. La parte funcional de C++ y la animación se implementará progresivamente con commits lógicos.

## Objetivo del proyecto

Explicar visualmente cómo funciona el algoritmo de Tarjan para encontrar componentes fuertemente conexos en un grafo dirigido, mostrando claramente la relación entre los valores de `disc`, `low`, la pila DFS y el criterio de cierre de un SCC.

## Requisitos en Arch Linux

Para trabajar en Arch Linux con este proyecto, conviene seguir esta preparación inicial:

1. Verificar si las dependencias del sistema están instaladas con `pacman -Q`.
2. Si faltan paquetes, instalar los necesarios con `sudo pacman -S --needed ...`.
3. Crear un entorno virtual local con `python -m venv .venv`.
4. Activarlo y instalar la dependencia de Manim con `pip install manim`.
5. Ejecutar el script idempotente `scripts/setup_arch.sh` para repetir el proceso de forma segura.

Paquetes típicos recomendados en Arch:

- `base-devel`, `gcc`, `cmake`, `make`
- `python`, `python-pip`, `python-virtualenv`
- `cairo`, `pango`, `pkgconf`, `harfbuzz`, `fribidi`
- `ffmpeg`, `sox`
- `git`, `openssl`, `mesa`

## Preparación del entorno

```bash
cd SCC-Strongly-Connected-Components-
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Script de setup

El script `scripts/setup_arch.sh` es idempotente y se encarga de:

- detectar si faltan paquetes del sistema,
- instalarlos con `pacman` cuando corresponde,
- crear el entorno virtual si no existe,
- instalar las dependencias de Python desde `requirements.txt`,
- compilar el proyecto C++ si el `Makefile` de `cpp` ya está disponible.

```bash
bash scripts/setup_arch.sh
```

## Flujo de trabajo previsto

- Compilar C++: `make -C cpp`
- Generar trazas: `make traces`
- Renderizar escenas por partes: `make s04`
- Concatenar: `make concat`
- Output final: `out/final.mp4`

> La animación usa un preset de Manim `-qh` para que todas las escenas compartan resolución y formato compatibles con `ffmpeg concat -c copy`.
