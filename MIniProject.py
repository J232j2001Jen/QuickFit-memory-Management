# J A Landsberger - 521446001 - s92086001
# Quick Fit Memory Management System with GUI
# This program uses the Tkinter library to simulate a memory allocation and deallocation system using the Quick Fit strategy.

import tkinter as tk
from tkinter import messagebox, simpledialog


class QuickFit:
    def __init__(self, memory_blocks):
        """
        Initialize the memory management system.
        :param memory_blocks: Dictionary of size-specific lists for memory blocks.
        """
        self.memory_blocks = memory_blocks  # Dictionary of available memory blocks categorized by size
        self.allocated_processes = {}  # Dictionary to track allocated processes

    def allocate(self, process_id, size):
        """
        Allocate memory to a process based on the requested size.
        :param process_id: Identifier of the process.
        :param size: Memory size required by the process.
        :return: Tuple (success, message)
        """
        # First, try to find an exact match for the requested size
        if size in self.memory_blocks and self.memory_blocks[size]:
            allocated_block = self.memory_blocks[size].pop(0)  # Remove the first available block of the required size
            self.allocated_processes[process_id] = {
                'block': allocated_block,
                'size': size
            }
            return True, f"Process {process_id} allocated to {allocated_block} ({size} KB)."

        # If no exact match is found
        return False, f"No exact block available for Process {process_id} requiring {size} KB."

    def deallocate(self, process_id):
        """
        Deallocate a memory block for a specific process.
        :param process_id: Identifier of the process to deallocate.
        :return: Tuple (success, message)
        """
        if process_id not in self.allocated_processes:
            return False, f"No allocation found for Process {process_id}."

        # Retrieve allocation details
        allocation = self.allocated_processes[process_id]
        block_size = allocation['size']
        block_name = allocation['block']

        # Return block to the available memory pool
        if block_size in self.memory_blocks:
            self.memory_blocks[block_size].append(block_name)
        else:
            # Create a new list for this block size if it doesn't exist
            self.memory_blocks[block_size] = [block_name]

        # Remove the process from allocated processes
        del self.allocated_processes[process_id]
        return True, f"Block {block_name} ({block_size} KB) deallocated."

    def get_memory_state(self):
        """
        Get the current state of memory blocks.
        :return: Formatted string of memory state
        """
        state = "Available Memory Blocks:\n"
        for size, blocks in self.memory_blocks.items():
            state += f"{size} KB Blocks: {blocks}\n"

        state += "\nAllocated Processes:\n"
        for process, details in self.allocated_processes.items():
            state += f"Process {process}: {details['block']} ({details['size']} KB)\n"

        return state


class QuickFitGUI:
    def __init__(self, master):
        """
        Initialize the Tkinter GUI for Quick Fit Memory Management.
        :param master: Root Tkinter window
        """
        self.master = master
        master.title("Quick Fit Memory Management")
        master.geometry("600x500")

        # Initial memory blocks setup
        initial_blocks = {
            50: ["Block1", "Block2"],
            100: ["Block3", "Block4"],
            200: ["Block5"]
        }
        self.quick_fit = QuickFit(initial_blocks)

        # Create and configure the GUI components
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout GUI widgets.
        """
        # Allocation Frame
        alloc_frame = tk.LabelFrame(self.master, text="Memory Allocation", padx=10, pady=10)
        alloc_frame.pack(padx=10, pady=10, fill="x")

        # Process ID Entry
        tk.Label(alloc_frame, text="Process ID:").grid(row=0, column=0, sticky="w")
        self.process_id_entry = tk.Entry(alloc_frame, width=20)
        self.process_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Memory Size Entry
        tk.Label(alloc_frame, text="Memory Size (KB):").grid(row=1, column=0, sticky="w")
        self.size_entry = tk.Entry(alloc_frame, width=20)
        self.size_entry.grid(row=1, column=1, padx=5, pady=5)

        # Allocate Button
        allocate_btn = tk.Button(alloc_frame, text="Allocate Memory", command=self.allocate_memory)
        allocate_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Deallocation Frame
        dealloc_frame = tk.LabelFrame(self.master, text="Memory Deallocation", padx=10, pady=10)
        dealloc_frame.pack(padx=10, pady=10, fill="x")

        # Deallocate Button
        deallocate_btn = tk.Button(dealloc_frame, text="Deallocate Process", command=self.deallocate_memory)
        deallocate_btn.pack(pady=5)

        # Memory State Display
        state_frame = tk.LabelFrame(self.master, text="Memory State", padx=10, pady=10)
        state_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.state_text = tk.Text(state_frame, height=10, width=70, wrap=tk.WORD)
        self.state_text.pack(padx=5, pady=5)

        # Refresh State Button
        refresh_btn = tk.Button(self.master, text="Refresh Memory State", command=self.refresh_state)
        refresh_btn.pack(pady=5)

        # Display the initial memory state
        self.refresh_state()

    def allocate_memory(self):
        """
        Handle memory allocation based on user input from the GUI.
        """
        process_id = self.process_id_entry.get()
        size_str = self.size_entry.get()

        # Validate input fields
        if not process_id or not size_str:
            messagebox.showerror("Error", "Please enter both Process ID and Memory Size")
            return

        try:
            size = int(size_str)  # Convert memory size to integer
        except ValueError:
            messagebox.showerror("Error", "Memory Size must be a number")
            return

        # Attempt to allocate memory
        success, message = self.quick_fit.allocate(process_id, size)

        if success:
            messagebox.showinfo("Allocation Success", message)
        else:
            messagebox.showwarning("Allocation Failed", message)

        # Clear input fields
        self.process_id_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)

        # Refresh memory state display
        self.refresh_state()

    def deallocate_memory(self):
        """
        Handle memory deallocation via a dialog.
        """
        process_id = simpledialog.askstring("Deallocate", "Enter Process ID to Deallocate:")

        if not process_id:
            return

        # Attempt to deallocate memory
        success, message = self.quick_fit.deallocate(process_id)

        if success:
            messagebox.showinfo("Deallocation Success", message)
        else:
            messagebox.showwarning("Deallocation Failed", message)

        # Refresh memory state display
        self.refresh_state()

    def refresh_state(self):
        """
        Refresh the memory state display in the GUI.
        """
        # Clear the current text display
        self.state_text.delete(1.0, tk.END)

        # Fetch and display the current memory state
        state = self.quick_fit.get_memory_state()
        self.state_text.insert(tk.END, state)


def main():
    """
    Main function to run the Tkinter GUI application.
    """
    root = tk.Tk()
    quick_fit_gui = QuickFitGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
