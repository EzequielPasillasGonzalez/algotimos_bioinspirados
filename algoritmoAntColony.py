import numpy as np
import random

n_ants = 10               # Numero de hormigas
n_cities = 5              # Numero de ciudades
n_iterations = 100        # Numero de iteraciones
alpha = 1.0               # Importancia relativa de las feromonas
beta = 5.0                # Importancia relativa de la heuristica (distancia)
evaporation_rate = 0.5    # Tasa de evaporacion de feromonas
initial_pheromone = 1.0   # Nivel inicial de feromonas en cada ruta


np.random.seed(42)
distance_matrix = np.random.randint(1, 100, size=(n_cities, n_cities))
distance_matrix = (distance_matrix + distance_matrix.T) / 2  # Para hacerla simetrica

# Inicializacion de feromonas
pheromone_matrix = np.full((n_cities, n_cities), initial_pheromone)

# Calcular la probabilidad de elegir la proxima ciudad
def calculate_transition_probabilities(current_city, visited, pheromone_matrix, distance_matrix):
    pheromone = pheromone_matrix[current_city]
    heuristic = 1 / (distance_matrix[current_city] + 1e-10) 
    probabilities = (pheromone ** alpha) * (heuristic ** beta)

    # Excluir ciudades ya visitadas
    probabilities[visited] = 0
    return probabilities / probabilities.sum()

# Simulacion del recorrido de una hormiga
def simulate_ant(pheromone_matrix, distance_matrix):
    visited = []
    current_city = random.randint(0, n_cities - 1)  # Seleccion de ciudad inicial aleatoria
    visited.append(current_city)
    
    while len(visited) < n_cities:
        probabilities = calculate_transition_probabilities(current_city, visited, pheromone_matrix, distance_matrix)
        next_city = np.random.choice(range(n_cities), p=probabilities)
        visited.append(next_city)
        current_city = next_city

    # Regreso a la ciudad inicial para completar el recorrido
    visited.append(visited[0])
    return visited

# Actualizacion de feromonas en funcion de la longitud del recorrido de cada hormiga
def update_pheromones(pheromone_matrix, ant_paths, distance_matrix):
    pheromone_matrix *= (1 - evaporation_rate)  # Evaporacion global de feromonas
    
    for path in ant_paths:
        path_length = sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            city_a, city_b = path[i], path[i + 1]
            pheromone_matrix[city_a, city_b] += 1 / path_length  # Deposito de feromonas en caminos

def ant_colony_optimization():
    best_path = None
    best_path_length = float('inf')
    
    for iteration in range(n_iterations):
        ant_paths = [simulate_ant(pheromone_matrix, distance_matrix) for _ in range(n_ants)]
        
        # Evaluacion de caminos y actualizacion del mejor camino
        for path in ant_paths:
            path_length = sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))
            if path_length < best_path_length:
                best_path_length = path_length
                best_path = path

        # Actualizacion de feromonas
        update_pheromones(pheromone_matrix, ant_paths, distance_matrix)
        
        print(f"Iteracion {iteration + 1}: Mejor camino = {best_path} con longitud = {best_path_length}")



def main():    
    ant_colony_optimization()



if __name__ == '__main__':
    main()

