import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkinter import font as tkfont

# Initialize Database
conn = sqlite3.connect('school.db')
c = conn.cursor()

# Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS student_courses (
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
            )''')

conn.commit()

# Custom Styles
class CustomStyle(ttk.Style):
    def __init__(self):
        super().__init__()
        self.configure('TNotebook', background='#f0f0f0')
        self.configure('TNotebook.Tab', padding=[10, 5], font=('Helvetica', 10))
        self.configure('TFrame', background='#ffffff')
        self.configure('TButton', padding=5, relief='flat', background='#4a8abc', foreground='Black')
        self.configure('TButton', font=('Helvetica', 10, 'bold'))
        self.configure('TLabel', background='#ffffff', font=('Helvetica', 10))
        self.configure('TEntry', font=('Helvetica', 10))
        self.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))

# Tkinter Application
class SchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student and Course Management")
        self.root.geometry("1200x1000")
        self.root.configure(bg='#f0f0f0')
        
        self.style = CustomStyle()
        
        # Create Tabs
        self.tab_control = ttk.Notebook(root)
        self.tab_students = ttk.Frame(self.tab_control)
        self.tab_courses = ttk.Frame(self.tab_control)
        self.tab_assignments = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_students, text='Manage Students')
        self.tab_control.add(self.tab_courses, text='Manage Courses')
        self.tab_control.add(self.tab_assignments, text='Assign Courses')
        
        self.tab_control.pack(expand=1, fill='both', padx=10, pady=10)
        
        # Student Tab
        self.manage_students()
        # Courses Tab
        self.manage_courses()
        # Assign Tab
        self.assign_courses()
        
    def manage_students(self):
        frame = ttk.Frame(self.tab_students)
        frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        ttk.Label(frame, text="Student Name").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.student_name = ttk.Entry(frame, width=30)
        self.student_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Add Student", command=self.add_student).grid(row=0, column=2, padx=5, pady=5)
        
        self.student_tree = ttk.Treeview(frame, columns=('ID', 'Name'), show='headings', height=15)
        self.student_tree.heading('ID', text='ID')
        self.student_tree.heading('Name', text='Name')
        self.student_tree.column('ID', width=50)
        self.student_tree.column('Name', width=200)
        self.student_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.student_tree.yview)
        scrollbar.grid(row=1, column=3, sticky='ns')
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        self.load_students()

    def add_student(self):
        name = self.student_name.get()
        if name:
            c.execute("INSERT INTO students (name) VALUES (?)", (name,))
            conn.commit()
            self.load_students()
            self.student_name.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a student name.")
    
    def load_students(self):
        for i in self.student_tree.get_children():
            self.student_tree.delete(i)
        c.execute("SELECT * FROM students")
        for student in c.fetchall():
            self.student_tree.insert('', 'end', values=student)

    def manage_courses(self):
        frame = ttk.Frame(self.tab_courses)
        frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        ttk.Label(frame, text="Course Name").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.course_name = ttk.Entry(frame, width=30)
        self.course_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Add Course", command=self.add_course).grid(row=0, column=2, padx=5, pady=5)
        
        self.course_tree = ttk.Treeview(frame, columns=('ID', 'Name'), show='headings', height=15)
        self.course_tree.heading('ID', text='ID')
        self.course_tree.heading('Name', text='Name')
        self.course_tree.column('ID', width=50)
        self.course_tree.column('Name', width=200)
        self.course_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.course_tree.yview)
        scrollbar.grid(row=1, column=3, sticky='ns')
        self.course_tree.configure(yscrollcommand=scrollbar.set)
        
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        self.load_courses()

    def add_course(self):
        name = self.course_name.get()
        if name:
            c.execute("INSERT INTO courses (name) VALUES (?)", (name,))
            conn.commit()
            self.load_courses()
            self.course_name.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a course name.")
    
    def load_courses(self):
        for i in self.course_tree.get_children():
            self.course_tree.delete(i)
        c.execute("SELECT * FROM courses")
        for course in c.fetchall():
            self.course_tree.insert('', 'end', values=course)

    def assign_courses(self):
        frame = ttk.Frame(self.tab_assignments)
        frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        ttk.Label(frame, text="Select Student").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.assign_student_list = ttk.Combobox(frame, width=30)
        self.assign_student_list.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Select Course").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.assign_course_list = ttk.Combobox(frame, width=30)
        self.assign_course_list.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Assign Course", command=self.assign_course).grid(row=2, column=1, padx=5, pady=10)
        
        self.assignments_tree = ttk.Treeview(frame, columns=('Student', 'Course'), show='headings', height=10)
        self.assignments_tree.heading('Student', text='Student')
        self.assignments_tree.heading('Course', text='Course')
        self.assignments_tree.column('Student', width=200)
        self.assignments_tree.column('Course', width=200)
        self.assignments_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.assignments_tree.yview)
        scrollbar.grid(row=3, column=2, sticky='ns')
        self.assignments_tree.configure(yscrollcommand=scrollbar.set)
        
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        
        self.load_assign_options()
        self.load_assignments()

    def load_assign_options(self):
        c.execute("SELECT * FROM students")
        students = [f"{student[0]} - {student[1]}" for student in c.fetchall()]
        self.assign_student_list['values'] = students
        
        c.execute("SELECT * FROM courses")
        courses = [f"{course[0]} - {course[1]}" for course in c.fetchall()]
        self.assign_course_list['values'] = courses

    def assign_course(self):
        student = self.assign_student_list.get().split(' - ')[0]
        course = self.assign_course_list.get().split(' - ')[0]
        if student and course:
            c.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student, course))
            conn.commit()
            messagebox.showinfo("Success", "Course assigned successfully!")
            self.load_assignments()
        else:
            messagebox.showwarning("Selection Error", "Please select both a student and a course.")

    def load_assignments(self):
        for i in self.assignments_tree.get_children():
            self.assignments_tree.delete(i)
        c.execute("""
            SELECT students.name, courses.name
            FROM student_courses
            JOIN students ON student_courses.student_id = students.id
            JOIN courses ON student_courses.course_id = courses.id
        """)
        for assignment in c.fetchall():
            self.assignments_tree.insert('', 'end', values=assignment)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolApp(root)
    root.mainloop()

# Close the database connection when the program ends
conn.close()