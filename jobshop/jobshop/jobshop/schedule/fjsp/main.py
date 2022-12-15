#!/usr/bin/env python

# This script contains a high level overview of the proposed hybrid algorithm
# The code is strictly mirroring the section 4.1 of the attached paper

import sys
import time

from .src.utils import parser, gantt
from .src.genetic import encoding, decoding, genetic, termination
from .src import config


# Beginning
def FJSPStart():
    # Parameters Setting
    parameters = parser.parse('./schedule/fjsp/test_data/fjsp_data.txt')

    t0 = time.time()

    # Initialize the Population
    population = encoding.initializePopulation(parameters)
    gen = 1

    # Evaluate the population
    while not termination.shouldTerminate(population, gen):
        # Genetic Operators
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        gen = gen + 1

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()
    total_time = t1 - t0


    # Termination Criteria Satisfied ?
    gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))
    gantt.draw_chart(gantt_data)

    if config.latex_export:
        gantt.export_latex(gantt_data)
    else:
        gantt.draw_chart(gantt_data)

    return "success"
