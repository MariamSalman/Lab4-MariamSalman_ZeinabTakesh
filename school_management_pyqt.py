import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, QLabel,
    QGroupBox, QStackedWidget, QMainWindow
)
from school_management_system import SchoolManagementSystem, Student, Instructor, Course

class SchoolManagementApp(QMainWindow):
    """
    The main application class for the School Management System GUI.

    This class initializes the main window for the application and sets up navigation
    between different pages (Student, Instructor, Course, Display & Registration) for
    managing and displaying school records.

    :param QMainWindow: Inherits from QMainWindow to create the main application window
    """

    def __init__(self):
        """
        Initializes the SchoolManagementApp with all required widgets, layouts,
        and navigation buttons.

        Creates pages for managing students, instructors, courses, and viewing records.
        """
        super().__init__()
        self.system = SchoolManagementSystem()
        self.setWindowTitle('School Management System')
        self.setGeometry(100, 100, 800, 600)
        
        # Central Widget and Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Stacked Widget for Pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Navigation Buttons
        nav_layout = QHBoxLayout()
        main_layout.addLayout(nav_layout)

        self.page1_button = QPushButton("Student")
        self.page1_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        nav_layout.addWidget(self.page1_button)

        self.page2_button = QPushButton("Instructor")
        self.page2_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        nav_layout.addWidget(self.page2_button)

        self.page3_button = QPushButton("Course")
        self.page3_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        nav_layout.addWidget(self.page3_button)

        self.page4_button = QPushButton("Display & Registration")
        self.page4_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        nav_layout.addWidget(self.page4_button)

        # Initialize Pages
        self.init_page1()
        self.init_page2()
        self.init_page3()
        self.init_page4()

    def init_page1(self):
        """
        Initializes the student management page with fields for entering student details.

        This page includes input fields for student name, age, email, and ID, as well
        as a button to add the student to the system.
        """
        page1 = QWidget()
        layout = QVBoxLayout(page1)

        student_group = QGroupBox("Student Details")
        student_layout = QFormLayout()
        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        self.student_id_input = QLineEdit()
        student_layout.addRow("Student Name:", self.student_name_input)
        student_layout.addRow("Student Age:", self.student_age_input)
        student_layout.addRow("Student Email:", self.student_email_input)
        student_layout.addRow("Student ID:", self.student_id_input)
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        student_layout.addRow(self.add_student_button)
        student_group.setLayout(student_layout)
        layout.addWidget(student_group)

        self.stacked_widget.addWidget(page1)

    def init_page2(self):
        """
        Initializes the instructor management page with fields for entering instructor details.

        This page includes input fields for instructor name, age, email, and ID, as well
        as a button to add the instructor to the system.
        """
        page2 = QWidget()
        layout = QVBoxLayout(page2)

        instructor_group = QGroupBox("Instructor Details")
        instructor_layout = QFormLayout()
        self.instructor_name_input = QLineEdit()
        self.instructor_age_input = QLineEdit()
        self.instructor_email_input = QLineEdit()
        self.instructor_id_input = QLineEdit()
        instructor_layout.addRow("Instructor Name:", self.instructor_name_input)
        instructor_layout.addRow("Instructor Age:", self.instructor_age_input)
        instructor_layout.addRow("Instructor Email:", self.instructor_email_input)
        instructor_layout.addRow("Instructor ID:", self.instructor_id_input)
        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        instructor_layout.addRow(self.add_instructor_button)
        instructor_group.setLayout(instructor_layout)
        layout.addWidget(instructor_group)

        self.stacked_widget.addWidget(page2)

    def init_page3(self):
        """
        Initializes the course management page with fields for entering course details.

        This page includes input fields for course ID and course name, as well
        as a button to add the course to the system.
        """
        page3 = QWidget()
        layout = QVBoxLayout(page3)

        course_group = QGroupBox("Course Details")
        course_layout = QFormLayout()
        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()
        course_layout.addRow("Course ID:", self.course_id_input)
        course_layout.addRow("Course Name:", self.course_name_input)
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        course_layout.addRow(self.add_course_button)
        course_group.setLayout(course_layout)
        layout.addWidget(course_group)

        self.stacked_widget.addWidget(page3)

    def init_page4(self):
        """
        Initializes the display and registration page, allowing for course registration
        and displaying all records.

        This page includes drop-down selections for student and course registration,
        and displays all entries in a table format.
        """
        page4 = QWidget()
        layout = QVBoxLayout(page4)

        # Registration and Assignment Section
        self.student_course_combo = QComboBox()
        self.instructor_course_combo = QComboBox()
        self.register_button = QPushButton("Register for Course")
        self.register_button.clicked.connect(self.register_course)
        self.assign_button = QPushButton("Assign Course to Instructor")
        self.assign_button.clicked.connect(self.assign_course)

        registration_layout = QHBoxLayout()
        registration_layout.addWidget(QLabel("Select Course for Student:"))
        registration_layout.addWidget(self.student_course_combo)
        registration_layout.addWidget(self.register_button)

        assignment_layout = QHBoxLayout()
        assignment_layout.addWidget(QLabel("Select Course for Instructor:"))
        assignment_layout.addWidget(self.instructor_course_combo)
        assignment_layout.addWidget(self.assign_button)

        layout.addLayout(registration_layout)
        layout.addLayout(assignment_layout)

        # Display Table Section
        self.display_button = QPushButton("Display All")
        self.display_button.clicked.connect(self.display_all)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Role", "ID", "Additional Info"])

        layout.addWidget(self.display_button)
        layout.addWidget(self.table)

        self.stacked_widget.addWidget(page4)

    def add_student(self):
        """
        Adds a new student to the system based on input fields.

        Validates input fields and, if successful, adds a student to the system and
        provides user feedback via a message box.
        """
        name = self.student_name_input.text()
        age = self.student_age_input.text()
        email = self.student_email_input.text()
        student_id = self.student_id_input.text()

        if name and age.isdigit() and email and student_id:
            student = Student(name, int(age), email, student_id)
            self.system.add_student(student)
            self.student_course_combo.addItem(student_id)
            QMessageBox.information(self, "Success", "Student added successfully!")
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields with valid data.")

    def add_instructor(self):
        """
        Adds a new instructor to the system based on input fields.

        Validates input fields and, if successful, adds an instructor to the system and
        provides user feedback via a message box.
        """
        name = self.instructor_name_input.text()
        age = self.instructor_age_input.text()
        email = self.instructor_email_input.text()
        instructor_id = self.instructor_id_input.text()

        if name and age.isdigit() and email and instructor_id:
            instructor = Instructor(name, int(age), email, instructor_id)
            self.system.add_instructor(instructor)
            self.instructor_course_combo.addItem(instructor_id)
            QMessageBox.information(self, "Success", "Instructor added successfully!")
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields with valid data.")

    def add_course(self):
        """
        Adds a new course to the system based on input fields.

        Validates input fields and, if successful, adds a course to the system and
        provides user feedback via a message box.
        """
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()

        if course_id and course_name:
            course = Course(course_id, course_name)
            self.system.add_course(course)
            QMessageBox.information(self, "Success", "Course added successfully!")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid course information.")

    def register_course(self):
        """
        Registers a student for a course based on the selected items in the combo boxes.

        Uses the student and course IDs from the combo boxes, retrieves the corresponding
        objects, and registers the student for the course. Provides user feedback via a message box.
        """
        student_id = self.student_course_combo.currentText()
        course_id = self.student_course_combo.currentText()
        
        student = self.system.get_student(student_id)
        course = self.system.get_course(course_id)
        
        if student and course:
            course.add_student(student)
            QMessageBox.information(self, "Success", f"Student {student_id} registered for course {course_id}!")

    def assign_course(self):
        """
        Assigns a course to an instructor based on the selected items in the combo boxes.

        Uses the instructor and course IDs from the combo boxes, retrieves the corresponding
        objects, and assigns the instructor to the course. Provides user feedback via a message box.
        """
        instructor_id = self.instructor_course_combo.currentText()
        course_id = self.instructor_course_combo.currentText()
        
        instructor = self.system.get_instructor(instructor_id)
        course = self.system.get_course(course_id)
        
        if instructor and course:
            course.assign_instructor(instructor)
            QMessageBox.information(self, "Success", f"Instructor {instructor_id} assigned to course {course_id}!")

    def display_all(self):
        """
        Displays all students, instructors, and courses in the system in a table.

        Clears the table and inserts rows for each student, instructor, and course
        currently in the system, including relevant information.
        """
        self.table.setRowCount(0)
        for student in self.system.get_all_students():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(student.name))
            self.table.setItem(row_position, 1, QTableWidgetItem("Student"))
            self.table.setItem(row_position, 2, QTableWidgetItem(student.student_id))
            self.table.setItem(row_position, 3, QTableWidgetItem(",".join([course.course_name for course in student.registered_courses])))

        for instructor in self.system.get_all_instructors():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(instructor.name))
            self.table.setItem(row_position, 1, QTableWidgetItem("Instructor"))
            self.table.setItem(row_position, 2, QTableWidgetItem(instructor.instructor_id))
            self.table.setItem(row_position, 3, QTableWidgetItem(",".join([course.course_name for course in instructor.assigned_courses])))

        for course in self.system.get_all_courses():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(course.course_name))
            self.table.setItem(row_position, 1, QTableWidgetItem("Course"))
            self.table.setItem(row_position, 2, QTableWidgetItem(course.course_id))
            instructor_name = course.instructor.name if course.instructor else "None"
            self.table.setItem(row_position, 3, QTableWidgetItem(f"Instructor: {instructor_name}"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())
