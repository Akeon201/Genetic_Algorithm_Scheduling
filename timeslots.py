import pandas as pd
import numpy as np
import math
import re
import os

global course, time_slots, conflict_list


# Sets global variables for the scope of this file
def set_file(file_name):
  global course, time_slots, conflict_list
  course = pd.read_excel(
      file_name, sheet_name='(I) Simulated Course Sections').to_numpy()
  time_slots = pd.read_excel(file_name, sheet_name='(K) Time Slots').to_numpy()
  format_time()
  conflict_list = generate_conflict_lists()


# Split each time slot string to a list
# Expected elements is what the length of the list is expected to be (to handle hyphens)
def split_string(string, expected_elements):
  str_list = string.split(" ")
  if len(str_list) == expected_elements:
    return str_list
  else:
    result = list()
    for i in range(len(str_list)):
      if "-" not in str_list[i]:
        result.append(str_list[i])
      else:
        result.extend(str_list[i].split("-"))
        result.insert(-1, "-")
    return result


# Add missing "am" or "pm" labels
def add_am_pm():
  for col in range(len(time_slots)):
    slot_list = split_string(time_slots[col][1], 4)
    # If the first time slot is missing something
    if "am" not in slot_list[1] and "pm" not in slot_list[1]:
      # If end time is in the morning
      if "am" in slot_list[3]:
        slot_list[1] += "am"
      # If end time is in the afternoon/evening
      if "pm" in slot_list[3]:
        first_time = slot_list[1]
        # If time includes a ":", only look at hours
        if ":" in first_time:
          first_time = first_time.split(":")[0]
        # Validate that classes between 9 and 12 are in the morning, not night
        if int(first_time) > 9 and int(first_time) < 12:
          slot_list[1] += "am"
        else:
          slot_list[1] += "pm"
      # If neither time slot has an "am" or "pm"
      if "am" not in slot_list[3] and "pm" not in slot_list[3]:
        slot_list[1] += "pm"
        slot_list[3] += "pm"
    # Save new time slot to original list
    time_slots[col][1] = " ".join(slot_list)
  return time_slots


# Function to convert time slots to minutes
def convert_to_minutes(slot):
  days, time_range = slot[1].split(' ', 1)

  # Parse time ranges
  start_time, end_time = map(lambda x: x.strip(), time_range.split('-'))

  # Convert times to 24-hour format
  start_time = time12_to_24(start_time)
  end_time = time12_to_24(end_time)

  # Convert times to minutes for easier comparison
  start_time_components = [
      int(comp) for comp in re.findall(r'\d+', start_time)
  ]
  end_time_components = [int(comp) for comp in re.findall(r'\d+', end_time)]

  # Check if only the hour is provided without minutes
  if len(start_time_components) == 1:
    start_time_components.append(0)

  if len(end_time_components) == 1:
    end_time_components.append(0)

  # Check if both start and end time components are present
  if len(start_time_components) != 2 or len(end_time_components) != 2:
    print(f"Invalid start or end time components: {start_time}, {end_time}")
    raise ValueError("Invalid start or end time components")

  start_time_minutes = start_time_components[0] * 60 + start_time_components[1]
  end_time_minutes = end_time_components[0] * 60 + end_time_components[1]

  return start_time_minutes, end_time_minutes


# Converts 12hr to 24hr time
def time12_to_24(time12):
  time_components = [int(comp) for comp in re.findall(r'\d+', time12)]
  hour = time_components[0]
  if 'pm' in time12.lower() and hour != 12:
    hour += 12
  minute = time_components[1] if len(time_components) > 1 else 0

  return f"{hour:02d}:{minute:02d}"


# Removes times from string leaving only days
def remove_time_slot():
  for slot in time_slots:
    days, time_range = slot[1].split(' ', 1)
    slot[1] = days


# Final format is [int 'str' int int] = [slot# 'days' start end]  (start and end in minutes)
def format_time():
  global time_slots
  time_slots = add_am_pm()
  # Add a new columns to the existing array representing time slots in minutes
  time_slots = np.column_stack(
      (time_slots, [convert_to_minutes(slot) for slot in time_slots]))
  remove_time_slot()
  return time_slots


def format_time2(time_slots):
  time_slots = add_am_pm()
  # Add a new columns to the existing array representing time slots in minutes
  time_slots = np.column_stack(
      (time_slots, [convert_to_minutes(slot) for slot in time_slots]))
  remove_time_slot()
  return time_slots


# Determines the day of the week and returns 2 or 1
def get_days_of_week(slotNum):
  if time_slots[slotNum - 1][1] == 'TR':
    return 2
  else:
    return 1


# Generates the time conflict list for time conflict comparisons
def generate_conflict_lists():
  i = 0
  conflicts = [[0] for _ in range(86)]
  for slot1 in time_slots:
    conflicts[i][0] = i + 1  # first value
    j = 0
    for slot2 in time_slots:
      if ((slot1[3] >= slot2[2] >= slot1[2])
          or (slot2[3] >= slot1[2] >= slot2[2]) and
          (get_days_of_week(i + 1) == get_days_of_week(j + 1))):
        conflicts[i].append(slot2[0])
      j += 1
    i += 1
  return conflicts


# Generates the credits and returns them
def generate_credits():
  i = 0
  credits = [0] * len(time_slots)
  for slot in time_slots:
    credits[i] = math.ceil((len(slot[1]) * (slot[3] - slot[2])) / 60)
    i += 1
  return credits


# Gets the time of day (evening, afternoon, morning) and returns an integer value accordingly
def get_time_of_day(slotNum):
  if time_slots[slotNum - 1][2] >= 1020:
    # is evening
    return 3
  elif time_slots[slotNum - 1][2] >= 720:
    # is afternoon
    return 2
  else:
    # is morning
    return 1


# Prints list
def print_list(list):
  i = 0
  for row in list:
    i += 1
    print(str(i) + " " + str(row))
  print()


# returns crn based on section number
def get_CRN(sectionNUM):
  return course[sectionNUM - 1][1]


# returns course credits based on section number
def get_course_credits(sectionNUM):
  return course[sectionNUM - 1][3]


# Gets credit hours based on timeslot id
def get_credit_hours(timeslot_ID):
  credits = generate_credits()
  return credits[timeslot_ID - 1]


# Returns some global variables for testing and use elsewhere
def get_values():
  time_slots = format_time()
  time_conflicts = generate_conflict_lists()
  credits = generate_credits()

  return time_slots, time_conflicts, credits


# Checks for a time conflict
def timeconflict(time1, time2):
  if time2 in conflict_list[time1 - 1]:
    return True
  return False


# returns the global time_slots variable
def get_timeslot():
  return time_slots
