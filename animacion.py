import json
import sys
from manim import *

class LRUAnimacion(Scene):
    # Configuración de tiempos (en segundos)
    velocidad = 1.0           # factor de escala: >1 más rápido, <1 más lento
    tiempo_por_evento = 1.0   # pausa base después de cada evento

    def construct(self):
        # Elegir archivo de trace
        archivo = "trace_normal.jsonl"

        with open(archivo, "r") as f:
            eventos = [json.loads(line) for line in f]

        # Configurar duración total estimada
        print(f"Procesando {len(eventos)} eventos...")

        # Mostrar título introductorio
        self.titulo_intro()

        # Procesar cada evento
        for idx, evento in enumerate(eventos):
            self.mostrar_evento(evento, idx)
            self.wait(self.tiempo_por_evento / self.velocidad)

        # Cierre
        self.cierre()

    def titulo_intro(self):
        titulo = Text("Simulación de Caché LRU", font_size=48, color=BLUE)
        subtitulo = Text("Algoritmo Least Recently Used", font_size=28, color=GREY)
        grupo = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.3)
        self.play(Write(titulo), FadeIn(subtitulo))
        self.wait(0.8)
        self.play(FadeOut(grupo))

    def mostrar_evento(self, evento, step):
        # Limpiar escena manteniendo el fondo
        self.clear()

        # ----- Barra de progreso / contador -----
        contador = Text(f"Paso {step}", font_size=20, color=WHITE).to_corner(UL)

        # ----- Texto de operación -----
        op = evento["op"].upper()
        key = evento["key"]
        valor = evento["value"]
        hit = evento["hit"]
        evicted = evento["evicted"]
        evicted_key = evento["evicted_key"]
        list_order = evento["list_order"]

        # Color según resultado
        color_op = GREEN if hit else RED
        if evicted:
            color_op = YELLOW

        op_text = Text(f"{op} {key} = {valor}", font_size=36, color=color_op)
        op_text.move_to(UP * 3.5)

        # Resultado
        resultado = ""
        if evicted:
            resultado = f"Evicted: {evicted_key}"
        elif hit:
            resultado = "HIT"
        else:
            resultado = "MISS"
        result_text = Text(resultado, font_size=28, color=color_op).next_to(op_text, DOWN, buff=0.2)

        # ----- Representación de la lista -----
        if len(list_order) == 0:
            # Caché vacía
            vacio = Text("Cache vacía", font_size=32, color=GREY).move_to(ORIGIN)
            self.play(FadeIn(op_text), FadeIn(result_text), FadeIn(contador), FadeIn(vacio))
            self.wait(0.3)
            self.play(FadeOut(op_text), FadeOut(result_text), FadeOut(contador), FadeOut(vacio))
            return

        # Crear nodos
        nodos = VGroup()
        for k in list_order:
            rect = Square(side_length=1.2, fill_color=BLUE_D, fill_opacity=0.8)
            valor_en_cache = self.obtener_valor(evento, k)  # función para recuperar valor si está en trace
            clave_label = Text(str(k), font_size=24, color=WHITE).move_to(rect)
            valor_label = Text(":" + str(valor_en_cache), font_size=16, color=WHITE).next_to(rect, DOWN, buff=0.1)
            nodo = VGroup(rect, clave_label, valor_label)
            nodos.add(nodo)

        # Organizar horizontalmente
        nodos.arrange(RIGHT, buff=0.4)
        nodos.move_to(ORIGIN)

        # Marcar el nodo recién usado (el primero) con color morado
        if list_order:
            primer = list_order[0]
            for nodo in nodos:
                # El texto clave es el segundo elemento
                texto = nodo[1].text
                if str(primer) in texto:
                    nodo[0].set_fill(PURPLE, opacity=0.9)
                    break

        # Mostrar todo
        self.play(FadeIn(op_text), FadeIn(result_text), FadeIn(contador), FadeIn(nodos), lag_ratio=0.2)
        self.wait(0.4)

    def obtener_valor(self, evento, key):
        # El trace no incluye valores en list_order, pero podemos intentar
        # buscar en el evento si es un put con esa clave.
        # Si no, devolvemos un placeholder.
        # Idealmente deberías modificar el TraceLogger para incluir los valores en list_order.
        # Aquí simplemente devolvemos "?"
        return "?"

    def cierre(self):
        texto = Text("Fin de la simulación", font_size=36, color=BLUE)
        self.play(Write(texto))
        self.wait(2)