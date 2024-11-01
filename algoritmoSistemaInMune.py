import numpy as np
import random

target        = [1, 0, 1, 1, 0, 1]  # Antigeno objetivo
n_antibodies  = 20                  # Numero de soluciones en cada generacion
clone_rate    = 0.1                 # Tasa de clonacion
mutation_rate = 0.1                 # Tasa de mutacion
generations   = 50

# Afinidad para maximizar el ajuste con el target
def affinity(antibody, target):
    return sum([1 if antibody[i] == target[i] else 0 for i in range(len(target))])

# Crear un anticuerpo aleatorio
def create_antibody(length):
    return [random.randint(0, 1) for _ in range(length)]

# Crear una poblacion inicial de anticuerpos
def create_population(size, length):
    return [create_antibody(length) for _ in range(size)]

# Clonacion y mutacion de anticuerpos de alta afinidad
def clone_and_mutate(population, target):
    new_population = []
    for antibody in population:
        clones = [antibody.copy() for _ in range(int(len(target) * clone_rate))]
        for clone in clones:
            if random.random() < mutation_rate:
                point = random.randint(0, len(clone) - 1)
                clone[point] = 1 - clone[point]  # Cambia 0 a 1 o viceversa
        new_population.extend(clones)
    return new_population

def artificial_immune_system():
    population = create_population(n_antibodies, len(target))

    for generation in range(generations):
        # Evaluacion de afinidad y seleccion de los mejores
        population = sorted(population, key=lambda x: affinity(x, target), reverse=True)
        best_antibodies = population[:n_antibodies // 2]

        # Clonacion y mutacion de los mejores anticuerpos
        population = clone_and_mutate(best_antibodies, target)

        # Generar nuevos anticuerpos aleatorios para mantener diversidad
        population.extend(create_population(n_antibodies - len(population), len(target)))

        # Informacion de la generacion actual
        best_solution = max(population, key=lambda x: affinity(x, target))
        print(f"Generacion {generation + 1}: Mejor afinidad = {affinity(best_solution, target)}")

        # Condicion de parada si se encuentra la solucion optima
        if affinity(best_solution, target) == len(target):
            print("¡Solucion optima encontrada!")
            break

def main():    
    artificial_immune_system()


if __name__ == '__main__':
    main()
