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
2. Elegir el _target_ `test_lru`.
3. Correr aquel _target_ para generar los _trace.jsonl_

> El proyecto también incluye el _target_ `main_A`, que corresponde a las
> pruebas propias de la implementación de la LRU Cache; sin embargo, aquel _target_ no es necesario
> para generar los _traces_ de la animación.

## Procedimiento para generar animación

La animación se construye con _Manim_ a partir de los archivos `trace_*.jsonl` que genera `test_lru`. Por lo tanto, primero se debe compilar y correr `test_lru`, y luego renderizar la animación como se indicó previamente. Al renderizarlo se producirán un total de 4 archivos en el directorio:

| Archivo | Tipo de caso |
|:-------:|:------------:|
| `trace_normal.jsonl` | Uso normal (sin eviction) |
| `trace_vacia.jsonl` | Caso borde: caché vacía |
| `trace_eviction.jsonl` | Caso borde: desalojo por capacidad máxima |
| `trace_capacidad_uno.jsonl` | Caso extremo: capacidad 1 |

Cada archivo contiene una línea _JSON_ por cada operación `get`/`put` ejecutada, con los campos:
   `step`, `op`, `key`, `value`, `hit`, `evicted`, `evicted_key` y `list_order`.

> Los `.jsonl` deben estar en el mismo directorio desde donde se llama a _Manim_, porque `animacion.py` los abre con rutas relativas (`open(archivo, "r")`).
> Además, se requiere _FFmpeg_ disponible en el directorio.

Para renderizar la animación, desde el directiorio que contiene `animacion.py` correr:

```bash
manim -pqh animacion.py LRUAnimacion
```

>El video no se rendizará si _Manim_ no está instalado, para verificar ello correr:
>
>```bash
>manim --version
>```

El video resultante se guardará en el directorio `media/videos/animacion/1080p60/LRUAnimacion.mp4`.

## Video y repositorio

- Video: [enlace al video](https://youtu.be/MaxEyjAYVAg)
- Repositorio: [enlace a este repositorio](https://github.com/Kroj-07/LRU-AED-26_2.git)
