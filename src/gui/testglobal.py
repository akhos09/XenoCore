import subprocess
import customtkinter as ctk
from tkinter import ttk, Menu
import threading

# Function to run the command and capture output with progress updates
def run_vagrant_command(command, machine_id, *args):
    # Initialize progress to 0
    progress_bar.set(0)
    status_label.configure(text=f"Running {command} on {machine_id}...")
    app.update()

    try:
        # Simulate a long-running task (you could monitor the process or use other mechanisms)
        process = subprocess.Popen(["vagrant", command, machine_id, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Process output line by line to update the progress bar
        for line in process.stdout:
            # Example of checking output (you can enhance this for actual progress information)
            line_str = line.decode('utf-8')
            if "progress" in line_str:  # Look for any markers in the output
                progress = int(line_str.split(" ")[-1].strip('%'))  # Placeholder for actual progress
                progress_bar.set(progress)  # Update progress bar
            app.update()  # Update the UI

        process.wait()  # Wait for the process to complete
    except subprocess.CalledProcessError as e:
        status_label.configure(text=f"Error: {e.stderr}")
    finally:
        update_treeview()  # Update the treeview after the operation
        progress_bar.set(100)  # Ensure progress bar reaches 100%
        status_label.configure(text="Task completed")

# Function to start a machine in a background thread
def start_machine():
    selected_item = tree.selection()[0]
    machine_id = tree.item(selected_item, "values")[0]
    task_thread = threading.Thread(target=run_vagrant_command, args=("up", machine_id))
    task_thread.start()

# Function to stop a machine in a background thread
def stop_machine():
    selected_item = tree.selection()[0]
    machine_id = tree.item(selected_item, "values")[0]
    task_thread = threading.Thread(target=run_vagrant_command, args=("halt", machine_id))
    task_thread.start()

# Function to reload a machine in a background thread
def reload_machine():
    selected_item = tree.selection()[0]
    machine_id = tree.item(selected_item, "values")[0]
    task_thread = threading.Thread(target=run_vagrant_command, args=("reload", machine_id))
    task_thread.start()

# Function to delete a machine in a background thread
def delete_machine():
    selected_item = tree.selection()[0]
    machine_id = tree.item(selected_item, "values")[0]
    task_thread = threading.Thread(target=run_vagrant_command, args=("destroy", machine_id, "-f"))
    task_thread.start()

# Function to update the treeview with the parsed data
def update_treeview():
    output = get_vagrant_status()
    data = parse_vagrant_status(output)
    tree.delete(*tree.get_children())  # Clear the treeview
    for item in data:
        tree.insert("", "end", values=(item["id"], item["name"], item["provider"], item["state"], item["directory"]))

# Function to run the command and capture output
def get_vagrant_status():
    try:
        # Run the command and capture the output
        result = subprocess.run(
            ["vagrant", "global-status"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

# Function to parse the output into a structured format
def parse_vagrant_status(output):
    lines = output.splitlines()
    data = []
    for line in lines[2:]:  # Skip the header lines
        if not line.strip():  # Skip empty lines
            continue
        if line.startswith("The above shows information"):  # Skip final message
            break
        parts = line.split()
        if len(parts) >= 5:  # Ensure the line contains machine data
            data.append({
                "id": parts[0],
                "name": parts[1],
                "provider": parts[2],
                "state": parts[3],
                "directory": " ".join(parts[4:])
            })
    return data

# Function to show the context menu on right-click
def show_context_menu(event):
    item = tree.identify_row(event.y)  # Get the item under the cursor
    if item:
        tree.selection_set(item)  # Select the item
        context_menu.post(event.x_root, event.y_root)  # Show the menu at the cursor position

# Create the main window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("XenoDashBoard")
app.geometry("800x500")

# Create a frame for the treeview
frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Create a treeview widget
tree = ttk.Treeview(frame, columns=("ID", "Name", "Provider", "State", "Directory"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Provider", text="Provider")
tree.heading("State", text="State")
tree.heading("Directory", text="Directory")
tree.column("ID", width=20)
tree.column("Name", width=60)
tree.column("Provider", width=30)
tree.column("State", width=40)
tree.column("Directory", width=150)
tree.pack(fill="both", expand=True)

# Create a context menu
context_menu = Menu(app, tearoff=0)
context_menu.add_command(label="Start", command=start_machine)
context_menu.add_command(label="Stop", command=stop_machine)
context_menu.add_command(label="Reload", command=reload_machine)
context_menu.add_command(label="Delete", command=delete_machine)

# Bind the right-click event to show the context menu
tree.bind("<Button-3>", show_context_menu)  # For Windows/Linux
tree.bind("<Button-2>", show_context_menu)  # For macOS

# Create a button to refresh the treeview
refresh_button = ctk.CTkButton(app, text="Refresh", command=update_treeview)
refresh_button.pack(pady=10)

# Create a progress bar to show task progress
progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.pack(pady=20)

# Create a label to display status
status_label = ctk.CTkLabel(app, text="Ready")
status_label.pack(pady=10)

# Initial update of the treeview
update_treeview()

# Run the application
app.mainloop()


# #TOOLTIP OPTION
# import tkinter as tk
# import Pmw

# # Initialize the main Tkinter application
# root = tk.Tk()
# root.title("Balloon Tooltip Example")

# # Initialize Pmw
# Pmw.initialise(root)

# # Create a label (e.g., an info icon)
# info_icon = tk.Label(root, text="ℹ️", font=("Arial", 16), cursor="hand2")
# info_icon.pack(pady=20)

# # Create a Balloon widget
# tooltip = Pmw.Balloon(root)

# # Attach the Balloon to the info icon
# tooltip.bind(info_icon, "This is some additional information displayed as a tooltip.")

# # Start the Tkinter event loop
# root.mainloop()