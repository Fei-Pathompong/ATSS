# ATSS Project

## Overview
The ATSS (Advanced Task Scheduling System) project is designed to efficiently schedule tasks based on technician availability and task requirements. It utilizes Object-Oriented Programming (OOP) principles to encapsulate the properties and methods related to tasks, technicians, and the scheduling process.

## File Structure
```
atss
├── src
├── ├── objects
│   │   ├── scheduler.py      # Contains the main scheduling logic using OOP principles
│   │   └── __init__.py       # Marks the objects directory as a Python package
├── requirements.txt       # Lists project dependencies
└── README.md              # Documentation for the project
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use the scheduling system, run the `scheduler.py` file. This will read tasks and technician availability from specified Excel files and generate a schedule based on the defined constraints.

### Example
1. Prepare your `tasks.xlsx` and `technicians.xlsx` files with the required data.
2. Execute the script:
   ```
   python src/scheduler.py
   ```

## Classes
- **Task**: Represents a task with properties such as date, machine name, hours required, and people required.
- **Technician**: Represents a technician with properties such as name, availability, and status.
- **Scheduler**: Manages the scheduling process, checking technician availability and assigning tasks accordingly.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.