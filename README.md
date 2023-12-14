# Scheduling with a Genetic Algorithm
#### Author: Kenyon Leblanc, Wesley Bafile, David Wolfe
This project is an implementation of a genetic algorithm to simulated data with contraints and teachers with preferences. 

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

You can change variables between lines 195 and 204 in main.py for different outcomes.

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
    #################################################################################

### Note

Decimal values are treated as percentages.

## Directions

    Make sure you are in the directory of "main.py". Start the program by typing "python main.py" or "python3 main.py".

    It may take a bit of time to generate initial hypotheses. If it is taking too long then decrease the num_hypotheses variable.

    
