import networkx as nx
import matplotlib.pyplot as plt
import sys

# Definimos una clase simple para manejar el algoritmo de Prim
class SimuladorPrim:
    def __init__(self, vertices):
        self.V = vertices
        # Usaré una lista de adyacencia para guardar el grafo: [origen, destino, peso]
        self.grafo = [] 

    # Función para agregar aristas (caminos entre nodos)
    def agregar_arista(self, u, v, w):
        self.grafo.append([u, v, w])

    # Algoritmo principal de Prim
    def ejecutar_prim(self):
        # Nodos que ya visitamos y son parte del árbol
        visitados = [False] * self.V 
        # Para guardar las aristas que forman el Árbol Parcial Mínimo
        mst_aristas = []
        
        # Empezamos por el nodo 0
        visitados[0] = True
        num_aristas = 0
        peso_total = 0

        print("\n--- INICIO DEL SIMULADOR DE PRIM ---\n")
        print(f"{'Paso':<10} | {'Arista (Origen-Destino)':<25} | {'Peso':<10}")
        print("-" * 50)

        # El árbol tendrá (V-1) aristas
        while num_aristas < self.V - 1:
            minimo = sys.maxsize
            x = 0 # Nodo origen temporal
            y = 0 # Nodo destino temporal
            encontrado = False

            
            for i in range(len(self.grafo)):
                u, v, w = self.grafo[i]
                
                # Caso 1: u está visitado y v no
                if visitados[u] and not visitados[v]:
                    if w < minimo:
                        minimo = w
                        x = u
                        y = v
                        encontrado = True
                
                # Caso 2: v está visitado y u no (por si el grafo no es dirigido explícitamente)
                elif visitados[v] and not visitados[u]:
                    if w < minimo:
                        minimo = w
                        x = v
                        y = u
                        encontrado = True

           
            if encontrado:
                visitados[y] = True
                mst_aristas.append((x, y, minimo))
                peso_total += minimo
                num_aristas += 1
                print(f"Paso {num_aristas:<5} | {x} - {y:<23} | {minimo}")

        print("-" * 50)
        print(f"Costo total del Árbol Mínimo: {peso_total}\n")
        return mst_aristas

    # Función para la parte de la Gráfica
    def graficar(self, mst_aristas):
        G = nx.Graph()
        
        # Agregamos todas las aristas originales al gráfico (color gris)
        for u, v, w in self.grafo:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42) # Layout fijo para que no baile

        plt.figure(figsize=(8, 6))
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Dibujar todas las aristas (base)
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, edge_color='gray', style='dashed')
        
        # Dibujar las etiquetas de peso
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # RESALTAR el Árbol de Prim (Rojo y grueso)
        # Convertimos la lista de resultados a formato que entienda networkx
        aristas_mst_simple = [(u, v) for u, v, w in mst_aristas]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_mst_simple, width=4, edge_color='r')

        plt.title(f"Árbol Parcial Mínimo de Prim (Costo: {sum([w for u,v,w in mst_aristas])})")
        plt.axis('off')
        print("Generando gráfico...")
        plt.show()

# --- BLOQUE PRINCIPAL ---
if __name__ == "__main__":
    # Ejemplo
    nodos = 5
    simulador = SimuladorPrim(nodos)

    # Agregando conexiones: origen, destino, peso
    simulador.agregar_arista(0, 1, 2)
    simulador.agregar_arista(0, 3, 6)
    simulador.agregar_arista(1, 2, 3)
    simulador.agregar_arista(1, 3, 8)
    simulador.agregar_arista(1, 4, 5)
    simulador.agregar_arista(2, 4, 7)
    simulador.agregar_arista(3, 4, 9)

    # Ejecutar lógica
    resultado = simulador.ejecutar_prim()
    
    # Ejecutar gráfica
    simulador.graficar(resultado)