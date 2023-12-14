import satisfaction
import numpy as np
import timeslots
import random
import math
import os


# See if a hypothesis has any values that defy constraints
def validate_hypothesis(hypothesis):
  for row_num in range(29):
    if row_num == 0:
      continue
    if (timeslots.get_course_credits(row_num - 1) !=
        timeslots.get_credit_hours(hypothesis[row_num][2])):
      # Credit hours
      return False
    for x in range(29):
      if row_num == x:
        break
      if timeslots.timeconflict(hypothesis[row_num][2], hypothesis[x][2]):
        if hypothesis[x][0] == hypothesis[row_num][0]:
          return False
        if hypothesis[x][1] == hypothesis[row_num][1]:
          return False

  # Make sure that all teachers have at least their minimum amount of classes
  for teacher in range(1, 11):
    class_count = 0
    for c in range(29):
      if hypothesis[c][0] == teacher:
        class_count += 1
    if class_count < satisfaction.get_min_sections(teacher):
      return False
    if class_count > satisfaction.get_max_sections(teacher):
      return False
  return True

# validates a hypothesis from a given line to the beginning
def check_row(hypothesis, row):
  if row == 0:
    return True

  current_prof = hypothesis[row][0]
  current_room = hypothesis[row][1]
  current_time = hypothesis[row][2]

  if (timeslots.get_course_credits(row - 1) !=
      timeslots.get_credit_hours(current_time)):
    # Credit hours
    return False

  class_count = 0
  while (row > 0):
    row -= 1
    if timeslots.timeconflict(current_time, hypothesis[row][2]):
      if hypothesis[row][0] == current_prof:
        #timeconflict with teacher
        return False
      if hypothesis[row][1] == current_room:
        #timeconflict with room
        return False
    elif current_prof == hypothesis[row][0]:
      # Max courses
      class_count += 1
      if class_count > satisfaction.get_max_sections(current_prof):
        return False

  return True


# Generate hypothesis for 1 schedule
def generate_hypothesis():
  # Initialize an empty hypothesis array
  hypothesis = np.zeros((29, 3), dtype=int)

  row = 0
  while row < 29:
    # Randomly select values for each column
    hypothesis[row, 0] = np.random.randint(1, 11)
    hypothesis[row, 1] = np.random.randint(1, 12)
    hypothesis[row, 2] = np.random.randint(1, 87)

    # Verify the hypothesis
    if check_row(hypothesis, row):
      row += 1  # Only increment row if validation passes

  # validate at the end, if false regenerate whole schedule
  if validate_hypothesis(hypothesis):
    return hypothesis
  else:
    return generate_hypothesis()


# Generate hypotheses for all schedules. Use generate_hypothesis() for each schedule.
def initialize_hypotheses(number_hypotheses):
  # Empty list
  hypotheses = []

  # Generate hypotheses
  for _ in range(number_hypotheses):
    hypothesis = generate_hypothesis()
    hypotheses.append(hypothesis)

  return hypotheses


# Heuristic function, set a value in teacher slot ([teacher id][-1]) or return value.
def fitness_check(hypothesis):
  score = 0

  for i in range(len(hypothesis)):
    row = 0
    # Board
    if satisfaction.get_board_type(
        hypothesis[i][1]) == satisfaction.get_board_pref(hypothesis[i][0]):
      score += 7
      row += 7
    elif satisfaction.get_board_pref(hypothesis[i][0]) == 0:
      score += 5
      row += 5
    else:
      score += 3
      row += 3

    # ToD
    if timeslots.get_time_of_day(
        hypothesis[i][2]) == satisfaction.get_time_pref(hypothesis[i][0]):
      score += 7
      row += 7
    elif satisfaction.get_time_pref(hypothesis[i][0]) == 0:
      score += 5
      row += 5
    else:
      score += 3
      row += 3

    # get
    if satisfaction.get_day_pref(
        hypothesis[i][0]) == timeslots.get_days_of_week(hypothesis[i][2]):
      score += 7
      row += 7
    elif satisfaction.get_day_pref(hypothesis[i][0]) == 0:
      score += 5
      row += 5
    else:
      score += 3
      row += 3

    score += (abs(satisfaction.get_satisfaction(hypothesis[i][0], i + 1) - 5) +
              1) * 2
    row += (abs(satisfaction.get_satisfaction(hypothesis[i][0], i + 1) - 5) +
            1) * 2

  return score


# mutate a hypothesis
def mutate_hypothesis(hypothesis, point1, point2):
  copy_hypothesis = np.copy(hypothesis)
  i = 0
  # Randomly select values for each column
  while check_row(hypothesis, point1) and i < 1000:
    if point2 == 0:
      temp = np.random.randint(1, 11)
      while temp == hypothesis[point1][0]:
        temp = np.random.randint(1, 11)
      copy_hypothesis[point1][0] = temp
    elif point2 == 1:
      temp = np.random.randint(1, 12)
      while temp == hypothesis[point1][1]:
        temp = np.random.randint(1, 12)
      copy_hypothesis[point1][1] = temp
    elif point2 == 2:
      temp = np.random.randint(1, 87)
      while temp == hypothesis[point1][2]:
        temp = np.random.randint(1, 87)
      copy_hypothesis[point1][2] = temp
    i += 1

  # Validate at the end, if false regenerate whole schedule
  if validate_hypothesis(copy_hypothesis):
    return copy_hypothesis
  else:
    return mutate_hypothesis(hypothesis, np.random.randint(0, 29),
                             np.random.randint(0, 3))


# mutate hypotheses using mutate_hypothesis() on chance
def mutate_hypotheses(hypotheses, mutate_rate):
  for i in range(len(hypotheses)):
    if np.random.rand() <= mutate_rate:
      for _ in range(np.random.randint(5,11)):
        point1 = np.random.randint(0,
                                 29)  # Random point between 0 and 28 inclusive
        point2 = np.random.randint(0,
                                 3)  # Random point between 0 and 2 inclusive
        hypotheses[i] = mutate_hypothesis(hypotheses[i], point1, point2)

  return hypotheses


# perform a crossover between 2 parents
def cross_hypothesis(parent1, parent2):
  test = False
  for _ in range(5000):
    sections = np.random.randint(10, 20)  # To include 29 in the range
    cross_points = []  # Initialize an empty list

    for _ in range(sections):
      point1 = np.random.randint(0,
                                 29)  # Random point between 0 and 28 inclusive
      point2 = np.random.randint(0,
                                 3)  # Random point between 0 and 2 inclusive
      cross_points.append([point1, point2])  # Append the pair as a sublist

    cross_parent = np.copy(parent1)

    # Perform crossover
    for point in cross_points:
      cross_parent[point[0]][point[1]] = parent2[point[0]][point[1]]

    # Check hypothesis
    if validate_hypothesis(cross_parent):
      test = True
      break

  return cross_parent, test


# Perform crossovers. Fill remaining hypotheses
# need teacher_num because selection should only keep elite hypotheses. Need to fill rest
def cross_hypotheses(hypotheses, cross_rate, num_hypotheses, timeout_seconds=5):
  needed_pop_size = math.ceil((1 - cross_rate) * num_hypotheses)
  sampling = len(hypotheses)
  size = 0

  while size < needed_pop_size:
    p1, p2 = random.sample(range(sampling), 2)

    result, test = cross_hypothesis(hypotheses[p1], hypotheses[p2])
    if test:
      hypotheses.append(result)
      #print ("cross_hypothesis, appended")
      size += 1
    #else:
      #print("cross_hypothesis timed out, trying different parents")
      # You can handle the timeout here, e.g., by trying different parents

  return hypotheses


# Select top valued hypotheses. These will 'survive' and may undergo crossover in next gen.
def elite_selection(hypotheses, cross_rate, num_hypotheses):
  remaining_pop_size = math.floor(cross_rate * num_hypotheses)
  fitness_scores = [fitness_check(hypothesis) for hypothesis in hypotheses]

  combined = zip(fitness_scores, hypotheses)
  sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)  # Sorting by fitness score, highest first

  sorted_fitness, sorted_hypotheses = zip(*sorted_combined)
  trimmed_hypotheses = list(sorted_hypotheses)[:remaining_pop_size]

  return trimmed_hypotheses


def get_next_filename(base_name="Generation", extension=".csv"):
    i = 1
    while os.path.exists(f"{base_name}{i}{extension}"):
        i += 1
    return f"{base_name}{i}{extension}"


# Random chance to injection fully random hypothesis
def injection(hypotheses, injection_rate):
  for i in range(len(hypotheses)):
    if np.random.rand() <= injection_rate:
      hypotheses[i] = generate_hypothesis()
  return hypotheses

# main function to run.
# fitness_cap - when heuristic value is high enough - ???
# cross_rate - proportion of teachers that will undergo crossover - .25
# mutate_rate - probability of mutation per teacher - .025 or .05
# teacher_num - how many teachers are there - 10
def genetic_algorithm(num_hypotheses, cross_rate, mutate_rate, injection_rate, plateau_generations):
  print(f"Initializing {num_hypotheses} hypotheses ...")
  hypotheses = initialize_hypotheses(num_hypotheses)
  generation = 1
  best = 0
  gen_num = 0
  best_hypothesis = hypotheses[0]
  # Repeat below until threshold met

  filename = get_next_filename()

  # Now, you can write to the file
  with open(filename, "a") as myfile:
    # Write your data here
    myfile.write(f"num_hypotheses,cross_rate,mutate_rate,injection_rate\n")
    myfile.write(f"{num_hypotheses},{cross_rate},{mutate_rate},{injection_rate}\n")
    myfile.write("\n")
    myfile.write(f"Generation,Fitness,Best Generation,Best fitness\n")

  while True:
    #print("sort")
    hypotheses = elite_selection(hypotheses, 1, num_hypotheses)

    fitness = fitness_check(hypotheses[0])
    if fitness > best:
      best = fitness
      gen_num = generation
      best_hypothesis = hypotheses[0]
    print(f"Generation: {generation} | Fitness: {fitness} | Best Generation: {gen_num} | Best fitness: {best}")

    #print("elite_selection")
    hypotheses = elite_selection(hypotheses, cross_rate, num_hypotheses)
    hypotheses = injection(hypotheses, injection_rate)
    #print("cross_hypotheses")
    hypotheses = cross_hypotheses(hypotheses, cross_rate, num_hypotheses)
    #print("mutate_hypotheses")
    hypotheses = mutate_hypotheses(hypotheses, mutate_rate)

    # Now, you can write to the file
    with open(filename, "a") as myfile:
      # Write your data here
      myfile.write(f"{generation},{fitness},{gen_num},{best}\n")

    generation += 1

    if generation - gen_num > plateau_generations:
      break

  return best_hypothesis
