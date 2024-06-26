from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import pickle
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('ToDo List!')
        self.root.config(bg='#223441')
        self.root.geometry("650x500")

        self.my_font = Font(family="Helvetica", size=18, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        # Display instructions as plain text
        instructions_label = Label(self.root, text="To-Do List", font=('Helvetica', 20, 'bold'), bg='#223441', fg='white')
        instructions_label.pack(pady=20)

        # Frame for the listbox and scrollbar
        self.my_frame = Frame(self.root)
        self.my_frame.pack(pady=10)

        # Listbox to display tasks
        self.my_list = Listbox(self.my_frame, font=self.my_font, width=28, height=7, bg="white",
                               bd=0, fg="#223441", highlightthickness=0, selectbackground="#223441", activestyle="none")
        self.my_list.pack(side=LEFT, fill=BOTH, expand=True)

        # Sample tasks
        self.stuff = ["Walk The Dog", "Buy Groceries", "Take A Nap"]
        for item in self.stuff:
            self.my_list.insert(END, item)

        # Scrollbar for the listbox
        self.my_scrollbar = Scrollbar(self.my_frame)
        self.my_scrollbar.pack(side=RIGHT, fill=BOTH)

        self.my_list.config(yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_list.yview)

        # Entry for adding new tasks
        self.my_entry = Entry(self.root, font=("Helvetica", 18), width=26)
        self.my_entry.pack(pady=20)

        # Frame for buttons
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=20)

        # Create buttons for various actions
        self.create_buttons()

        # Create menu for file operations
        self.create_menu()

    def create_buttons(self):
        # Buttons for task operations
        add_button = Button(self.button_frame, text="Add Task", bg='gray', font=('Helvetica 11'), command=self.add_item)
        delete_button = Button(self.button_frame, text="Delete Task", bg='blue', font=('Helvetica 11'), command=self.delete_item)
        mark_done_button = Button(self.button_frame, text="Mark as Done", bg='gray', font=('Helvetica 11'), command=self.mark_done)
        mark_undone_button = Button(self.button_frame, text="Mark as Undone", bg='blue', font=('Helvetica 11'), command=self.mark_undone)
        delete_done_button = Button(self.button_frame, text="Delete Done Tasks", bg='gray', font=('Helvetica 11'), command=self.delete_done)
        edit_button = Button(self.button_frame, text="Edit Task", bg='blue', font=('Helvetica 11'), command=self.edit_item)

        # Grid layout for buttons
        add_button.grid(row=0, column=0)
        delete_button.grid(row=0, column=1, padx=5)
        mark_done_button.grid(row=0, column=2)
        mark_undone_button.grid(row=0, column=3, padx=5)
        delete_done_button.grid(row=0, column=4)
        edit_button.grid(row=0, column=5, padx=5)

    def create_menu(self):
        # Create menu for file operations
        my_menu = Menu(self.root)
        self.root.config(menu=my_menu)

        file_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="Save/Open File", menu=file_menu)

        # Menu options for saving, opening, and clearing list
        file_menu.add_command(label="Save List", command=self.save_list)
        file_menu.add_command(label="Open List", command=self.open_list)
        file_menu.add_separator()
        file_menu.add_command(label="Clear List", command=self.delete_list)

    def delete_item(self):
        # Delete selected item from listbox
        self.my_list.delete(ANCHOR)

    def add_item(self):
        # Add new task to listbox
        task = self.my_entry.get()
        if task:
            self.my_list.insert(END, task)
            self.my_entry.delete(0, END)

    def mark_done(self):
        # Mark selected task as done (change text color to gray)
        self.my_list.itemconfig(self.my_list.curselection(), fg="gray")
        self.my_list.selection_clear(0, END)

    def mark_undone(self):
        # Mark selected task as undone (change text color back to default)
        self.my_list.itemconfig(self.my_list.curselection(), fg="#223441")
        self.my_list.selection_clear(0, END)

    def delete_done(self):
        # Delete all tasks marked as done (gray text)
        count = 0
        while count < self.my_list.size():
            if self.my_list.itemcget(count, "fg") == "gray":
                self.my_list.delete(count)
            else:
                count += 1

    def save_list(self):
        # Save current list to a file using pickle
        file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save File",
                                                 filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*")))
        if file_name:
            if not file_name.endswith(".dat"):
                file_name = f'{file_name}.dat'

            # Remove done tasks before saving
            count = 0
            while count < self.my_list.size():
                if self.my_list.itemcget(count, "fg") == "gray":
                    self.my_list.delete(count)
                else:
                    count += 1

            # Get remaining tasks and save to file
            stuff = self.my_list.get(0, END)

            with open(file_name, 'wb') as output_file:
                pickle.dump(stuff, output_file)

    def open_list(self):
        # Open a saved list from a file
        file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File",
                                               filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*")))
        if file_name:
            # Clear current list
            self.my_list.delete(0, END)

            # Load tasks from file and populate listbox
            with open(file_name, 'rb') as input_file:
                stuff = pickle.load(input_file)
                for item in stuff:
                    self.my_list.insert(END, item)

    def delete_list(self):
        # Clear all tasks from the listbox
        self.my_list.delete(0, END)

    def edit_item(self):
        # Edit selected task in the entry widget
        selected_task_index = self.my_list.curselection()
        if selected_task_index:
            task_text = self.my_list.get(selected_task_index)
            self.my_entry.delete(0, END)
            self.my_entry.insert(0, task_text)
            self.delete_item()

if __name__ == "__main__":
    root = Tk()
    app = ToDoApp(root)
    root.mainloop()
