class Student():
    """
    A class representing a student.

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
        self.__type = new_type

    def __str__(self):
        return f"{self.id}, {self.type}, {self.name}" # return a string representation of the object

    @staticmethod
    def new_student(student_type, student_id, name):
        """
        Create a new student object based on the given student type.

        Inpute:
            student_type (str): The type of the student ('U' for Undergraduate, 'P' for Postgraduate).
            student_id (str): The ID of the student. Must start with 'S'.
            name (str): The name of the student.

        Returns:
            Student: A new student object of the appropriate type.

        """
        if student_type == 'U' and student_id.startswith('S'):
            return Undergraduate(student_id, name)
        elif student_type == 'P' and student_id.startswith('S'):
            return Postgraduate(student_id, name)
        else:
            raise ValueError("Invalid student type or ID")

class Undergraduate(Student):

    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        # Modify the type attribute of the object
        self.type = 'U'

class Postgraduate(Student):
    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        # Modify the type attribute of the object
        self.type = 'P'

def main():
    pass

if __name__ == "__main__":
    main()
