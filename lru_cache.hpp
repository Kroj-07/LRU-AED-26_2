#pragma once
#include <unordered_map>
#include <string>
#include <fstream>
#include <vector>
#include <stdexcept>

struct TraceLogger {
    std::ofstream out;
    int step = 0;

    explicit TraceLogger(const std::string& path): out(path) {
        if (!out) throw std::runtime_error("No se pudo abrir " + path);
    }

    void log(const std::string& op, int key, int value,
             const std::vector<int>& list_order, 
             const std::vector<std::pair<int,int>>& cache_state,
             bool hit, bool evicted = false, int evicted_key = -1) {
        out << "{"
            << "\"step\":" << step++ << ","
            << "\"op\":\"" << op << "\","
            << "\"key\":" << key << ","
            << "\"value\":" << value << ","
            << "\"hit\":" << (hit ? "true" : "false") << ","
            << "\"evicted\":" << (evicted ? "true" : "false") << ","
            << "\"evicted_key\":" << evicted_key << ","
            << "\"list_order\":[";
        for (size_t i = 0; i < list_order.size(); i++) {
            out << list_order[i];
            if (i + 1 < list_order.size()) out << ",";
        }
        out << "]}\n";
        out.flush(); // por si el programa se corta a mitad de la demo
    }
};

struct Node {
    int key, value;
    Node* prev = nullptr;
    Node* next = nullptr;
    Node(int k, int v) : key(k), value(v) {}
};


class LRUCache {
public:
    LRUCache(int capacity, TraceLogger* logger)
        : cap(capacity), logger(logger) {
        if (cap <= 0) throw std::invalid_argument("La capacidad debe ser > 0");
        // Nodos centinela: evitan chequear nullptr en los bordes de la lista.
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head -> next = tail;
        tail -> prev = head;
    }

    ~LRUCache() {
        Node* cur = head;
        while (cur) {
            Node* nxt = cur->next;
            delete cur;
            cur = nxt;
        }
    }

    LRUCache(const LRUCache&) = delete;
    LRUCache& operator=(const LRUCache&) = delete;

    int get(int key) {
        auto it = map.find(key);
        if (it == map.end()) {
            logger -> log("get", key, -1, listOrder(), cacheState(), /*hit=*/false);
            return -1; // miss (en un caso real usarían std::optional<int>)
        }
        Node* node = it -> second;
        moveToFront(node);
        logger -> log("get", key, node->value, listOrder(), cacheState(), /*hit=*/true);
        return node -> value;
    }

   
    void put(int key, int value) {
        auto it = map.find(key);
        if (it != map.end()) {
            it -> second -> value = value;
            moveToFront(it -> second);
            logger -> log("put", key, value, listOrder(), cacheState(), /*hit=*/true);
            return;
        }

        bool didEvict = false;
        int evictedKey = -1;
        if ((int)map.size() >= cap) {
            evictedKey = evict();
            didEvict = true;
        }

        Node* node = new Node(key, value);
        map[key] = node;
        insertFront(node);
        logger -> log("put", key, value, listOrder(), cacheState(), /*hit=*/false, didEvict, evictedKey);
    }

    int size() const { return (int)map.size(); }
    int capacity() const { return cap; }

private:
    int cap;
    Node* head; // sentinel: head->next es el MRU (+ recientemente usado)
    Node* tail; // sentinel: tail->prev es el LRU (- recientemente usado)
    std::unordered_map<int, Node*> map;
    TraceLogger* logger;

    void insertFront(Node* node) {
        node -> next = head -> next;
        node -> prev = head;
        head -> next -> prev = node;
        head -> next = node;
    }

    void removeNode(Node* node) {
        node -> prev -> next = node -> next;
        node -> next -> prev = node -> prev;
    }

    void moveToFront(Node* node) {
        removeNode(node); insertFront(node);
    }

    std::vector<int> listOrder() const {
        std::vector<int> order;
        for (Node* cur = head -> next; cur != tail; cur = cur -> next)
            order.push_back(cur -> key);
        return order;
    }

    std::vector<std::pair<int,int>> cacheState() const {
        std::vector<std::pair<int,int>> state; 
        for(Node* cur = head -> next; cur!=tail; cur = cur -> next){
            state.push_back({cur -> key, cur -> value});
        } return state;
    }

    int evict() {
        if(head -> next == tail) return -1; // caché vacía, se llama
    // cuando map.size() >= cap, no debería pasar si cap > 0

        Node* lru = tail -> prev; 
        int k = lru -> key;
        removeNode(lru); // desconecta double linked list
        map.erase(k); // elimina hash map
        delete lru; 
        return k;
    }
};
