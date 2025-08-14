import os
import sys
import tkinter as tk
from threading import Thread
from tkinter import filedialog, messagebox, ttk

import pandas as pd

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from libs.scheduler import create_advanced_schedule


class TextRedirector(object):
    def __init__(self, widget, tags):
        """
        Initializes the redirector with the text widget and a dictionary of color tags.
        """
        self.widget = widget
        self.tags = tags

    def write(self, text_string):
        """
        Writes text to the widget and applies color tags based on content.
        """
        self.widget.configure(state='normal')
        
        if "WARNING:" in text_string:
            self.widget.insert('end', text_string, self.tags['warning'])
        elif "ERROR:" in text_string or "AN ERROR OCCURRED:" in text_string:
            self.widget.insert('end', text_string, self.tags['error'])
        elif "Process finished." in text_string or "Schedule generation complete!" in text_string:
            self.widget.insert('end', text_string, self.tags['success'])
        else:
            self.widget.insert('end', text_string, self.tags['info'])
            
        self.widget.see('end')
        self.widget.configure(state='disabled')

    def flush(self):
        pass

def start_gui(project_root):
    """
    Initializes and runs the main application window using Tkinter.
    """
    root = tk.Tk()
    root.title("ATSS - Advanced Task Scheduling System")
    root.geometry("650x600")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Technician Scheduling System", font=("Helvetica", 16)).pack(pady=5)
    ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=5)
    
    file_frame = ttk.Frame(main_frame)
    file_frame.pack(fill='x', pady=10)

    tasks_file_var = tk.StringVar()
    techs_file_var = tk.StringVar()
    output_dir_var = tk.StringVar()

    default_output_path = os.path.join(project_root, 'output')
    output_dir_var.set(default_output_path)

    ttk.Label(file_frame, text="Tasks File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(file_frame, textvariable=tasks_file_var, state='readonly', width=60).grid(row=0, column=1, sticky='ew')
    ttk.Button(file_frame, text="Browse...", command=lambda: tasks_file_var.set(filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")]))).grid(row=0, column=2, padx=5)

    ttk.Label(file_frame, text="Technicians File:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(file_frame, textvariable=techs_file_var, state='readonly', width=60).grid(row=1, column=1, sticky='ew')
    ttk.Button(file_frame, text="Browse...", command=lambda: techs_file_var.set(filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")]))).grid(row=1, column=2, padx=5)
    
    ttk.Label(file_frame, text="Output Folder:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
    ttk.Entry(file_frame, textvariable=output_dir_var, state='readonly', width=60).grid(row=2, column=1, sticky='ew')
    ttk.Button(file_frame, text="Browse...", command=lambda: output_dir_var.set(filedialog.askdirectory() or default_output_path)).grid(row=2, column=2, padx=5)

    file_frame.columnconfigure(1, weight=1)

    ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=5)

    log_frame = ttk.Frame(main_frame)
    log_frame.pack(fill="both", expand=True, pady=10)
    ttk.Label(log_frame, text="Status Log:").pack(anchor='w')
    
    log_text = tk.Text(log_frame, height=15, state='disabled', bg="#f0f0f0", font=("Consolas", 9))
    log_text.pack(fill="both", expand=True)

    log_tags = {
        'info': 'info',
        'warning': 'warning',
        'error': 'error',
        'success': 'success'
    }
    log_text.tag_configure(log_tags['info'], foreground='black')
    log_text.tag_configure(log_tags['warning'], foreground='#b5830d', font=("Consolas", 9, "bold"))
    log_text.tag_configure(log_tags['error'], foreground='red', font=("Consolas", 9, "bold"))
    log_text.tag_configure(log_tags['success'], foreground='green', font=("Consolas", 9, "bold"))

    sys.stdout = TextRedirector(log_text, log_tags)

    def run_scheduler_thread():
        tasks_file = tasks_file_var.get()
        techs_file = techs_file_var.get()
        output_dir = output_dir_var.get()

        if not all([tasks_file, techs_file, output_dir]):
            messagebox.showerror("Error", "Please select the tasks file, technicians file, and an output folder.")
            generate_button.config(state="normal")
            return

        log_text.configure(state='normal')
        log_text.delete('1.0', 'end')
        log_text.configure(state='disabled')
        generate_button.config(state="disabled")

        print("Starting schedule generation...")
        print(f"Tasks file: {tasks_file}")
        print(f"Technicians file: {techs_file}")
        print(f"Output folder: {output_dir}")
        print("-" * 30)

        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            output_schedule = os.path.join(output_dir, 'scheduled_tasks.xlsx')
            output_unscheduled = os.path.join(output_dir, 'unscheduled_tasks.xlsx')

            try:
                tasks_df = pd.read_excel(tasks_file)
                tasks_df['Date'] = pd.to_datetime(tasks_df['Date'], errors='coerce')
                
                invalid_tasks = tasks_df[tasks_df['Date'].isna()]
                if not invalid_tasks.empty:
                    print("WARNING: The following tasks have invalid or missing dates and will be skipped:")
                    print(invalid_tasks.to_string())
                    print("-" * 30)
                
                tasks_df.dropna(subset=['Date'], inplace=True)

            except Exception as e:
                raise Exception(f"Failed to read or process the tasks file '{tasks_file}'. Error: {e}")

            create_advanced_schedule(
                tasks_df=tasks_df,
                techs_file=techs_file,
                output_schedule_file=output_schedule,
                output_unscheduled_file=output_unscheduled
            )
            
            print("-" * 30)
            print("Process finished.")
            messagebox.showinfo("Success", f'Schedule generation complete!\n\nFiles saved in:\n{output_dir}')

        except Exception as e:
            print(f"\nAN ERROR OCCURRED:\n{e}")
            messagebox.showerror("Error", f'An unexpected error occurred. Please check the status log for details.\n\nError: {e}')
        finally:
            generate_button.config(state="normal")

    def on_generate_click():
        thread = Thread(target=run_scheduler_thread)
        thread.start()

    generate_button = ttk.Button(main_frame, text="Generate Schedule", command=on_generate_click)
    generate_button.pack(pady=10)

    root.mainloop()

    sys.stdout = sys.__stdout__
