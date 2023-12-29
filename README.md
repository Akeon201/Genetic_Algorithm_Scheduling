# Scheduling with a Genetic Algorithm
#### Author: Kenyon Leblanc, Wesley Bafile, David Wolfe
In our project, we utilized our genetic algorithm to optimize class scheduling based on data from an Excel (.xlsx) file. This file contained details about available classes, available times, classroom allocations, and professor preferences. The genetic algorithm was designed to mimic human genetic processes in reproduction. A key feature was the crossover rate, where two 'parent' data sets combined to produce a 'child' dataset. This incorporate elements from both parents. Another critical aspect was the mutation rate, which randomly altered a value in the dataset to another valid option, introducing variability and potential improvements in the scheduling. We additionally implemented an injection rate, which is analogous to random death in natural selection. This process randomly replaces existing hypotheses (scheduling plans) with entirely new ones, not derived from any existing 'parent' plans. This approach allowed for the introduction of fresh, potentially advantageous scheduling options into the algorithm the existing hypotheses. It greatly enhances the diversity and robustness of our scheduling solutions. The combination of these elements in our genetic algorithm aimed to efficiently and effectively optimize class scheduling, balancing various constraints and preferences.

## Requirements

Packages: numpy, openpyxl, pandas

Make a virtual environment

    python -m venv myenv
    
Activate virtual environment on windows:
    
    myenv\Scripts\activate

Activate virtual environment on linux:

    source myenv/bin/activate

Install packages

    pip install numpy openpyxl pandas

## Configurations

You can change variables between lines 195 and 206 (bottom of file) in main.py for different outcomes.

Example of variable configuration:

    ########################################################################    
    # Number of hypotheses you want in every generation
    num_hypotheses = 100
    # proportion of teachers that will undergo crossover
    cross_rate = 0.45
    # probability of mutation per teacher
    mutate_rate = .3
    # probability of injecting a random hypothesis
    injection_rate = 0.025
     # The number of generations it takes to stop running and return the best hypothesis
    plateau_generations = 10
    #################################################################################

### Note

Decimal values are treated as percentages.

## Directions

    Make sure you are in the directory of "main.py". Start the program by typing "python main.py" or "python3 main.py".

    It may take a bit of time to generate initial hypotheses. If it is taking too long then decrease the num_hypotheses variable.

    After initializing all hypotheses, the console will display the generation and fitness score, as well as best generation and best fitness score.

    
