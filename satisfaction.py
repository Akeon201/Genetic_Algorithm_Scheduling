import pandas as pd

global teach_sat, classrooms
'''
Teacher ID starts at 1 and goes to 10
'''


def set_file(file_name):
  global teach_sat, classrooms
  teach_sat = pd.read_excel(file_name,
                            sheet_name='Teacher Satisfaction').to_numpy()
  classrooms = pd.read_excel(file_name,
                            sheet_name='(J) Classrooms').to_numpy()


# Get min section preference by teacher ID
def get_min_sections(id):  #C
  return teach_sat[id][1]


def get_board_type(classroomID):
  return classrooms[classroomID-1][1]


# Get max section preference by teacher ID
def get_max_sections(id):  #C
  return teach_sat[id][2]


# Get board type preference by teacher ID
def get_board_pref(id):  #P
  return teach_sat[id][3]


# Get time of day preference by teacher ID
def get_time_pref(id):  #P
  return teach_sat[id][4]


# Get days of week preference by teacher ID
def get_day_pref(id):  #P
  return teach_sat[id][5]


def get_satisfaction(id, section):  #P
  return teach_sat[id][section + 5]

