cmake_minimum_required(VERSION 4.0)
project(LRU_AED_26_2)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

# Ejecutable de A: sus pruebas propias de la clase LRUCache
add_executable(main_A
        lru_cache.hpp
        main.cpp)

# Ejecutable de Persona C: las 4 secuencias de prueba que generan los trace_*.jsonl
add_executable(test_lru
        lru_cache.hpp
        test_lru.cpp)