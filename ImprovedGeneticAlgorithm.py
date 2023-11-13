from GlobalFunction import read_distances, read_coordinates, State, calculate_fitness, create_initial_state
import random
import operator
import math
import matplotlib.pyplot as plt
from datetime import datetime
import time

def rank_select_parents(brackets):
    try:
        rand = random.randint(1, brackets[len(brackets) - 1][1])
    except:
        x = 0
    i = 0
    while True:
        if brackets[i][0] <= rand <= brackets[i][1]:
            break
        i = i + 1

    while True:
        try:
            rand = random.randint(1, brackets[len(brackets) - 1][1])
        except:
            x = 0
        j = 0
        while True:
            if brackets[j][0] <= rand <= brackets[j][1]:
                if i != j:
                    return i, j
                else:
                    break
            j = j + 1


def calculate_rank_brackets(population):
    length = len(population)
    brackets = [0] * length
    brackets = [length - i for i in range(length)]
    for i in range(1, length):
        if population[i].fitness == population[i - 1].fitness:
            brackets[i] = brackets[i - 1]

    mul = 100 * k / sum(brackets)
    for i in range(length):
        brackets[i] = math.floor(brackets[i] * mul)

    brackets[0] = 1, brackets[0]
    for i in range(1, length):
        brackets[i] = brackets[i - 1][1] + 1, brackets[i - 1][1] + brackets[i]
        # x = brackets[i - 1][1] + 1
        # y = brackets[i - 1][1] + brackets[i]
        # if x < y: brackets[i] = x, y
        # else: brackets[i] = x, x

    return brackets


def select_new_generation(old_population, new_generation):
    new_generation.sort(key=operator.attrgetter('fitness'), reverse=True)
    i1 = 0
    i2 = 0
    result = []

    while len(result) != k:
        if old_population[i1].fitness < new_generation[i2].fitness:
            if new_generation[i2] not in result:
                result.append(new_generation[i2])
            i2 = i2 + 1
        else:
            if old_population[i1] not in result:
                result.append(old_population[i1])
            i1 = i1 + 1

    return result


def create_initial_population():
    population = []
    while len(population) != k:
        s = create_initial_state(problem_length)
        if s not in population:
            population.append(s)

    return population


def swapped_inverted_crossover(parent1, parent2):
    # Ensure the parents are of same length
    assert len(parent1) == len(parent2)
    
    #--- Two Points SIC ---
    # Create Subtour
    subtour1 = []
    subtour2 = []
    rand1 = random.randint(2, len(parent1) - 2)
    rand2 = rand1
    while rand1 == rand2: rand2 = random.randint(rand1, len(parent1) - 1)
    for i in range(rand1,rand2 + 1):
        subtour1.append(parent1[i])
        subtour2.append(parent2[i])

    # Create Head Part
    head1 = []
    head2 = []
    for i in range(rand1 - 1, - 1, -1):
        head1.append(parent1[i])
        head2.append(parent2[i])

    # Create Tail Part
    tail1 = []
    tail2 = []
    for i in range(len(parent1) - 1, rand1 + 2, -1):
        tail1.append(parent1[i])
        tail2.append(parent2[i])

    # Create Remaining Part
    remain1 = []
    remain2 = []
    for i in range(0, len(parent1)):
        if parent1[i] not in head2 and parent1[i] not in tail2:
            remain1.append(parent1[i])
        if parent2[i] not in head1 and parent2[i] not in tail1:
            remain2.append(parent2[i])

    o1 = tail2 + remain1 + head2
    o2 = tail1 + remain2 + head1

    o3 = head2 + remain1 + tail2
    o4 = head1 + remain2 + tail1



    #--- One Point SIC ---
    #Create Cutpoint
    rand = random.randint(2, len(parent1) - 2)

    # Create Head Part
    head1 = []
    head2 = []
    for i in range(rand, -1, -1):
        head1.append(parent1[i])
        head2.append(parent2[i])
    
    # Create Tail Part
    tail1 = []
    tail2 = []
    for i in range(len(parent1) - 1, rand1 -1, -1):
        tail1.append(parent1[i])
        tail2.append(parent2[i])
    
    # Create Remaining Part
    remain1 = []
    remain2 = []
    remain3 = []
    remain4 = []
    for i in range(0, len(parent1)):
        if parent1[i] not in head2: remain1.append(parent1[i])
        if parent2[i] not in head1: remain2.append(parent2[i])
        if parent1[i] not in tail2: remain3.append(parent1[i])
        if parent2[i] not in tail1: remain4.append(parent2[i])
    
    o5 = head1 + remain2
    o6 = remain2 + head1

    o7 = head2 + remain1
    o8 = remain1 + head2

    o9 = tail1 + remain4
    o10 = remain4 + tail1

    o11 = tail2 + remain3
    o12 = remain3 + tail2
    
    offsprings = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11, o12]
    return offsprings


# random.randint(1, 101) <= mutation_rate


def apply_mutation(chromosome):
    index = random.randint(0, problem_length - 1)
    value = random.randint(0, problem_length - 1)
    while value == chromosome[index]: value = random.randint(0, problem_length - 1)
    index2 = chromosome.index(value)
    chromosome[index], chromosome[index2] = value, chromosome[index]
    return chromosome


def genetic_algorithm():
    population = create_initial_population()
    for i in population:
        if i.fitness is None:
            i.fitness = calculate_fitness(distances, i.chromosome)

    i = iterations
    while i != 0:
        population.sort(key=operator.attrgetter('fitness'), reverse=True)
        if fitness <= population[0].fitness: break

        i -= 1

        new_generation = []
        brackets = calculate_brackets(population)
        while len(new_generation) != k:
            x, y = rank_select_parents(brackets)
            offsprings = crossover(population[x].chromosome, population[y].chromosome)

            for p in offsprings:
                if random.randint(1, 101) <= mutation_rate: p = apply_mutation(p)

            for j in offsprings:
                if len(new_generation) != k:
                    s = State()
                    s.chromosome = j
                    s.fitness = calculate_fitness(distances, s.chromosome)
                    if s not in new_generation: new_generation.append(s)
                else:
                    break

        population = select_new_generation(population, new_generation)

    return population[0], iterations - i

k = 100
mutation_rate = 3
iterations = 1000
fitness = -1000
file = "usca312"

distances = read_distances(file)
coordinates = read_coordinates(file)
problem_length = len(coordinates)
calculate_brackets = calculate_rank_brackets
crossover = swapped_inverted_crossover

time.ctime()
fmt = '%H:%M:%S'
start = time.strftime(fmt)

result, i = genetic_algorithm()

time.ctime()
end = time.strftime(fmt)
print("Time taken(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))

print('Iterations Taken: ', i)
print('Fitness of final configuration:', result.fitness)
print(len(result.chromosome) == len(set(result.chromosome)))

x, y = [], []
for i in range(problem_length):
    x.append(coordinates[result.chromosome[i]][0])
    y.append(coordinates[result.chromosome[i]][1])
plt.plot(x, y, marker='o')
plt.show()