# [CS2023] Proyecto I: LRU Cache

**Estructura de datos:** _LRU Cache_.
**Curso:** CS2023 - Algoritmos y Estructuras de Datos (2026-2)
**Docente:** Víctor Racsó Galván Oyola

**Integrantes**:

|Nombre|Código|
|:----:|:----:|
| Abigail Jaslin Cabanillas Ventocilla | 202510438 |
| Azul Arbulú Silva | 202510303 |
| Kiara Luz Rojas Meza | 202510620 |

## Descripción del proyecto

El presente repositorio almacena el código para producir el video del funcionamiento de una
**LRU Cache**. Dentro del proyecto se tiene:

1. La implementación _LRU Cache en C++_ sin utilizar librerías estándar de caché ya existentes.
2. Un _script_ en _Python_ (_Manim_) utilizado para generar la animación correspondiente.
3. El video renderizado en `.mp4` con los requisitos planteados:
   - Introducción conceptual.
   - Demostración animada de `get` y `put`.
   - Casos borde relevantes (caché vacía, un solo elemento, desalojo en capacidad máxima).
   - Análisis de complejidad temporal.

## Requisitos

- Compilador _C++23_.
- _Python 3_ + _Manim_, para renderizar las escenas de animación.
- _Manim Community Edition_ (`pip install manim`).
-  _FFmpeg_ (requerido por _Manim_ para renderizar).

## Procedimiento de compilación y ejecución de pruebas

1. Abrir la carpeta del proyecto en _CLion_.
2. Elegir el _target_ **`test_lru`**.
3. Correr aquel _target_ para generar los _trace.jsonl_

> El proyecto también incluye el _target_ `main_A`, que corresponde a las
> pruebas propias de la implementación de la LRU Cache; sin embargo, aquel _target_ no es necesario
> para generar los _traces_ de la animación.

## Procedimiento para generar animación

...

## Video y repositorio

- Video: [enlace al video / YouTube no listado]
- Repositorio: [[enlace a este repositorio](https://github.com/Kroj-07/LRU-AED-26_2.git)]
