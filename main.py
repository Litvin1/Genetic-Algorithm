# Vadin Litvinov - 314552365
# Shiran Ben-Meir- 311308035

import itertools
import random
import numpy as np
from random import randint

MUTATION_RATE = 0.03
GENERATIONS = 50

'''
The mutation method creates a solution with random mutations.
The method choose a random location out of the blank cells locations and replace the value 
in the chosen location with a random number in range 1-9.

@:param fit: a fitted solution (one of the solution that has survived).
@:param zeroPlacesList: a list that contains the indexes of the number 0 at the input soduku.
@:return fit - the solution with mutations 
'''
def mutation(fit, zeroPlacesList):
    for i in range(0, round(81 * MUTATION_RATE)):
        randZeroLocaton = random.choice(zeroPlacesList)  # choose random location out of the blank cells
        row = randZeroLocaton[0]
        column = randZeroLocaton[1]
        fit[row][column] = random.randint(1, 9)    # replace the value at the random location with random num
    return fit


'''
The crossover method creates an offspring solution from 2 solutions.
The method choose a random number of crossovers and random rows to swap between 
the 2 solutions.

@:param detail1: one solution
@:param detail2: second solution
@:return offspring
'''
def crossover(detail1, detail2):
    listOfRows=[]
    rowsToSwitch = random.randint(0, 8)      # choose number of crossovers
    offspring = detail1.copy()              # creating initial offspring contains detail1's genes only
    for x in range(0, rowsToSwitch):
        offspring[x] = detail2[x]      # swap
    return offspring


'''
The fitness method gives a fitness score to a solution.
The method uses row_check, col_check and square_checks methods.

@:param detail: one solution
@:return fitness score.
'''
def fitness(detail):
    rowDup = 0
    columnDup = 0
    squareDup = 0
    for i in range(0, len(detail)-1):
        rowDup = rowDup + row_check(detail, i)        # sum number of replications in rows
    for j in range(0, len(detail[0])-1):
        columnDup = columnDup + col_check(detail, j)    # sum number of replications in columns
    for k in range(0, 6, +3):
        for m in range(0, 6, +3):
            squareDup = squareDup + square_check(detail, k, m)   # sum number of replications in squares
    fitness = 243 - (squareDup + rowDup + columnDup)         # creating fitness function
    return fitness


'''
The optimization method returns an improves solution.
The method checks for replacement for every index and if the optional replacement
increases the fitness function- the replacement will occur.

@:param detail: one solution
@:param zeroPlacesList: a list contains the 0 indexes
@:param type: type of policy
@:return detail.
'''
def optimization(detail, zeroPlacesList, type):
    dtlCpy = detail.copy()
    maxScore = -7
    max = detail[0][0]
    rowIndx = 0
    colIndx = 0
    # the main loop that iterates over the cells, checks if its a legal cell to optimizde
    # checks the score of the current value in the cell, and then if what is the best way
    # to change the value of the cell to get a higher score.
    for i in range(0,9):
        for j in range(0,9):
            if i % 3 == 0 and j % 3 == 0:
                square = dtlCpy[i:i+3, j:j+3]
                square = list(np.array(square).ravel())
            if [i,j] in zeroPlacesList:
                r = zeroPlacesList[i][0]
                c = zeroPlacesList[i][1]
                curScore=0
                row = list(dtlCpy[r])
                if row.count(row[j]) > 1:
                    curScore -= 1
                col = list(dtlCpy[0:9, j])
                if col.count(dtlCpy[i][j]) > 1:
                    curScore -= 1
                if square.count(dtlCpy[i][j]) > 1:
                    curScore -= 1
                for k in range(1, 9):
                    repScore = 0
                    if row.count(k)>0:
                        repScore -= 1
                    if col.count(k)>0:
                        repScore -= 1
                    if square.count(k)>0:
                        repScore -= 1
                    if (repScore - curScore) > maxScore and repScore - curScore > 0:
                        maxScore = repScore - curScore
                        max = k
                        rowIndx = i
                        colIndx = j
    dtlCpy[rowIndx][colIndx] = max
    if type == 2:
        return fitness(dtlCpy)
    if type == 3:
        detail = dtlCpy.copy()
        return detail


'''
The square_check method returns the number of replications of numbers in a square.

@:param sudokuInput
@:param  rowNum: number of the row we want to check.
@:param colNum: number of the column we want to check.
@:return counter- number of replications in a square.
'''
def square_check(sudokuInput, rowNum, colNum):
    counter=0
    # definding a square:
    if (rowNum <=3 and colNum <=3): topEdge= 0 ; bottomEdge=3 ; leftEdge=0 ; rightEdge=3
    if (rowNum<=3 and 3< colNum<=6): topEdge= 0 ; bottomEdge=3 ; leftEdge=3 ; rightEdge=6
    if (rowNum<=3 and 6< colNum): topEdge= 0 ; bottomEdge=3 ; leftEdge=6 ; rightEdge=9
    if (3< rowNum<= 6 and colNum <=3): topEdge= 3 ; bottomEdge=6 ; leftEdge=0 ; rightEdge=3
    if (3< rowNum<= 6 and 3< colNum<=6): topEdge= 3 ; bottomEdge=6 ; leftEdge=3 ; rightEdge=6
    if (3< rowNum<= 6 and 6< colNum): topEdge= 3 ; bottomEdge=6 ; leftEdge=6 ; rightEdge=9
    if (6< rowNum and colNum <=3): topEdge= 6 ; bottomEdge=9 ; leftEdge=0 ; rightEdge=3
    if (6< rowNum and 3< colNum<=6): topEdge= 6 ; bottomEdge=9 ; leftEdge=3 ; rightEdge=6
    if (6< rowNum and 6< colNum): topEdge= 6 ; bottomEdge=9 ; leftEdge=6 ; rightEdge=9
    box = [l[leftEdge:rightEdge] for l in sudokuInput[topEdge:bottomEdge]]
    chainedBox = (list(itertools.chain.from_iterable(box)))

    for k in range(1, len(chainedBox)+1):    # fonding replications
        if chainedBox.count(k) > 1:
            counter +=chainedBox.count(k)
    return counter


'''
The col_check method returns the number of replications of numbers in a column.

@:param sudokuInput
@:param colNum: number of the row we want to check.
@:return counter- number of replications in a row.
'''
def col_check(sudokuInput, colNum):
    counter = 0
    columnLst = []
    for i in sudokuInput:
        columnLst.append(i[colNum])
    for y in range (1, len(columnLst)+1):
        if columnLst.count(y) > 1:
            counter += columnLst.count(y)
    return counter


'''
The row_check method returns the number of replications of numbers in a row.

@:param sudokuInput
@:param  rowNum: number of the column we want to check.
@:return counter- number of replications in a row.
'''
def row_check(sudokuInput, rowNum):
    counter = 0
    for i in range(1, len(sudokuInput[rowNum]) + 1):
        if list(sudokuInput[rowNum]).count(i) > 1:
            counter += list(sudokuInput[rowNum]).count(i)
    return counter


'''
The population_generator method returns the population (which doesn't contain 0 number)

@:param sudokuInput
@:return population
'''
def population_generator(sudokuInput):
    matricesList = []*100
    for i in range(0, 100):              # creates population of 100 solutions
        tempMat = np.array(sudokuInput)
        for j in range(0, 9):
            for k in range(0, 9):
                if tempMat[j][k] == 0:   # insert random number instead of zero in  sudoku_input.
                    tempMat[j][k] = randint(1, 9)
        matricesList.append(tempMat)
    return matricesList


'''
The get_zeros method returns a list that holds the indexes of number 0 in sudoku_input

@:param sudoku
@:return zeroPlacesList
'''
def get_zeros(sudoku):
    zeroPlacesList = [] * 81
    tempMat = np.array(sudoku)
    for j in range(0, 9):
        for k in range(0, 9):
            if tempMat[j][k] == 0:    # if the value of the cell is 0- insert the index to the list zeroPlacesList.
                zeroPlacesList.append([j, k])
    return zeroPlacesList


'''
The run_evolution method runs the improvment evolution of the solutions until it finds a solution, or until the generation
number reaches GENERATION constant.

@:param sudokuInput
@:param type: type of policy
@:return zeroPlacesList
'''
def run_evolution(sudokuInput, type):
    callsNum = 0
    #the array of the fittest each generation.
    fit = []
    nextGen = []
    #the counter for premature convergence. if it reaches a certain value, it will seed partially new population.
    conv = 0
    #generations counter.
    generations = 0
    #the legal cells to change. the empty/zero cells in the input
    zeroPlacesList = get_zeros(sudokuInput)
    #creates fully random new population of solutions.
    population = population_generator(sudokuInput)
    #p = 0
    while generations < GENERATIONS:
        bestIndx = 0
        totalFitness = 0
        previousBest = 0
        for i in range(0, len(population)):
            if fitness(population[i]) >= fitness(population[bestIndx]):
                bestIndx = i
            totalFitness = totalFitness + fitness(population[i])
            rand = random.randint(0, 243)
            if fitness(population[i]) == 243:
                print(fitness(population[i]))
                print(population)
                return
                break
            print(type)
            if type == 1:
                p = fitness(population[i])
                print("in")
            if type == 2:
                p = optimization(population[i], zeroPlacesList, type)
            if type == 3:
                population[i] = optimization(population[i], zeroPlacesList, type)
                p = fitness(population[i])
            if rand <= p:
                fit.append(population[i])
        if fitness(population[previousBest]) == fitness(population[bestIndx]):
            conv += 1
        if conv == 12:
            for j in range(0, 10):
                nextGen.append(population[bestIndx])
            newPopul = population_generator(sudokuInput)
            newPopul.sort(reverse=True, key=fitness)
            for i in range(0, 90):
                nextGen.append(newPopul[i])
            conv = 0
        else:
            previousBest = bestIndx
            fit.sort(reverse=True, key=fitness)
            for j in range(0, round(len(population) * 0.3)):
                nextGen.append(fit[0])
            for i in range(round(len(fit) * 0.3), len(fit) - 1):
                nextGen.append(crossover(fit[random.randint(i, len(fit) - 1)],
                                          fit[i + 1]))
                nextGen.append(mutation(crossover(fit[random.randint(0, len(fit) - 1)], fit[i]),
                                         zeroPlacesList))
                nextGen.append(fit[i])
                if len(nextGen) >= 100:
                    break
            population = nextGen
            nextGen = []
            fit = []
            generations += 1
            print(generations)
    #Printing the best solution the algorithm has come to
    print(population[bestIndx])
    #Printing the number of calls the to fitness function
    if type == 1:
        print("Number of calls to the fitness evaluation function: ", generations * len(population))
    if type == 2 or type == 3:
        print("Number of calls to the fitness evaluation function and to the optimization function: ",
              (generations * len(population) * 2))


'''
main.
'''
def main():
    sudokuInput = []
    print("Please enter a sudoku table (Press enter after every row): ")
    for x in range(0, 9):
        a = list(map(int, input("").strip().split()))[:9]
        if len(a) != 9:
            print("You entered more or less than 9 numbers in a row. Please try again")
            break
        for counter, value in enumerate(a):
            if (value > 9) or (value < 0):
                print("You entered an out of range number. Please try again")
                return
        sudokuInput.append(a)

    type = input("please enter 1 for regular genetic algorithm" "\n"
                 "2 for partially Lamarck algorithem" "\n"
                 "3 for full Lamarck algorithm""\n")

    run_evolution(sudokuInput, type)


main()
