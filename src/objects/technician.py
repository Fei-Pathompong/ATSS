from datetime import datetime


class Technician:
    """
    Represents a technician.
    This revised version simplifies the class to only manage the technician's
    name and their busy schedule across all days.
    """
    def __init__(self, name: str):
        """
        Initializes a Technician instance.
        Args:
            name (str): The name of the technician.
        """
        self.name = name
        self.busy_schedule = []

    def is_available(self, start_time: datetime, end_time: datetime, day_availability: dict) -> bool:
        """
        Checks if the technician is available for a given time interval on a specific day.
        
        Args:
            start_time (datetime): The potential start time for a task.
            end_time (datetime): The potential end time for a task.
            day_availability (dict): A dictionary containing the technician's work hours
                                     and status for that specific day.
                                     e.g., {'start': time(8,0), 'end': time(17,0), 'status': 'Normal'}
        
        Returns:
            bool: True if the technician is available, False otherwise.
        """
        if not day_availability or day_availability['status'] != 'Normal':
            return False

        tech_work_start = datetime.combine(start_time.date(), day_availability['start'])
        tech_work_end = datetime.combine(start_time.date(), day_availability['end'])
        
        if not (tech_work_start <= start_time and end_time <= tech_work_end):
            return False
            
        for busy_start, busy_end in self.busy_schedule:
            if max(start_time, busy_start) < min(end_time, busy_end):
                return False
                
        return True

    def assign_task(self, start_time: datetime, end_time: datetime):
        """
        Assigns a task to the technician by adding the time interval to their busy schedule.
        
        Args:
            start_time (datetime): The start time of the assigned task.
            end_time (datetime): The end time of the assigned task.
        """
        self.busy_schedule.append((start_time, end_time))
