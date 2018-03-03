#
# Genetic Algorithm
#
import string
import random
import math
import operator
import matplotlib.pyplot as plt

TARGET = 'to be or not to be'

class GeneticAlgorithm:
    '''GeneticAlgorithm'''
    def __init__(self, population_size):
        self.population = []
        for _ in range(population_size):
            self.population.append(Creature())
    
    def print(self):
        print('Population :')
        for i in range(len(self.population)):
            print(self.population[i])
    
    def evolve(self):
        new_population = []
        for _ in range(len(self.population)):
            parent_a = self.get_creature()
            parent_b = self.get_creature()
            new_population.append(Creature(parent_a, parent_b))
        self.population = new_population

    def get_creature(self, bestone = False):
        if(bestone):
            pass
            return sorted(self.population, reverse=True)[0]
        else:
            items_w = [x.fitness for x in self.population]
            return random.choices(self.population, weights = items_w).pop()

    def get_fitness(self):
        return sum([x.fitness for x in self.population]) / len(self.population)

class Creature:
    '''Creature'''
    mutation_rate = 0.01
    #mutation_count = 0
    def __init__(self, parent_a = None, parent_b = None):
        self.fitness = 0
        self.dna = ''
        if((parent_a is None) or (parent_b is None)):
            self.dna = ''.join([self._random_gene() for n in range(len(TARGET))])
        else:
            self._mix_and_mutate(parent_a, parent_b)
        self._update_fitness()

    def __str__(self):
        return 'Creature[%.4f, %s]' % (self.fitness, self.dna)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def _random_gene(self):
        return random.choice(string.ascii_lowercase + ' ')

    def _update_fitness(self):
        score = 0
        tlen = len(TARGET)
        for i in range(tlen):
            if(TARGET[i] == self.dna[i]):
                score += 1
        self.fitness = pow(score/tlen, 2)

    def _mix_and_mutate(self, parent_a, parent_b):
        split = math.floor(random.random() * len(self.dna))
        self.dna = parent_a.dna[0:split] + parent_b.dna[split:len(parent_b.dna)]

        if(random.random() < Creature.mutation_rate):
            new_dna = list(self.dna)
            new_dna[math.floor(random.random() * len(self.dna))] = self._random_gene()
            self.dna = ''.join(new_dna)
            #type(self).mutation_count +=1
            #print('***** Mutation has occured [%s] *****' % type(self).mutation_count)


if __name__ ==  '__main__':
    print('Main...')
    ga = GeneticAlgorithm(500)

    # ga.print()
    # print(ga.get_fitness())

    figure = plt.figure()
    plot = figure.add_subplot(1, 1, 1)
    plt.ion()
    plt.show()
    
    print('**********')
    for i in range(1000):
        ga.evolve()
        #print(ga.get_fitness())
        if(i % 10 == 0):
            print('Gen[%s] : %s' % (i, ga.get_creature(bestone = True)))
            plt.plot(i, ga.get_fitness(), 'r+')
            plt.pause(.001)
    # print(ga.get_creature())
    print('**********')
    ga.print()
