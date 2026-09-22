#include "lru_cache.hpp"
#include <iostream>

int main() {
    TraceLogger logger("trace.jsonl");
    LRUCache cache(4, &logger); // capacidad 4, suficiente para no evictar aún

    cache.put(1, 10); // list: [1]
    cache.put(2, 20); // list: [2,1]
    cache.put(3, 30); // list: [3,2,1]

    cache.get(1);     // hit -> list: [1,3,2]

    cache.get(99);    // miss -> list no cambia: [1,3,2]

    cache.put(2, 999); // hit en put -> list: [2,1,3]

    std::cout << "Trace generado en trace.jsonl (" << logger.step
              << " eventos). Tamano final de la cache: " << cache.size()
              << "/" << cache.capacity() << "\n";
    return 0;
}
