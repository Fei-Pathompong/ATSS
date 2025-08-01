class Task:
    """
    Represents a scheduled task assigned to a machine, including details such as date, machine name, required hours, and required personnel.
    
    Attributes:
        date (str): The date the task is scheduled for.
        machine_name (str): The name of the machine assigned to the task.
        hours_required (float): The number of hours required to complete the task.
        people_required (int): The number of people required to complete the task.
    
    Methods:
        __init__(date, machine_name, hours_required, people_required):
            Initializes a Task instance with the specified attributes.
        update_hours(new_hours):
            Updates the number of hours required for the task.
        update_people(new_people):
            Updates the number of people required for the task.
        change_machine(new_machine_name):
            Changes the machine assigned to the task.
        reschedule(new_date):
            Changes the date of the task.
        to_dict():
            Returns a dictionary representation of the task.
    """
    def __init__(self, 
                 date: str, 
                 machine_name: str, 
                 hours_required: float, 
                 people_required: int) -> None:
        """
        Initializes a Task instance.

        Args:
            date (str): The date the task is scheduled for.
            machine_name (str): The name of the machine assigned to the task.
            hours_required (float): The number of hours required to complete the task.
            people_required (int): The number of people required to complete the task.
        """
        self.date = date
        self.machine_name = machine_name
        self.hours_required = hours_required
        self.people_required = people_required

    def update_hours(self, new_hours: float) -> None:
        """
        Updates the number of hours required for the task.

        Args:
            new_hours (float): The new number of hours required.
        """
        self.hours_required = new_hours

    def update_people(self, new_people: int) -> None:
        """
        Updates the number of people required for the task.

        Args:
            new_people (int): The new number of people required.
        """
        self.people_required = new_people

    def change_machine(self, new_machine_name: str) -> None:
        """
        Changes the machine assigned to the task.

        Args:
            new_machine_name (str): The new machine name.
        """
        self.machine_name = new_machine_name

    def reschedule(self, new_date: str) -> None:
        """
        Changes the date of the task.

        Args:
            new_date (str): The new date for the task.
        """
        self.date = new_date

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the task.
        """
        return {
            "date": self.date,
            "machine_name": self.machine_name,
            "hours_required": self.hours_required,
            "people_required": self.people_required
        }
