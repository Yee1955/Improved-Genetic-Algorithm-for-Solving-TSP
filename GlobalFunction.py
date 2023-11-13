import math
import random

class State:
    chromosome = None
    fitness = None

    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.fitness == other.fitness


def calculate_fitness(distances, chromosome):
    f = 0
    problem_length = len(chromosome)
    for i in range(problem_length - 1):
        f += distances[chromosome[i]][chromosome[i + 1]]

    return -f


def create_initial_state(problem_length, distance):
    chromosome = greedy_search(distance, problem_length)

    s = State()
    s.chromosome = chromosome
    return s


def read_distances(file):
    distances = []
    file = open(file + '_dist.txt')
    for i in range(7):
        next(file)
    for line in file:
        line = line.rstrip().lstrip().split(" ")
        for num in line:
            try:
                distances.append(int(num))
            except:
                x = 0

    n = int(math.sqrt(len(distances)))
    l = distances
    return [l[i:i + n] for i in range(0, len(l), n)]


def read_coordinates(file):
    coordinates = []
    file = open(file + '_xy.txt')
    for i in range(7):
        next(file)

    for line in file:
        line = ' '.join(line.lstrip().rstrip().split(' ')).split()
        coordinates.append((float(line[0]), float(line[1])))

    return coordinates

def greedy_search(distance, problem_length):
    path = []
    visited = set()  # Use a set to keep track of visited cities for faster lookup

    # Choose a random city to start with and add it to the path and visited cities
    current_city = random.randint(0, problem_length - 1)
    path.append(current_city)
    visited.add(current_city)

    # Continue until the path includes all cities
    while len(path) < problem_length:
        # Initialize shortest_distance with a large number
        shortest_distance = float('inf')
        # Initialize the next city as None
        next_city = None
        
        # Check all cities to find the nearest unvisited city
        for city in range(problem_length):
            if city not in visited and distance[current_city][city] < shortest_distance:
                shortest_distance = distance[current_city][city]
                next_city = city

        # If we found a next city, add it to the path and mark it as visited
        if next_city is not None:
            path.append(next_city)
            visited.add(next_city)
            current_city = next_city
        else:
            # If no next city is found, break the loop (this shouldn't happen if the distance matrix is correct)
            break

    return path

def calculate_index(fitness, runtime):
    # Calculate total seconds
    total_seconds = runtime.total_seconds()

    normalize_fitness = -fitness
    normalize_runtime = int(total_seconds)

    try:
        index = 10000000 / ((normalize_fitness) * normalize_runtime)
    except ZeroDivisionError:
        index = 0
    
    return index