#include "lru_cache.hpp"
#include <iostream>

//Secuencia 1: caso normal (sin eviction todavía)
void secuenciaNormal() {
    std::cout << "\n Secuencia 1: normal \n";
    TraceLogger logger("trace_normal.jsonl");
    LRUCache cache(3, &logger);
    cache.put(1, 10);
    cache.put(2, 20);
    cache.get(1);       // hit, mueve 1 al frente
    cache.put(3, 30);
    std::cout << "eventos: " << logger.step
              << " | tamano: " << cache.size() << "/" << cache.capacity() << "\n";
}

//Secuencia 2: caso borde — cache vacía (primer get antes de cualquier put)
void secuenciaVacia() {
    std::cout << "\n Secuencia 2: cache vacia \n";
    TraceLogger logger("trace_vacia.jsonl");
    LRUCache cache(2, &logger);
    cache.get(1);        // miss, cache vacía
    cache.put(1, 100);
    cache.get(1);         // hit ahora
    std::cout << "eventos: " << logger.step
              << " | tamano: " << cache.size() << "/" << cache.capacity() << "\n";
}

//Secuencia 3: caso borde — cache llena, fuerza eviction
void secuenciaEviction() {
    std::cout << "\n Secuencia 3: eviction \n";
    TraceLogger logger("trace_eviction.jsonl");
    LRUCache cache(2, &logger);
    cache.put(1, 10);
    cache.put(2, 20);
    cache.put(3, 30);    // cache llena -> evict key 1 (LRU)
    cache.get(1);         // miss, ya no está
    cache.get(2);         // hit
    std::cout << "eventos: " << logger.step
              << " | tamano: " << cache.size() << "/" << cache.capacity() << "\n";
}

//Secuencia 4: caso extremo — capacidad 1
void secuenciaCapacidadUno() {
    std::cout << "\n Secuencia 4: capacidad 1 \n";
    TraceLogger logger("trace_capacidad_uno.jsonl");
    LRUCache cache(1, &logger);
    cache.put(1, 10);
    cache.put(2, 20);     // evict inmediato del 1
    cache.get(1);          // miss
    cache.get(2);          // hit
    std::cout << "eventos: " << logger.step
              << " | tamano: " << cache.size() << "/" << cache.capacity() << "\n";
}

int main() {
    secuenciaNormal();
    secuenciaVacia();
    secuenciaEviction();
    secuenciaCapacidadUno();
    std::cout << "\nListo. 4 archivos trace.jsonl generados.\n";
    return 0;
}

