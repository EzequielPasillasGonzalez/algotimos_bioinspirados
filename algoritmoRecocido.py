import numpy as np
import random


n_cities = 5              # Numero de ciudades
initial_temp = 100.0      # Temperatura inicial
cooling_rate = 0.99       # Tasa de enfriamiento
n_iterations = 1000       # Numero maximo de iteraciones

# Matriz de distancias entre ciudades
np.random.seed(42)
distance_matrix = np.random.randint(1, 100, size=(n_cities, n_cities))
distance_matrix = (distance_matrix + distance_matrix.T) / 2  # Hacerla simetrica

# Calcular la longitud de un camino
def calculate_path_length(path, distance_matrix):
    return sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1)) + distance_matrix[path[-1], path[0]]

# Generar un vecino intercambiando dos ciudades en el camino actual
def get_neighbor(path):
    new_path = path.copy()
    i, j = random.sample(range(len(path)), 2)
    new_path[i], new_path[j] = new_path[j], new_path[i]
    return new_path

def simulated_annealing():
    # Generar un camino inicial aleatorio
    current_path = list(range(n_cities))
    random.shuffle(current_path)
    current_length = calculate_path_length(current_path, distance_matrix)
    
    best_path = current_path
    best_length = current_length
    temp = initial_temp

    for iteration in range(n_iterations):
        # Generar un vecino y calcular su longitud
        neighbor_path = get_neighbor(current_path)
        neighbor_length = calculate_path_length(neighbor_path, distance_matrix)
        
        # Calcular el cambio de energia
        delta = neighbor_length - current_length

        # Aceptar el cambio con probabilidad dependiente de la temperatura
        if delta < 0 or random.random() < np.exp(-delta / temp):
            current_path = neighbor_path
            current_length = neighbor_length

            # Actualizar el mejor camino si el nuevo es mejor
            if current_length < best_length:
                best_path = current_path
                best_length = current_length

        # Disminuir la temperatura
        temp *= cooling_rate
        
        print(f"Iteraciin {iteration + 1}: Mejor longitud = {best_length}")

    return best_path, best_length

def main():    
    best_path, best_length = simulated_annealing()
    print(f"\nMejor camino encontrado: {best_path} con longitud = {best_length}")



if __name__ == '__main__':
    main()

