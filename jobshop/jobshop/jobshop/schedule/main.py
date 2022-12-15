from .utils import readFilePairs
from .jspGA import genetic


filedir = 'schedule/'
def GAStart():
    target = None

    population_size=100 # int(input('Please input the size of population (default: 30): ') or 30)
    mutation_rate=0.2 # float(input('Please input the size of Mutation Rate (default 0.2): ') or 0.2)
    iterations=100 # int(input('Please input number of iteration (default 2000): ') or 2000)

    times, machines, n, mn = readFilePairs(filedir + "cases/scheduling_set.txt")
    result = genetic(times, machines, n, mn, population_size, iterations, mutation_rate, target)

    return result