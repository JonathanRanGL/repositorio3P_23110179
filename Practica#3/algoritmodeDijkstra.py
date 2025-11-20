import networkx as nx
import matplotlib.pyplot as plt
import heapq
import time

def visualizar_dijkstra(grafo_dict, inicio, fin):
    # --- CONFIGURACIÓN GRÁFICA ---
    G = nx.DiGraph() # Grafo dirigido
    for nodo, vecinos in grafo_dict.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)

    # Posición fija de los nodos
    pos = nx.spring_layout(G, seed=42) 
    
    # Configuración inicial de la ventana
    plt.figure(figsize=(10, 7))
    ax = plt.gca()
    
    # --- VARIABLES ALGORITMO ---
    distancias = {nodo: float('inf') for nodo in G.nodes}
    distancias[inicio] = 0
    previos = {nodo: None for nodo in G.nodes}
    cola = [(0, inicio)]
    visitados = set()

    # --- FUNCIÓN DE DIBUJO ---
    def dibujar_estado(nodo_actual=None, vecinos_actuales=[], camino_final=[]):
        plt.cla() # Limpiar gráfico anterior
        plt.title(f"Simulación Dijkstra: Buscando ruta de {inicio} a {fin}")
        
        # Definir colores de nodos
        colores_nodos = []
        for n in G.nodes:
            if n in camino_final:
                colores_nodos.append('#32CD32') # Verde lima (Camino final)
            elif n == nodo_actual:
                colores_nodos.append('#FFD700') # Dorado (Procesando actualmente)
            elif n in visitados:
                colores_nodos.append('#ADD8E6') # Azul claro (Ya visitado/cerrado)
            else:
                colores_nodos.append('#D3D3D3') # Gris (No descubierto)

        # Dibujar nodos y aristas base
        nx.draw_networkx_nodes(G, pos, node_color=colores_nodos, node_size=700)
        nx.draw_networkx_labels(G, pos)
        
        # Dibujar aristas (Gris por defecto)
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
        
        # Resaltar aristas que se estan evaluando en este momento
        if nodo_actual:
            aristas_activas = [(nodo_actual, v) for v in vecinos_actuales]
            nx.draw_networkx_edges(G, pos, edgelist=aristas_activas, edge_color='red', width=2)
        
        # Resaltar camino final si existe
        if camino_final:
            aristas_camino = list(zip(camino_final, camino_final[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, edge_color='#32CD32', width=3)

        # Etiquetas de peso en las aristas
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        # Etiquetas de distancia actual sobre los nodos
        pos_attrs = {k: (v[0], v[1] + 0.1) for k, v in pos.items()}
        labels_dist = {n: (f"{distancias[n]}" if distancias[n] != float('inf') else "∞") for n in G.nodes}
        nx.draw_networkx_labels(G, pos_attrs, labels=labels_dist, font_color='blue', font_size=8)

        plt.pause(1.5) # PAUSA PARA VER LA ANIMACIÓN (1.5 segundos por paso)

    # --- BUCLE PRINCIPAL ---
    while cola:
        dist_actual, u = heapq.heappop(cola)
        
        # Dibujar estado: Ubicación: 'u'
        dibujar_estado(nodo_actual=u, vecinos_actuales=list(grafo_dict[u].keys()) if u in grafo_dict else [])
        
        if u == fin:
            break
            
        if dist_actual > distancias[u]:
            continue
        
        visitados.add(u)
        
        # Explorar vecinos
        if u in grafo_dict:
            for v, peso in grafo_dict[u].items():
                if dist_actual + peso < distancias[v]:
                    distancias[v] = dist_actual + peso
                    previos[v] = u
                    heapq.heappush(cola, (distancias[v], v))
    
    # --- RECONSTRUCCIÓN DEL CAMINO ---
    camino = []
    curr = fin
    if distancias[fin] != float('inf'):
        while curr is not None:
            camino.insert(0, curr)
            curr = previos[curr]
            
    # Dibujar estado final
    print(f"Costo final: {distancias[fin]}")
    print(f"Ruta: {camino}")
    dibujar_estado(camino_final=camino)
    plt.show() # Mantener ventana abierta al final

# --- DATOS ---
mi_grafo = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
    'E': {'C': 10, 'D': 2, 'Z': 3},
    'Z': {'D': 6, 'E': 3}
}

if __name__ == "__main__":
    visualizar_dijkstra(mi_grafo, 'A', 'Z')