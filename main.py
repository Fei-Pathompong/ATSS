import os
import sys

from src.ui.gui import start_gui


def main():
    """
    Sets up the application environment and starts the GUI.
    This is the main entry point for the ATSS application.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, src_path)
    print(sys.path)
    
    start_gui(project_root)

if __name__ == "__main__":
    main()
