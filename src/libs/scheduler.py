import os
from collections import defaultdict
from datetime import datetime, time, timedelta

import pandas as pd

from src.objects.task import Task
from src.objects.technician import Technician

# --- Configuration ---
# Load environment variables or use defaults
WORKDAY_START_HOUR = int(os.getenv("WORKDAY_START_HOUR", 8))
WORKDAY_END_HOUR = int(os.getenv("WORKDAY_END_HOUR", 17))
SCHEDULER_INTERVAL_MINUTES = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", 15))


class Scheduler:
    """
    Scheduler class for assigning tasks to technicians based on availability.
    """
    def __init__(self, tasks, technicians_availability):
        self.tasks = tasks
        self.technicians_availability = technicians_availability
        self.technicians = {name: Technician(name) for name in technicians_availability.keys()}
        
        self.final_schedule = []
        self.unscheduled_tasks = []

    def schedule_tasks(self):
        """
        Groups tasks by date and processes each day individually.
        """
        tasks_by_date = defaultdict(list)
        for task in self.tasks:
            tasks_by_date[task.date].append(task)

        for task_date in sorted(tasks_by_date.keys()):
            tasks_for_day = tasks_by_date[task_date]
            sorted_tasks_for_day = sorted(tasks_for_day, key=lambda t: -t.people_required)
            self._schedule_tasks_for_day(task_date, sorted_tasks_for_day)

    def _schedule_tasks_for_day(self, task_date, tasks):
        """Schedules all tasks for a single given day."""
        task_day_name = task_date.strftime('%A')
        
        techs_on_duty = [
            tech_object for name, tech_object in self.technicians.items()
            if self.technicians_availability.get(name, {}).get(task_day_name)
        ]

        for task in tasks:
            self._find_slot_for_task(task, task_day_name, techs_on_duty)

    def _find_slot_for_task(self, task, task_day_name, techs_on_duty):
        """Finds an available time slot and team for a single task."""
        day_start = datetime.combine(task.date, time(WORKDAY_START_HOUR, 0))
        day_end = datetime.combine(task.date, time(WORKDAY_END_HOUR, 0))
        
        possible_start_time = day_start
        
        while possible_start_time + timedelta(hours=task.hours_required) <= day_end:
            potential_end_time = possible_start_time + timedelta(hours=task.hours_required)
            
            available_team = []
            for tech_object in techs_on_duty:
                tech_day_availability = self.technicians_availability.get(tech_object.name, {}).get(task_day_name)
                if tech_object.is_available(possible_start_time, potential_end_time, tech_day_availability):
                    available_team.append(tech_object)

            if len(available_team) >= task.people_required:
                assigned_team = available_team[:task.people_required]
                self.final_schedule.append({
                    'Date': task.date.strftime('%Y-%m-%d'),
                    'Start Time': possible_start_time.strftime('%H:%M'),
                    'End Time': potential_end_time.strftime('%H:%M'),
                    'Machine': task.machine_name,
                    'Assigned Technicians': ', '.join(tech.name for tech in assigned_team)
                })
                for tech in assigned_team:
                    tech.assign_task(possible_start_time, potential_end_time)
                return

            possible_start_time += timedelta(minutes=SCHEDULER_INTERVAL_MINUTES)
        
        self.unscheduled_tasks.append({
            'Date': task.date.strftime('%Y-%m-%d'),
            'Machine Name': task.machine_name,
            'Hours Required': task.hours_required,
            'People Required': task.people_required,
            'Reason': 'Could not find an available time slot with enough technicians.'
        })

    def save_schedule(self, output_schedule_file, output_unscheduled_file):
        """Saves the final schedule and unscheduled tasks to Excel files."""
        if self.final_schedule:
            pd.DataFrame(self.final_schedule).to_excel(output_schedule_file, index=False)
            print(f"✅ Schedule successfully generated and saved to '{output_schedule_file}'")
        else:
            print("⚠️ No tasks could be scheduled.")
        if self.unscheduled_tasks:
            pd.DataFrame(self.unscheduled_tasks).to_excel(output_unscheduled_file, index=False)
            print(f"❌ Some tasks could not be scheduled. See '{output_unscheduled_file}' for details.")
        else:
            print("🎉 All tasks were successfully scheduled!")


def load_technician_availability(techs_df):
    """Processes the technician dataframe into a structured dictionary."""
    availability = {}
    for _, row in techs_df.iterrows():
        name = row['Technician Name']
        if name not in availability:
            availability[name] = {}
        
        start_time_str = str(row['Available Start'])
        end_time_str = str(row['Available End'])
        
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time() if ':' in start_time_str else pd.to_datetime(start_time_str).time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time() if ':' in end_time_str else pd.to_datetime(end_time_str).time()

        availability[name][row['Day of Week']] = {
            "start": start_time,
            "end": end_time,
            "status": row['Status']
        }
    return availability


def create_advanced_schedule(tasks_df, techs_file, output_schedule_file, output_unscheduled_file):
    """
    Main function to run the scheduling process.
    Accepts a pre-loaded tasks DataFrame to allow for pre-processing.
    """
    try:
        techs_df = pd.read_excel(techs_file)
    except Exception as e:
        raise Exception(f"Failed to read or process the technicians file '{techs_file}'. Error: {e}")

    # Create Task objects from the cleaned DataFrame
    tasks = [Task(row['Date'], row['Machine Name'], row['Hours Required'], row['People Required']) for _, row in tasks_df.iterrows()]
    
    technician_availability_data = load_technician_availability(techs_df)

    scheduler = Scheduler(tasks, technician_availability_data)
    scheduler.schedule_tasks()
    scheduler.save_schedule(output_schedule_file, output_unscheduled_file)


if __name__ == '__main__':
    base_path = os.path.join(os.path.dirname(__file__), '..', '..')
    tasks_path = os.path.join(base_path, 'input_examples', 'tasks.xlsx')
    techs_path = os.path.join(base_path, 'input_examples', 'technicians.xlsx')
    output_path = os.path.join(base_path, 'output')
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    create_advanced_schedule(
        tasks_file=tasks_path,
        techs_file=techs_path,
        output_schedule_file=os.path.join(output_path, 'scheduled_tasks.xlsx'),
        output_unscheduled_file=os.path.join(output_path, 'unscheduled_tasks.xlsx')
    )
