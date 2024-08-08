import tkinter as tk
from context import Context
from utils.actions import Actions

class ControlWindow:
    def __init__(self, master):
        self.master = master
        self.context = Context()
        master.title("Robot Control")
        master.geometry("400x300")  # Increased window size

        self.create_widgets()

    def create_widgets(self):
        # Interact button
        self.interact_button = tk.Button(self.master, text="Interact", command=self.interact)
        self.interact_button.pack(pady=10)

        # Destroy button
        self.destroy_button = tk.Button(self.master, text="Destroy", command=self.destroy)
        self.destroy_button.pack(pady=10)

        # Clear Orders button
        self.clear_button = tk.Button(self.master, text="Clear Orders", command=self.clear_orders)
        self.clear_button.pack(pady=10)

        # Set Arms Default button
        self.set_arms_default_button = tk.Button(self.master, text="Set Arms Default", command=self.set_arms_default)
        self.set_arms_default_button.pack(pady=10)

        # Move Forward button
        self.move_forward_button = tk.Button(self.master, text="Move Forward", command=self.move_forward)
        self.move_forward_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.master, text="Status: Ready")
        self.status_label.pack(pady=10)

    def interact(self):
        self.status_label.config(text="Status: Interacting with context")
        # Add your interaction logic here
        print("Interacting with context")

    def destroy(self):
        self.status_label.config(text="Status: Destroying")
        print("Destroying")
        self.context.destruct(self.context.data.index)  # Assuming 0 is a valid index, adjust as needed

    def clear_orders(self):
        self.status_label.config(text="Status: Clearing orders")
        print("Clearing orders")
        self.context.clearAction()

    def set_arms_default(self):
        self.status_label.config(text="Status: Setting arms to default position")
        print("Setting arms to default position")
        # Implement the logic to set arms to default position
        # You might need to add this method to your Context or Body class

    def move_forward(self):
        self.status_label.config(text="Status: Moving forward")
        print("Moving forward")
        # Implement the logic to move the robot forward
        # You might need to add this method to your Context or Body class

if __name__ == "__main__":
    root = tk.Tk()
    control_window = ControlWindow(root)
    root.mainloop()