import networkx as nx
import matplotlib.pyplot as plt

# --- Clase para manejar los conjuntos disjuntos (Union-Find) ---
class UnionFind:
    def __init__(self, nodos):
        # Al principio, cada nodo es su propio padre 
        self.padre = {nodo: nodo for nodo in nodos}

    def find(self, nodo):
        
        if self.padre[nodo] != nodo:
            self.padre[nodo] = self.find(self.padre[nodo]) # Compresión de ruta
        return self.padre[nodo]

    def union(self, nodo1, nodo2):
        # Unir dos conjuntos conectando sus raíces
        raiz1 = self.find(nodo1)
        raiz2 = self.find(nodo2)
        if raiz1 != raiz2:
            self.padre[raiz1] = raiz2
            return True # Unión exitosa
        return False # Ya estaban unidos (formaría un ciclo)

# --- Clase principal del Simulador ---
class SimuladorKruskal:
    def __init__(self):
        self.aristas = []
        self.nodos = set()

    def agregar_arista(self, u, v, peso):
        # Guardar la arista como una tupla (u, v, peso)
        self.aristas.append((u, v, peso))
        self.nodos.add(u)
        self.nodos.add(v)

    def ejecutar_kruskal(self, buscar_maximo=False):
        
        tipo = "MÁXIMO" if buscar_maximo else "MÍNIMO"
        print(f"\n--- INICIANDO SIMULACIÓN: Árbol de {tipo} Coste ---")
        
        # 1. Ordenar aristas por peso
        # Si buscamos máximo, ordenamos de mayor a menor (reverse=True)
        # Si buscamos mínimo, ordenamos de menor a mayor (reverse=False)
        self.aristas.sort(key=lambda x: x[2], reverse=buscar_maximo)
        
        uf = UnionFind(self.nodos)
        arbol_resultado = []
        coste_total = 0
        
        step = 1
        print(f"{'Paso':<5} | {'Arista':<10} | {'Peso':<5} | {'Acción'}")
        print("-" * 45)

        for u, v, peso in self.aristas:
            raiz_u = uf.find(u)
            raiz_v = uf.find(v)

            if raiz_u != raiz_v:
                # No forman ciclo, aceptar la arista
                uf.union(u, v)
                arbol_resultado.append((u, v, peso))
                coste_total += peso
                print(f"{step:<5} | {u}-{v:<8} | {peso:<5} | ACEPTADA (Une conjuntos)")
            else:
                # Forman ciclo, descartaar
                print(f"{step:<5} | {u}-{v:<8} | {peso:<5} | RECHAZADA (Forma ciclo)")
            
            step += 1

        print("-" * 45)
        print(f"Coste Total del Árbol: {coste_total}")
        return arbol_resultado

    def visualizar(self, arbol_resultado, titulo="Resultado Kruskal"):
        # Usamos NetworkX para el gráfico y Matplotlib para dibujar
        G = nx.Graph()
        
        # Agregamos todas las aristas originales 
        for u, v, w in self.aristas:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42) # Layout fijo para que no se muevan los nodos

        plt.figure(figsize=(10, 6))
        plt.title(titulo)

        # 1. Dibujar el grafico  completo
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgray')
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.4, style='dashed')
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Etiquetas de peso para todas las aristas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # 2. Resaltar las aristas del Árbol solución (línea sólida y color)
        aristas_solucion = [(u, v) for u, v, w in arbol_resultado]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_solucion, width=3, edge_color='blue')

        print("\n> Generando gráfico... (Revisa la ventana emergente)")
        plt.axis('off')
        plt.show()

# --- Bloque principal de ejecución ---
if __name__ == "__main__":
    
    sim = SimuladorKruskal()

    # Agregar datos de prueba 
    # Formato: nodo_origen, nodo_destino, peso
    datos = [
        ('A', 'B', 4), ('A', 'H', 8),
        ('B', 'C', 8), ('B', 'H', 11),
        ('C', 'D', 7), ('C', 'F', 4), ('C', 'I', 2),
        ('D', 'E', 9), ('D', 'F', 14),
        ('E', 'F', 10),
        ('F', 'G', 2),
        ('G', 'H', 1), ('G', 'I', 6),
        ('H', 'I', 7)
    ]

    for u, v, w in datos:
        sim.agregar_arista(u, v, w)

    # Menú simple para probar
    print("1. Calcular Árbol de Mínimo Coste (MST)")
    print("2. Calcular Árbol de Máximo Coste")
    opcion = input("Elige una opción (1 o 2): ")

    if opcion == '1':
        resultado = sim.ejecutar_kruskal(buscar_maximo=False)
        sim.visualizar(resultado, "Kruskal - Mínimo Coste")
    elif opcion == '2':
        resultado = sim.ejecutar_kruskal(buscar_maximo=True)
        sim.visualizar(resultado, "Kruskal - Máximo Coste")
    else:
        print("Opción no válida.")