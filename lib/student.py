"""
Student class and its subclasses.
"""

from .challenge import Challenge

class Student():
    """
    A base class representing a student.

    Attributes:
        id (str): The ID of the student. Must start with 'S'.
        name (str): The name of the student.
        type (str): The type of the student (default as 'None', 'U' for Undergraduate, 'P' for Postgraduate).
    """
    def __init__(self, student_id, name):
        self.__id = student_id
        self.__name = name
        self.__type = None

    @property
    def id(self):
        """
        Returns the ID of the student.
        """
        return self.__id

    @id.setter
    def id(self, new_id):
        if not new_id.startswith('S'):
            raise ValueError("Invalid student ID. Must start with 'S'")
        self.__id = str(new_id)

    @property
    def name(self):
        """
        Returns the name of the student.
        """
        return self.__name

    @name.setter
    def name(self, new_name:str):
        self.__name = str(new_name)

    @property
    def type(self):
        """
        Returns the type of the student.
        """
        if self.__type is None:
            return " "
        return self.__type
    @type.setter
    def type(self, new_type):
        if new_type not in ['U', 'P']:
            raise ValueError("Invalid student type")
        self.__type = new_type


    def meets_requirements(self, result_dict: dict) -> bool:
        """Use the participation with type dictionary from competition class to check if the student meets the requirements for the competition as an undergraduate student
        
        Input:
        
        - result_dict (dict): {student_id: (participation_type, participation_status)}
        
        Returns:
        - bool (True or False): True if the student meets the requirements, False if not
        """
        if self.type == 'U':
            min_special_challenge = 1
        elif self.type == 'P':
            min_special_challenge = 2
        else:
            raise ValueError("Invalid student type")
        meet_min_special = False
        complete_all_mandatory = True  # Assume all mandatory challenges are completed until proven otherwise
        special_challenge_count = 0
        for participation_status in result_dict.values():
            if participation_status[0] == 'M':
                if participation_status[1] != 1:  # If a mandatory challenge is not completed, set complete_all_mandatory to False
                    complete_all_mandatory = False
                    break
            if participation_status[0] == 'S' and participation_status[1] == 1:  # Only count completed special challenges
                special_challenge_count += 1
        if special_challenge_count >= min_special_challenge:
            meet_min_special = True
        if meet_min_special and complete_all_mandatory:
            return True
        return False

    def __str__(self):
        return f"{self.id} ({self.name})" # return a string representation of the object

class Undergraduate(Student):
    """
    A subclass of Student representing an undergraduate student.
    """
    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        # Modify the type attribute of the object
        self.type = 'U'


class Postgraduate(Student):
    """
    A subclass of Student representing a postgraduate student.
    """
    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        # Modify the type attribute of the object
        self.type = 'P'

class StudentFactory():
    """
    A factory class for creating new student objects.
    """
    @staticmethod
    def new_student(student_id, name, student_type) -> Student:
        """
        Create a new student object based on the given student type.

        Inpute:
            student_type (str): The type of the student ('U' for Undergraduate, 'P' for Postgraduate).
            student_id (str): The ID of the student. Must start with 'S'.
            name (str): The name of the student.

        Returns:
            Student: A new student object of the appropriate type. Can be either Undergraduate or Postgraduate.

        """
        if not student_id.startswith('S'):
            raise ValueError("Invalid student ID. Must start with 'S'")
        if student_type == 'U':
            return Undergraduate(student_id, name)
        elif student_type == 'P':
            return Postgraduate(student_id, name)
        else:
            raise ValueError("Invalid student type")

class StudentManager():
    """
    A class for managing students.
    """
    def __init__(self):
        self.__students = [] # A list of student objects
    
    @property
    def students(self) -> list:
        """
        Returns the students attribute.
        """
        return self.__students
    
    @students.setter
    def students(self, new_student):
        self.__students = new_student
    
    def add_student(self, new_student):
        """
        Adds a new student to the list of students.

        Parameters:
        - new_student: The student object to be added.

        Returns:
        None
        """
        self.__students.append(new_student)
    
    def remove_student(self, student_id):
        """
        Remove a student from the students attribute.
        
        Input:
            student_id (str): The ID of the student to remove.
        """
        for student in self.__students:
            if student.id == student_id:
                self.__students.remove(student)
                return True
        return False
    
    def get_student(self, student_id) -> Student:
        """
        Get a student from the students attribute.

        Input:
            student_id (str): The ID of the student to get.
        
        Returns:
            Student: The student object with the given ID. None if not found.
        """
        for student in self.__students:
            if student.id == student_id:
                return student
        return None
    
    def read_student_file(self, file_name):
        """
        Read the students from the given file and save it to the students attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the students attribute.
        
        """
        if file_name is None:
            raise ValueError(f"Missing student file name {file_name}")
        with open(file_name, "r", encoding="utf-8") as file:
            # read the rest of the file
            for line in file:
                if ',' not in line:
                    raise ValueError("Student record must be separated by comma")
                elements = [item.strip() for item in line.strip().split(",")]
                if len(elements) == 3:
                    student = StudentFactory.new_student(elements[0], elements[1], elements[2])
                    self.add_student(student)
                else:
                    raise ValueError("Unexpected number of elements in student record or record is not separated by comma")
                

if __name__ == "__main__":
    # Test code
    student_manager = StudentManager()
    undergrad = StudentFactory.new_student("S2", 'U', "Mary")
    postgrad = StudentFactory.new_student("S3","P", "Peter")
    student_manager.add_student(undergrad)
    student_manager.add_student(postgrad)
    print(student_manager.get_student("S1"))
    print(undergrad)
    print(postgrad)
    print(student_manager.students)  # Print all students
