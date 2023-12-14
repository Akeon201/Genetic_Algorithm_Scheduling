# David, Ken, Wes
# Genetic Algorithm Project

# Hypothesis Representation
#
# Class = Teacher  Room  TIME
# Class =  1-10    1-11  1-86
# [29][4] - course numbers

# Constraints
#   Teacher with timeslots
#   Classrooms with timeslots
#   Min courses
#   Max courses
#   Credit hours

# Preferences
#   Board
#   Time of day
#   Days of week
#   Section number

import pandas as pd
import os
import genetic_algorithm
import timeslots
import numpy as np
import satisfaction
import sys

sys.setrecursionlimit(2147483647)


# Gets data from sheets in excel file
def load_file(file_name: str):
  sim_course_sections = pd.read_excel(
      file_name, sheet_name='(I) Simulated Course Sections').to_numpy()

  classrooms = pd.read_excel(file_name, sheet_name='(J) Classrooms').to_numpy()

  time_slots = pd.read_excel(file_name, sheet_name='(K) Time Slots').to_numpy()

  teacher_satisfaction = pd.read_excel(
      file_name, sheet_name='Teacher Satisfaction').to_numpy()

  return sim_course_sections, classrooms, time_slots, teacher_satisfaction


def check_valid_file(file_name):
  """
  Check if file provided by user input is valid.
  :param file_name: file name w/ extension
  :return: valid file name
  """
  # Current directory
  directory = os.getcwd()
  # List of files from cwd
  listed_directory = os.listdir(directory)
  # Continue loop until valid file name is given
  while file_name not in listed_directory:
    print("File not found, please try again.")
    file_name = input("Please enter file name with extension: ")

  return file_name


# Returns a list of days of the week corresponding to abbreviation in excel file
def get_day(string):
  if string == 'MW':
    return ["Monday", "Wednesday"]
  if string == 'MF':
    return ["Monday", "Friday"]
  if string == 'MWF':
    return ["Monday", "Wednesday", "Friday"]
  if string == 'TR':
    return ["Tuesday", "Thursday"]
  if string == 'WF':
    return ["Wednesday", "Friday"]


# Converts time from minute
def convert_from_min(time, ID):
  start = time[ID - 1][2]
  end = time[ID - 1][3]

  start_hour = start // 60
  start_min = start % 60
  end_hour = end // 60
  end_min = end % 60

  return f"{start_hour:02d}:{start_min:02d}-{end_hour:02d}:{end_min:02d}"


# Takes in a hypothesis/schedule and saves it to a csv file. Pass populate_schedule_dict() returned value as parameter
def save_data_to_csv(schedule):
  time_slots2 = timeslots.get_timeslot()
  with open("output.csv", "w") as output:
    output.write(f"Monday,Tuesday,Wednesday,Thursday,Friday\n")
    for i in range(max(len(schedule[day]) for day in schedule)):
      for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        if i < len(schedule[day]):
          output.write(f"Teacher: {schedule[day][i][0]},")
        else:
          output.write(",")
      output.write("\n")
      for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        if i < len(schedule[day]):
          output.write(f"Course: {schedule[day][i][3]},")
        else:
          output.write(",")
      output.write("\n")
      for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        if i < len(schedule[day]):
          output.write(f"Classroom: {schedule[day][i][1]},")
        else:
          output.write(",")
      output.write("\n")
      for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        if i < len(schedule[day]):
          output.write(
              f"Time: {convert_from_min(time_slots2, schedule[day][i][2])},")
        else:
          output.write(",")
      output.write("\n\n")


# Print a hypothesis converted to a schedule into the terminal. Pass populate_schedule_dict() returned value as parameter
def print_schedule(schedule):
  # Print the schedule
  time_slots2 = timeslots.get_timeslot()
  print(
      "Monday\t\t\t\t\t\tTuesday\t\t\t\t\t\tWednesday\t\t\t\t\tThursday\t\t\t\t\tFriday"
  )
  for i in range(max(len(schedule[day]) for day in schedule)):
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
      if i < len(schedule[day]):
        print(f"[Teacher: {schedule[day][i][0]}]", end='\t\t\t\t')
      else:
        print("", end='\t\t\t\t\t\t\t')
    print()
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
      if i < len(schedule[day]):
        print(f"[CRN: {timeslots.get_CRN(schedule[day][i][3])}]",
              end='\t\t\t\t\t')
      else:
        print("", end='\t\t\t\t\t\t\t')
    print()
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
      if i < len(schedule[day]):
        print(f"[Room: {schedule[day][i][1]}]", end='\t\t\t\t\t')
      else:
        print("", end='\t\t\t\t\t\t\t')
    print()
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
      if i < len(schedule[day]):
        print(f"[Time: {convert_from_min(time_slots2, schedule[day][i][2])}]",
              end='\t\t\t')
      else:
        print("", end='\t\t\t\t\t\t\t')
    print("\n")

# populates a dictionary and returns a schedule to be passed to print_schedule() and save_data_to_csv()
def populate_schedule_dict(hypothesis):
  time_slots2 = timeslots.get_timeslot()

  # Create a dictionary to hold the schedule for each day
  schedule = {
      'Monday': [],
      'Tuesday': [],
      'Wednesday': [],
      'Thursday': [],
      'Friday': []
  }

  # Populate the schedule dictionary
  section = 0
  for row in hypothesis:
    section += 1
    days_of_week = get_day(str(time_slots2[row[2] - 1][1]))
    row = np.append(row, [section])
    for day in days_of_week:
      schedule[day].append(row)

  return schedule


if __name__ == '__main__':
  # file_name = input("Please enter file name with extension: ")
  file_name = "Simulated Data.xlsx"
  file_name = check_valid_file(file_name)

  satisfaction.set_file(file_name)
  timeslots.set_file(file_name)

 #################################################################################
  # Number of hypotheses you want in every generation
  num_hypotheses = 50
  # proportion of teachers that will undergo crossover
  cross_rate = 0.25
  # probability of mutation per teacher - .025 or .05
  mutate_rate = .3
  # probability of injecting a random hypothesis
  injection_rate = 0.02
  #################################################################################

  best_hypothesis = genetic_algorithm.genetic_algorithm(
      num_hypotheses, cross_rate, mutate_rate, injection_rate)

  schedule = populate_schedule_dict(best_hypothesis)

  print_schedule(schedule)

  save_data_to_csv(schedule)
