import tkinter as tk
import pandas as pd
import os
import genetic_algorithm as ga
import timeslots
import satisfaction
from datetime import datetime


def get_start_time(slot_id, time_slot_descriptions):
    description = time_slot_descriptions[slot_id]['description']
    # Splitting the description into day part and time part
    day_part, time_part = description.split(' ', 1)
    start_time_str, end_time_str = time_part.split('-')

    # Extracting hour and minute
    hour, minute_part = start_time_str.strip().split(':')
    hour = int(hour)
    minute = int(minute_part[:2])  # Extracting only the minute digits

    # Determine if it's PM and convert to 24-hour format if necessary
    if 'pm' in minute_part.lower() and hour < 12:
        hour += 12

    # Return a time object
    return datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()


# Function to parse the description of time slots and convert to day indices
def parse_description(description):
    days_map = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4}
    day_indices = [days_map[day] for day in description.split(' ')[0] if day in days_map]
    return day_indices



def sort_schedule(schedule_list, time_slot_descriptions):
    return sorted(schedule_list, key=lambda entry: get_start_time(entry[2], time_slot_descriptions))


# Function to load data from an Excel file
def load_file(file_name: str):
    sim_course_sections = pd.read_excel(
        file_name, sheet_name='(I) Simulated Course Sections').to_numpy()
    classrooms = pd.read_excel(file_name, sheet_name='(J) Classrooms').to_numpy()
    teacher_satisfaction = pd.read_excel(
        file_name, sheet_name='Teacher Satisfaction').to_numpy()
    time_slots_array = pd.read_excel(file_name, sheet_name='(K) Time Slots').to_numpy()
    time_slots_dict = {row[0]: {'description': row[1], 'day_index': parse_description(row[1])} for row in time_slots_array}
    return sim_course_sections, classrooms, time_slots_dict, teacher_satisfaction

# Function to check if the provided file is valid
def check_valid_file(file_name):
    directory = os.getcwd()
    listed_directory = os.listdir(directory)
    while file_name not in listed_directory:
        print("File not found, please try again.")
        file_name = input("Please enter file name with extension: ")
    return file_name

# Function to create the schedule on the GUI
def create_schedule(root, schedule_list, time_slot_descriptions):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # Create a canvas with a scrollbar
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Place the headers for the days
    for i, day in enumerate(days):
        tk.Label(scrollable_frame, text=day).grid(row=0, column=i + 1, sticky="ew", padx=10, pady=10)

    # Initialize a list to keep track of the row indices for each day
    day_row_indices = [1] * len(days)

    # Loop through the sorted schedule entries
    for entry in sort_schedule(schedule_list, time_slot_descriptions):
        teacher_id, room_id, slot_id = entry
        slot_info = time_slot_descriptions.get(slot_id, None)

        if slot_info:
            description = slot_info['description']
            day_indices = slot_info['day_index']

            # Place the entry under each applicable day without empty spaces
            for day_index in day_indices:
                current_row = day_row_indices[day_index]
                tk.Label(scrollable_frame, text=f"Teacher: {teacher_id}\nRoom: {room_id}\nTime: {description}").grid(
                    row=current_row, column=day_index + 1, sticky="ew", padx=10, pady=10)
                day_row_indices[day_index] += 1  # Increment the row index for that day

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# Main function to set up the application window
def main():
    root = tk.Tk()
    root.title("Schedule")
    # Set a reasonable size for the initial window
    root.geometry('800x600')

    file_name = "Simulated Data.xlsx"
    file_name = check_valid_file(file_name)
    sim_course_sections, classrooms, time_slot_descriptions, teacher_satisfaction = load_file(file_name)

    # Generate the schedule list using the genetic algorithm (as an example)
    schedule_list = ga.generate_hypothesis()

    # Sort the schedule list based on time before creating the schedule
    sorted_schedule_list = sort_schedule(schedule_list, time_slot_descriptions)

    create_schedule(root, sorted_schedule_list, time_slot_descriptions)
    root.mainloop()

if __name__ == "__main__":
    file_name = "Simulated Data.xlsx"
    satisfaction.set_file(file_name)
    timeslots.set_file(file_name)
    main()
