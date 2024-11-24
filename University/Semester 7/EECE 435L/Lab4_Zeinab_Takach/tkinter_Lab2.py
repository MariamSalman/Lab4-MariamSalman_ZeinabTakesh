import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Dict, Any
import json

class Person:
    def __init__(self, name: str, age: int, email: str):
        self.validate_age(age)
        self.validate_email(email)
        self.name = name
        self.age = age
        self.__email = email
        
    def introduce(self) -> str:
        return f"My name is {self.name}, I am {self.age} years old."

    def get_email(self) -> str:
        return self.__email
    
    @staticmethod
    def validate_age(age: int):
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer.")
        
    @staticmethod
    def validate_email(email: str):
        if not isinstance(email, str):
            raise ValueError("Email must be a string.")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "age": self.age,
            "email": self.__email
        }

    used_emails = set() 
    used_ids = set()

class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str):
        if email in Person.used_emails:
            raise ValueError(f"The email {email} already exists.")
        if student_id in Person.used_ids:
            raise ValueError(f"The ID '{student_id}' already exists.")
        Person.used_ids.add(student_id)
        Person.used_emails.add(email)

        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []
    
    def register_course(self, course: 'Course'):
        if course not in self.registered_courses:
            self.registered_courses.append(course)

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "student_id": self.student_id,
            "registered_courses": [course.to_dict() for course in self.registered_courses]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        student = cls(data["name"], data["age"], data["email"], data["student_id"])
        student.registered_courses = [Course.from_dict(c) for c in data.get("registered_courses", [])]
        return student

class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        if email in Person.used_emails:
            raise ValueError(f"The email {email} already exists.")
        if instructor_id in Person.used_ids:
            raise ValueError(f"The ID '{instructor_id}' already exists.")
        
        Person.used_ids.add(instructor_id)
        Person.used_emails.add(email)

        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course: 'Course'):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)

    def get_email(self):
        return self.email
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.to_dict() for course in self.assigned_courses]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        instructor = cls(data["name"], data["age"], data["email"], data["instructor_id"])
        instructor.assigned_courses = [Course.from_dict(c) for c in data.get("assigned_courses", [])]
        return instructor

class Course:
    existing_course_ids: set = set()

    def __init__(self, course_id: str, course_name: str):
        if course_id in Course.existing_course_ids:
            raise ValueError(f"Course ID '{course_id}' already exists.")
        
        self.course_id = course_id
        self.course_name = course_name
        Course.existing_course_ids.add(course_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "course_id": self.course_id,
            "course_name": self.course_name
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data["course_id"], data["course_name"])
    
class SchoolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")

        self.tabs = ttk.Notebook(root)
        self.student_tab = ttk.Frame(self.tabs)
        self.instructor_tab = ttk.Frame(self.tabs)
        self.course_tab = ttk.Frame(self.tabs)
        self.overview_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.student_tab, text='Students')
        self.tabs.add(self.instructor_tab, text='Instructors')
        self.tabs.add(self.course_tab, text='Courses')
        self.tabs.add(self.overview_tab, text='Overview')
        self.tabs.pack(expand=1, fill='both')

        self.students: List[Student] = []
        self.instructors: List[Instructor] = []
        self.courses: List[Course] = []

        self.register_course_dropdown_var = tk.StringVar()
        self.assign_course_dropdown_var = tk.StringVar()

        self.register_course_dropdown = ttk.Combobox(self.student_tab, textvariable=self.register_course_dropdown_var, state="readonly")
        self.assign_course_dropdown = ttk.Combobox(self.instructor_tab, textvariable=self.assign_course_dropdown_var, state="readonly")

        self.init_student_tab()
        self.init_instructor_tab()
        self.init_course_tab()
        self.init_overview_tab()
        self.init_search_in_overview_tab()

    def update_course_dropdown(self):
        course_names = ["None"] + [course.course_name for course in self.courses]
        if self.register_course_dropdown:
            self.register_course_dropdown['values'] = course_names
        if self.assign_course_dropdown:
            self.assign_course_dropdown['values'] = course_names


    def init_course_tab(self):
        course_frame = ttk.Frame(self.course_tab)
        course_frame.pack(pady=10)

        ttk.Label(course_frame, text="Course ID:").grid(row=0, column=0)
        self.course_id_entry = ttk.Entry(course_frame)
        self.course_id_entry.grid(row=0, column=1)

        ttk.Label(course_frame, text="Course Name:").grid(row=1, column=0)
        self.course_name_entry = ttk.Entry(course_frame)
        self.course_name_entry.grid(row=1, column=1)
      
        input_button_frame = ttk.Frame(self.course_tab)
        input_button_frame.pack(fill='x', pady=10)
        ttk.Button(input_button_frame, text="Add Course", command=self.add_course).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(input_button_frame, text="Edit Course", command=self.edit_course).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(input_button_frame, text="Delete Course", command=self.delete_course).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(input_button_frame, text="Save Changes", command=self.add_and_delete_course).grid(row=1, column=3, padx=5, pady=5)

        self.course_tree = ttk.Treeview(self.course_tab, columns=("Course ID", "Course Name"), show='headings')
        self.course_tree.heading("Course ID", text="Course ID")
        self.course_tree.heading("Course Name", text="Course Name")
        self.course_tree.pack(fill='both', expand=True)
        
    def add_and_delete_course(self):
        self.delete_course()
        self.add_course()

    def edit_course(self):
        selected_item = self.course_tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Course", "Please select a course to edit.")
            return
        
        course_id = self.course_tree.item(selected_item)['values'][0]
        course = next((c for c in self.courses if c.course_id == course_id), None)

        self.course_id_entry.delete(0, tk.END)
        self.course_id_entry.insert(0, course.course_id)
        self.course_name_entry.delete(0, tk.END)
        self.course_name_entry.insert(0, course.course_name)

    def delete_course(self):
        selected_item = self.course_tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Course", "Please select a course to delete.")
            return
        course_id = self.course_tree.item(selected_item)['values'][0]
        
        self.courses = [c for c in self.courses if c.course_id != course_id]
        
        self.course_tree.delete(selected_item)

    def register_course(self):
        selected_course_name = self.register_course_dropdown_var.get()
        selected_course = next((c for c in self.courses if c.course_name == selected_course_name), None)

        if selected_course is not None:
            selected_student_id = self.student_id_entry.get()
            student = next((s for s in self.students if s.student_id == selected_student_id), None)
            if student:
                student.register_course(selected_course)
                messagebox.showinfo("Success", f"Registered {student.name} for {selected_course.course_name}!")
            else:
                messagebox.showerror("Error", "Student not found.")
        else:
            messagebox.showerror("Error", "No course selected.")

    def assign_course(self):
        selected_course_name = self.assign_course_dropdown_var.get()
        selected_course = next((c for c in self.courses if c.course_name == selected_course_name), None)

        if selected_course is not None:
            selected_instructor_id = self.instructor_id_entry.get()
            instructor = next((i for i in self.instructors if i.instructor_id == selected_instructor_id), None)
            if instructor:
                instructor.assign_course(selected_course)
                messagebox.showinfo("Success", f"Assigned {selected_course.course_name} to {instructor.name}!")
            else:
                messagebox.showerror("Error", "Instructor not found.")
        else:
            messagebox.showerror("Error", "No course selected.")

    def init_student_tab(self):
        student_frame = ttk.Frame(self.student_tab)
        student_frame.pack(pady=(10))

        ttk.Label(student_frame, text="Name:").pack(side=tk.LEFT)
        self.student_name_entry = ttk.Entry(student_frame, width=15)  # Adjusted width for smaller box
        self.student_name_entry.pack(side=tk.LEFT)

        ttk.Label(student_frame, text="Age:").pack(side=tk.LEFT)
        self.student_age_entry = ttk.Entry(student_frame, width=5)  # Smaller box for age
        self.student_age_entry.pack(side=tk.LEFT)

        ttk.Label(student_frame, text="Email:").pack(side=tk.LEFT)
        self.student_email_entry = ttk.Entry(student_frame, width=15)  # Adjusted width for smaller box
        self.student_email_entry.pack(side=tk.LEFT)

        ttk.Label(student_frame, text="Student ID:").pack(side=tk.LEFT)
        self.student_id_entry = ttk.Entry(student_frame, width=15)  # Adjusted width for smaller box
        self.student_id_entry.pack(side=tk.LEFT)

        course_frame = ttk.Frame(self.student_tab)
        course_frame.pack(pady=(5, 10))  

        ttk.Label(course_frame, text="Select Course to Register:").pack(side=tk.LEFT)
        self.register_course_dropdown.pack(side=tk.TOP)  # Place dropdown beside label

        add_button_frame = ttk.Frame(self.student_tab)
        add_button_frame.pack()
        ttk.Button(add_button_frame, text="Add Student", command=self.add_student, width=15).pack(side=tk.LEFT)

        self.student_tree = ttk.Treeview(self.student_tab, columns=("ID", "Name", "Age", "Email"), show='headings')
        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Age", text="Age")
        self.student_tree.heading("Email", text="Email")
        self.student_tree.pack(fill='both', expand=True)

        self.update_course_dropdown()
        if self.courses:
            self.register_course_dropdown.current("None")  # Set current to "None" if no courses are selected

    def init_instructor_tab(self):
        instructor_frame = ttk.Frame(self.instructor_tab)
        instructor_frame.pack(pady=10)

        ttk.Label(instructor_frame, text="Name:").pack(side=tk.LEFT)
        self.instructor_name_entry = ttk.Entry(instructor_frame, width=15)
        self.instructor_name_entry.pack(side=tk.LEFT)

        ttk.Label(instructor_frame, text="Age:").pack(side=tk.LEFT)
        self.instructor_age_entry = ttk.Entry(instructor_frame, width=5)
        self.instructor_age_entry.pack(side=tk.LEFT)

        ttk.Label(instructor_frame, text="Email:").pack(side=tk.LEFT)
        self.instructor_email_entry = ttk.Entry(instructor_frame, width=15)
        self.instructor_email_entry.pack(side=tk.LEFT)

        ttk.Label(instructor_frame, text="Instructor ID:").pack(side=tk.LEFT)
        self.instructor_id_entry = ttk.Entry(instructor_frame, width=15)
        self.instructor_id_entry.pack(side=tk.LEFT)

        course_assign_frame = ttk.Frame(self.instructor_tab)
        course_assign_frame.pack(pady=(5, 10)) 

        ttk.Label(course_assign_frame, text="Select Course to Assign:").pack(side=tk.LEFT)
        self.assign_course_dropdown.pack(side=tk.TOP)  

        add_instructor_button_frame = ttk.Frame(self.instructor_tab)
        add_instructor_button_frame.pack()
        ttk.Button(add_instructor_button_frame, text="Add Instructor", command=self.add_instructor, width=15).pack(side=tk.LEFT)

        # Treeview for instructors
        self.instructor_tree = ttk.Treeview(self.instructor_tab, columns=("ID", "Name", "Age", "Email"), show='headings')
        self.instructor_tree.heading("ID", text="ID")
        self.instructor_tree.heading("Name", text="Name")
        self.instructor_tree.heading("Age", text="Age")
        self.instructor_tree.heading("Email", text="Email")
        self.instructor_tree.pack(fill='both', expand=True)

        # Update the dropdown with course list
        self.update_course_dropdown()
        if self.courses:
            self.assign_course_dropdown.current(0)  # Set current to the first course if available

    def add_student(self):
        name = self.student_name_entry.get()
        age = int(self.student_age_entry.get())
        email = self.student_email_entry.get()
        student_id = self.student_id_entry.get()

        try:
            student = Student(name, age, email, student_id)
            self.students.append(student)
            self.student_tree.insert("", "end", values=(student_id, name, age, email))
            self.clear_student_entries()
            
            # Automatically register the selected course
            selected_course_name = self.register_course_dropdown_var.get()
            selected_course = next((c for c in self.courses if c.course_name == selected_course_name), None)

            if selected_course is not None:
                student.register_course(selected_course)
                messagebox.showinfo("Success", f"Registered {student.name} for {selected_course.course_name}!")

            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_instructor(self):
        name = self.instructor_name_entry.get()
        age = int(self.instructor_age_entry.get())
        email = self.instructor_email_entry.get()
        instructor_id = self.instructor_id_entry.get()

        try:
            instructor = Instructor(name, age, email, instructor_id)
            self.instructors.append(instructor)
            self.instructor_tree.insert("", "end", values=(instructor_id, name, age, email))
            self.clear_instructor_entries()

            # Automatically assign the selected course
            selected_course_name = self.assign_course_dropdown_var.get()
            selected_course = next((c for c in self.courses if c.course_name == selected_course_name), None)

            if selected_course is not None:
                instructor.assign_course(selected_course)
                messagebox.showinfo("Success", f"Assigned {selected_course.course_name} to {instructor.name}!")

            messagebox.showinfo("Success", "Instructor added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_course(self):
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()

        try:
            course = Course(course_id, course_name)
            self.courses.append(course)
            self.course_tree.insert("", "end", values=(course_id, course_name))
            self.clear_course_entries()
            self.update_course_dropdown()  # Update dropdowns after adding a course
            messagebox.showinfo("Success", "Course added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_student_entries(self):
        self.student_name_entry.delete(0, tk.END)
        self.student_age_entry.delete(0, tk.END)
        self.student_email_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)

    def clear_instructor_entries(self):
        self.instructor_name_entry.delete(0, tk.END)
        self.instructor_age_entry.delete(0, tk.END)
        self.instructor_email_entry.delete(0, tk.END)
        self.instructor_id_entry.delete(0, tk.END)

    def clear_course_entries(self):
        self.course_id_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)

    def update_course_dropdown(self):
        # Update the course dropdowns with the latest course names
        course_names = ["None"] + [course.course_name for course in self.courses]
        self.register_course_dropdown['values'] = course_names
        self.assign_course_dropdown['values'] = course_names
        
    def init_search_in_overview_tab(self):
        search_frame = ttk.Frame(self.overview_tab)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT)

        ttk.Button(search_frame, text="Search", command=self.search_records).pack(side=tk.LEFT)

    def search_records(self):
        query = self.search_entry.get().strip().lower()
        
        filtered_students = [
            student for student in self.students 
            if query in student.name.lower() or query in student.student_id.lower()
        ]
        filtered_instructors = [
            instructor for instructor in self.instructors 
            if query in instructor.name.lower() or query in instructor.instructor_id.lower()
        ]
        filtered_courses = [
            course for course in self.courses 
            if query in course.course_name.lower()
        ]

        self.students_text.delete(1.0, tk.END)
        self.students_text.insert(tk.END, "Students:\n")
        for student in filtered_students:
            self.students_text.insert(tk.END, str(student.to_dict()) + '\n')

        self.instructors_text.delete(1.0, tk.END)
        self.instructors_text.insert(tk.END, "Instructors:\n")
        for instructor in filtered_instructors:
            self.instructors_text.insert(tk.END, str(instructor.to_dict()) + '\n')

        self.courses_text.delete(1.0, tk.END)
        self.courses_text.insert(tk.END, "Courses:\n")
        for course in filtered_courses:
            self.courses_text.insert(tk.END, str(course.to_dict()) + '\n')
    import json

    def save_data(self):
        """Save all the data (students, instructors, courses) to a JSON file."""
        try:
            data = {
                "students": [student.to_dict() for student in self.students],
                "instructors": [instructor.to_dict() for instructor in self.instructors],
                "courses": [course.to_dict() for course in self.courses]
            }

            with open('school_data.json', 'w') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_data(self):
        """Load data from the JSON file and populate the app."""
        try:
            with open('school_data.json', 'r') as file:
                data = json.load(file)
            self.students = [Student.from_dict(student_data) for student_data in data.get("students", [])]
            self.instructors = [Instructor.from_dict(instructor_data) for instructor_data in data.get("instructors", [])]
            self.courses = [Course.from_dict(course_data) for course_data in data.get("courses", [])]

            self.refresh_overview()

            self.update_course_dropdown()

            messagebox.showinfo("Success", "Data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def refresh_overview(self):
        """Refresh overview section."""
        self.students_text.delete(1.0, tk.END)
        self.students_text.insert(tk.END, "Students:\n")
        for student in self.students:
            self.students_text.insert(tk.END, str(student.to_dict()) + '\n')

        self.instructors_text.delete(1.0, tk.END)
        self.instructors_text.insert(tk.END, "Instructors:\n")
        for instructor in self.instructors:
            self.instructors_text.insert(tk.END, str(instructor.to_dict()) + '\n')

        self.courses_text.delete(1.0, tk.END)
        self.courses_text.insert(tk.END, "Courses:\n")
        for course in self.courses:
            self.courses_text.insert(tk.END, str(course.to_dict()) + '\n')

    def init_overview_tab(self):
        """Initialize Overview Tab with buttons for saving and loading."""
        overview_frame = ttk.Frame(self.overview_tab)
        overview_frame.pack(pady=10)

        overview_frame = ttk.Frame(self.overview_tab)
        overview_frame.pack(pady=10)

        self.students_text = tk.Text(overview_frame, wrap='word', height=10)
        self.students_text.pack(fill='both', expand=True, padx=10, pady=5)
        ttk.Label(overview_frame, text="Students").pack() 
        self.students_text.pack(fill='both', expand=True)
        self.instructors_text = tk.Text(overview_frame, wrap='word', height=10)
        self.instructors_text.pack(fill='both', expand=True, padx=10, pady=5)
        ttk.Label(overview_frame, text="Instructors").pack() 
        self.instructors_text.pack(fill='both', expand=True)
        self.courses_text = tk.Text(overview_frame, wrap='word', height=10)
        self.courses_text.pack(fill='both', expand=True, padx=10, pady=5)
        ttk.Label(overview_frame, text="Courses").pack()  
        self.courses_text.pack(fill='both', expand=True)
        ttk.Button(overview_frame, text="Refresh Overview", command=self.refresh_overview).pack(side="left", padx=10, pady=10)
        ttk.Button(overview_frame, text="Save Data", command=self.save_data).pack(side="left", padx=5, pady=5)
        ttk.Button(overview_frame, text="Load Data", command=self.load_data).pack(side="left", padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()