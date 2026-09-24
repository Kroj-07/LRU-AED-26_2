import json
import sys
from manim import *


class LRUAnimacion(Scene):
    # Configuración de tiempos (en segundos)
    # Configuración de tiempos
    velocidad = 0.5
    tiempo_por_evento = 2.5

    # Tupla actualizada con los 4 archivos de test_lru.cpp
    traces_a_mostrar = [
        ("trace_normal.jsonl",
         "Caso de Uso Normal",
         "Capacidad: 3 elementos.\nDemuestra operaciones básicas: PUT(1), PUT(2), GET(1) y PUT(3).\nAl consultar el 1, este se mueve al frente como el MRU."),

        ("trace_vacia.jsonl",
         "Caso Borde: Caché Vacía",
         "Capacidad: 2 elementos.\nDemuestra qué ocurre al intentar consultar (GET 1)\ncuando la estructura aún no tiene elementos (MISS)."),

        ("trace_eviction.jsonl",
         "Caso Borde: Desalojo (Eviction)",
         "Capacidad: 2 elementos.\nSe insertan 3 elementos. Al superar el límite,\nse expulsa automáticamente el menos usado (LRU)."),

        ("trace_capacidad_uno.jsonl",
         "Caso Extremo: Capacidad Mínima",
         "Capacidad: 1 elemento.\nLa caché solo puede almacenar un nodo a la vez.\nCada nueva inserción expulsa inmediatamente a la anterior.")
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.valores_cacheados = {}

    def construct(self):
        self.titulo_intro()

        # Cambio clave: agregar 'descripcion' al desempaquetado del for
        for archivo, etiqueta_caso, descripcion in self.traces_a_mostrar:
            self.valores_cacheados.clear()

            try:
                with open(archivo, "r") as f:
                    eventos = [json.loads(line) for line in f]
            except FileNotFoundError:
                print(f"Archivo {archivo} no encontrado. Saltando...")
                continue

            # Pasamos la descripción a la escena
            self.mostrar_etiqueta_caso(etiqueta_caso, descripcion)

            for idx, evento in enumerate(eventos):
                self.actualizar_estado_interno(evento)
                self.mostrar_evento(evento, idx + 1)

        self.escena_complejidad()
        self.cierre()

    # Cambio clave: recibir y renderizar la variable 'descripcion'
    def mostrar_etiqueta_caso(self, etiqueta, descripcion):
        titulo = Text(etiqueta, font_size=36, color=YELLOW)
        # Se eliminó el parámetro text_alignment=LEFT
        desc_text = Text(descripcion, font_size=24, color=WHITE)
        grupo = VGroup(titulo, desc_text).arrange(DOWN, buff=0.6)

        self.play(FadeIn(grupo))
        self.wait(4.0)
        self.play(FadeOut(grupo))

    def actualizar_estado_interno(self, evento):
        if evento["op"].upper() == "PUT":
            self.valores_cacheados[evento["key"]] = evento["value"]

    def titulo_intro(self):
        titulo = Text("LRU Cache", font_size=48, color=BLUE)
        subtitulo = Text("Least Recently Used Cache", font_size=28, color=GREY)
        integrantes = Text(
            "Integrantes: [Nombre A], [Nombre B], Abigail Jaslin Cabanillas Ventocilla",
            font_size=20, color=GREY,
        )
        grupo_titulo = VGroup(titulo, subtitulo, integrantes).arrange(DOWN, buff=0.3)
        self.play(Write(titulo), FadeIn(subtitulo), FadeIn(integrantes))
        self.wait(1.0)
        self.play(FadeOut(grupo_titulo))

        tda = Text(
            "TDA: combinación de una Tabla Hash\ny una Lista Doblemente Enlazada",
            font_size=32, color=WHITE,
        )
        uso = Text(
            "Permite acceder y expirar elementos en O(1)\nsegún su orden de uso reciente",
            font_size=26, color=GREY,
        )
        grupo_tda = VGroup(tda, uso).arrange(DOWN, buff=0.4)
        self.play(FadeIn(tda))
        self.wait(0.8)
        self.play(FadeIn(uso))
        self.wait(1.2)
        self.play(FadeOut(grupo_tda))

        ejemplo = Text(
            "Ejemplo real: caché del navegador,\nmemoria de acceso rápido con espacio limitado",
            font_size=26, color=GREEN,
        )
        self.play(FadeIn(ejemplo))
        self.wait(1.2)
        self.play(FadeOut(ejemplo))


    def escena_complejidad(self):
        titulo = Text("Análisis de complejidad", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(titulo))
        self.wait(0.5)

        get_texto = Text(
            "get(key) → O(1)\nBúsqueda directa en la tabla hash",
            font_size=28, color=WHITE,
        )
        put_texto = Text(
            "put(key, value) → O(1)\nInsertar/mover un nodo en la lista\nenlazada no requiere recorrerla",
            font_size=28, color=WHITE,
        )
        grupo = VGroup(get_texto, put_texto).arrange(DOWN, buff=0.6).next_to(titulo, DOWN, buff=0.8)

        self.play(FadeIn(get_texto))
        self.wait(1.0)
        self.play(FadeIn(put_texto))
        self.wait(1.5)
        self.play(FadeOut(titulo), FadeOut(grupo))

    def mostrar_evento(self, evento, step):
        # 1. Agruparemos TODO lo de este evento aquí para borrarlo junto al final
        elementos_evento = VGroup()

        contador = Text(f"Paso {step}", font_size=20, color=WHITE).to_corner(UL)
        elementos_evento.add(contador)

        op = evento["op"].upper()
        key = evento["key"]
        valor = evento["value"]
        hit = evento.get("hit", False)
        evicted = evento.get("evicted", False)
        evicted_key = evento.get("evicted_key", None)
        list_order = evento["list_order"]

        color_op = GREEN if hit else RED
        if evicted:
            color_op = YELLOW

        texto_operacion = f"{op} {key}" + (f" = {valor}" if op == "PUT" else "")
        op_text = Text(texto_operacion, font_size=36, color=color_op).move_to(UP * 3.0)
        elementos_evento.add(op_text)

        if evicted:
            resultado = f"Evicted: {evicted_key}"
        elif hit:
            resultado = "HIT"
        else:
            resultado = "MISS"

        result_text = Text(resultado, font_size=28, color=color_op).next_to(op_text, DOWN, buff=0.2)
        elementos_evento.add(result_text)

        if len(list_order) == 0:
            vacio = Text("Cache vacía", font_size=32, color=GREY).move_to(ORIGIN)
            elementos_evento.add(vacio)

            self.play(FadeIn(elementos_evento), run_time=0.5)
            self.wait(self.tiempo_por_evento / self.velocidad)
            self.play(FadeOut(elementos_evento), run_time=0.3)
            return

        # Nodos de la estructura
        nodos = VGroup()
        for k in list_order:
            rect = Square(side_length=1.2, fill_color=BLUE_D, fill_opacity=0.8)
            valor_en_cache = self.valores_cacheados.get(k, "?")

            clave_label = Text(str(k), font_size=24, color=WHITE).move_to(rect)
            valor_label = Text(":" + str(valor_en_cache), font_size=16, color=WHITE).next_to(rect, DOWN, buff=0.1)

            nodo = VGroup(rect, clave_label, valor_label)
            nodos.add(nodo)

        nodos.arrange(RIGHT, buff=1.0).move_to(ORIGIN + DOWN * 0.5)
        elementos_evento.add(nodos)

        # Enlaces para representar visualmente la Lista Doblemente Enlazada
        if len(nodos) > 1:
            enlaces = VGroup()
            for i in range(len(nodos) - 1):
                flecha = DoubleArrow(
                    nodos[i][0].get_right(),
                    nodos[i + 1][0].get_left(),
                    buff=0.1,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                    color=GREY
                )
                enlaces.add(flecha)
            elementos_evento.add(enlaces)

        # Resaltar el MRU (Most Recently Used - al frente de la lista)
        if list_order:
            nodos[0][0].set_fill(PURPLE, opacity=0.9)
            mru_label = Text("MRU", font_size=18, color=PURPLE_A).next_to(nodos[0], UP, buff=0.2)
            elementos_evento.add(mru_label)

        # Mostrar todo el grupo
        self.play(FadeIn(elementos_evento), lag_ratio=0.1, run_time=0.8)

        # Esperar el tiempo configurado
        self.wait(self.tiempo_por_evento / self.velocidad)

        # 2. LIMPIEZA EXPLÍCITA: Desaparecer todo el evento antes de pasar al siguiente
        self.play(FadeOut(elementos_evento), run_time=0.3)

    def cierre(self):
        texto = Text("Fin de la simulación", font_size=36, color=BLUE)
        self.play(Write(texto))
        self.wait(2)