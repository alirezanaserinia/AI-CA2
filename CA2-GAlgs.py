import math
import random

# TODO assign numbers to variables below
crossoverProbability = 0.8
exchangeProbability = 0.5
mutationProbability = 0.04
carryPercentage = 0.2
populationSize = 1000


class EquationBuilder:
    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber

        # Create the earliest population at the beginning
        self.population = self.makeFirstPopulation()
        self.fitnesses = []

    def makeFirstPopulation(self):
        # TODO create random chromosomes to build the early population, and return it
        firstPopulation = []
        for i in range(populationSize):
            chromosome = []
            for j in range(equationLength//2):
                chromosome.append(random.choice(self.operands))
                chromosome.append(random.choice(self.operators))
            chromosome.append(random.choice(self.operands))
            firstPopulation.append(chromosome)
        return firstPopulation

    def findEquation(self):
        generationNumber = 0
        # Create a new generation of chromosomes, and make it better in every iteration
        while True:
            random.shuffle(self.population)
            self.fitnesses = []
            for i in range(populationSize):
                # TODO calculate the fitness of each chromosome
                fitness = self.calcFitness(self.population[i])
                if fitness == 0:
                    return self.population[i]
                else:
                    self.fitnesses.append(fitness)
                # TODO return chromosome if a solution is found, else save the fitness in an array

            bestChromosomesIndices = sorted(range(len(self.fitnesses)), key=lambda sub: self.fitnesses[sub])[:int(populationSize*carryPercentage)]
            # TODO find the best chromosomes based on their fitnesses, and carry them directly to the next generation
            #  (optional)
            carriedChromosomes = []
            for index in bestChromosomesIndices:
                carriedChromosomes.append(self.population[index])

            # A pool consisting of potential candidates for mating (crossover and mutation)
            matingPool = self.createMatingPool()

            # The pool consisting of chromosomes after crossover
            crossoverPool = self.createCrossoverPool(matingPool)

            # print("Generation", generationNumber, ": Min Fitness :", min(self.fitnesses))

            # Delete the previous population
            self.population.clear()

            # Create the portion of population that is undergone crossover and mutation
            for i in range(populationSize - int(populationSize*carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))

            # Add the prominent chromosomes directly to next generation
            self.population.extend(carriedChromosomes)
            generationNumber += 1

    def createMatingPool(self):
        # TODO make a brand new custom pool to accentuate prominent chromosomes (optional)
        # TODO create the matingPool using custom pool created in the last step and return it
        matingPool = []
        while len(matingPool) != populationSize:
            index = self.selection()
            matingPool.append(self.population[index][:])
        return matingPool

    def selection(self):
        bestIndex = -math.inf
        for i in range(15):
            randIndex = random.randint(0, populationSize - 1)
            if bestIndex == -math.inf or self.fitnesses[bestIndex] > self.fitnesses[randIndex]:
                bestIndex = randIndex
        return bestIndex

    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        for i in range(0, len(matingPool), 2):
            if random.random() > crossoverProbability:
                # TODO don't perform crossover and add the chromosomes to the next generation directly to crossoverPool
                crossoverPool.append(matingPool[i])
                crossoverPool.append(matingPool[i + 1])
            else:
                # TODO find 2 child chromosomes, crossover, and add the result to crossoverPool
                child1, child2 = self.crossover(matingPool[i], matingPool[i + 1])
                crossoverPool.append(child1)
                crossoverPool.append(child2)
        return crossoverPool

    def crossover(self, chromosome1, chromosome2):
        for i in range(self.equationLength):
            if random.random() < exchangeProbability:
                chromosome1[i], chromosome2[i] = chromosome2[i], chromosome1[i]

        return chromosome1, chromosome2

    def mutate(self, chromosome):
        # TODO mutate the input chromosome
        for i in range(len(chromosome)):
            if random.random() < mutationProbability:
                point1 = random.randint(0, len(chromosome) - 3)
                if point1 % 2 == 0:
                    point2 = 1
                    while point2 % 2 != 0:
                        point2 = random.randint(point1 + 1, len(chromosome) - 1)
                    chromosome[point1], chromosome[point2] = chromosome[point2], chromosome[point1]
                else:
                    point2 = 0
                    while point2 % 2 != 1:
                        point2 = random.randint(point1 + 1, len(chromosome) - 1)
                    chromosome[point1], chromosome[point2] = chromosome[point2], chromosome[point1]
        return chromosome

    def calcFitness(self, chromosome):
        # TODO define the fitness measure here
        oprnds = []
        oprtors = []
        for i in range(0, len(chromosome) - 1, 2):
            oprnds.append(chromosome[i])
            oprtors.append(chromosome[i + 1])
        oprnds.append(chromosome[-1])
        while len(oprtors) > 0:
            while '*' in oprtors:
                oprtorIndex = oprtors.index('*')
                firstOprndIndex = oprtorIndex
                secondOprndIndex = oprtorIndex + 1
                oprnds[firstOprndIndex] = oprnds[firstOprndIndex] * oprnds[secondOprndIndex]
                del oprnds[secondOprndIndex]
                del oprtors[oprtorIndex]
            while '%' in oprtors:
                oprtorIndex = oprtors.index('%')
                firstOprndIndex = oprtorIndex
                secondOprndIndex = oprtorIndex + 1
                oprnds[firstOprndIndex] = oprnds[firstOprndIndex] % oprnds[secondOprndIndex]
                del oprnds[secondOprndIndex]
                del oprtors[oprtorIndex]
            while '-' in oprtors:
                oprtorIndex = oprtors.index('-')
                firstOprndIndex = oprtorIndex
                secondOprndIndex = oprtorIndex + 1
                oprnds[firstOprndIndex] = oprnds[firstOprndIndex] - oprnds[secondOprndIndex]
                del oprnds[secondOprndIndex]
                del oprtors[oprtorIndex]
            while '+' in oprtors:
                oprtorIndex = oprtors.index('+')
                firstOprndIndex = oprtorIndex
                secondOprndIndex = oprtorIndex + 1
                oprnds[firstOprndIndex] = oprnds[firstOprndIndex] + oprnds[secondOprndIndex]
                del oprnds[secondOprndIndex]
                del oprtors[oprtorIndex]

        return abs(self.goalNumber - oprnds[0])


def EquationString(equationList):
    equationStr = ""
    for i in range(len(equationList)):
        equationStr += str(equationList[i])
    return equationStr


operands = [1, 2, 3, 4, 5, 6, 7, 8]
operators = ['+', '-', '*']
equationLength = 21
goalNumber = 18019

equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)
equation = equationBuilder.findEquation()
print(EquationString(equation))
# print(eval(EquationString(equation)))
