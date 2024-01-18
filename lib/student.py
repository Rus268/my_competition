"""
Student class and its subclasses.
"""

from .result import Result
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
        self.__challenges = []

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
        self.__type = new_type
    
    @property
    def challenges(self):
        """
        Returns the challenges of the student.
        """
        return self.__challenges
    
    def add_challenges(self, new_challenge: Challenge):
        """Add a new challenge to the student"""
        self.__challenges.append(new_challenge)
    
    def remove_challenges(self, challenge):
        """Remove a challenge from the student"""
        self.__challenges.remove(challenge)
    
    def meets_requirements(self):
        """Check if the student meets the requirements for the competition"""
        pass


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
    
    def meets_requirements(self):
        """Check if the student meets the requirements for the competition as a Undergraduate student"""
        special_challenge_count = 0
        mandatory_challenge_count = 0
        total_challenge_count = len(self.challenges)
        for challenge in self.challenges:
            if challenge.type == 'M':
                mandatory_challenge_count += 1
            elif challenge.type == 'S':
                special_challenge_count += 1
        if special_challenge_count >= 1 and (total_challenge_count - special_challenge_count) == mandatory_challenge_count:
            return True
        return False

class Postgraduate(Student):
    """
    A subclass of Student representing a postgraduate student.
    """
    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        # Modify the type attribute of the object
        self.type = 'P'

    def meets_requirements(self):
        """Check if the student meets the requirements for the competition as a Pndergraduate student"""
        special_challenge_count = 0
        mandatory_challenge_count = 0
        total_challenge_count = len(self.challenges)
        for challenge in self.challenges:
            if challenge.type == 'M':
                mandatory_challenge_count += 1
            elif challenge.type == 'S':
                special_challenge_count += 1
        if special_challenge_count >= 2 and (total_challenge_count - special_challenge_count) == mandatory_challenge_count:
            return True
        return False


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
        if student_type == 'U' and student_id.startswith('S'):
            return Undergraduate(student_id, name)
        elif student_type == 'P' and student_id.startswith('S'):
            return Postgraduate(student_id, name)
        else:
            raise ValueError("Invalid student type or ID")

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
                elements = [item.strip() for item in line.strip().split(",")]
                if len(elements) == 3:
                    student = StudentFactory.new_student(elements[0], elements[1], elements[2])
                    self.add_student(student)
                else:
                    raise ValueError("Invalid student record")

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
