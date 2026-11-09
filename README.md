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
