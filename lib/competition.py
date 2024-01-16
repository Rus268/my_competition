"""
Competition class to store the competition data and process the data 

"""
import sys
from student import Student
from challenge import Challenge

class Competition():
    """ Competition class to store the competition data and process the data
    
    Attributes:
        results (list): A list of results
        challenges (list): A list of challenges
        students (list): A list of students
    """
    def __init__(self):
        self.__results = []
        self.__challenges = []
        self.__students = []
    def __str__(self):
        return "Competition object"
    
    @property
    def results(self):
        """Return a list of results with the latest result at beginning of the list [index 0]]"""
        return self.__results
    
    @property
    def challenges(self):
        """Return a list of challenges"""
        return self.__challenges
    
    @property
    def students(self):
        """Return a list of students"""
        return self.__students
    
    @staticmethod
    def resuls_table_process(value):
        """Process the value in the result table to ensure it is in the correct format."""
        value = value.strip() # Remove the leading and trailing whitespace
        if value == "":
            return "Results"
        if value in '-1':
            return ''
        if value.isdigit():
            return float(value)
        if value in ["444", 'TBA', 'tba']:
            return "--"
        return value

    def read_results(self, result_file: str) -> None:
        """
        Read the results from the given file and save it to the results attribute.

        Input:
        - result_file (str): The path to the file to read.
          If None, use the value of the result_file attribute.
        """
        result_array = []  # Define result_array variable
        # open the file with explicit encoding
        with open(result_file, "r", encoding="utf-8") as file:
            # read the rest of the file
            for line in file:
                row = []
                cells = line.strip().split(",")
                for cell in cells:
                    cell = self.resuls_table_process(cell)  # Define self variable
                    row.append(cell)
                result_array.append(row)
        self.__results.insert(0, result_array)  # Define self variable
    
    def display_results(self):
        """
        Display the latest results in a table.
        """
        table = self.results[0] # Get the latest result
        # Replace None values with an empty string
        table = [[col if col is not None else '' for col in row] for row in table]
        widths = [max(map(len, str(col))) for col in zip(*table)]
        row_template = '|'.join(f"{{:{width}}}" for width in widths)
        no_student = len(table) - 1
        no_challenge = len(table[0]) - 1
        fastest_student, fastest_time = self.show_fastest_student()
        # Print header
        print("COMPETITION DASHBOARD")
        print('+'.join('-'*(w + 2) for w in widths))
        print(row_template.format(*table[0], *widths))
        print('+'.join('-'*(w + 2) for w in widths))
        # Print table content
        for row in table[1:]:
            print(row_template.format(*row, *widths))
        print('+'.join('-'*(w + 2) for w in widths))
        print(f'There are {no_student} students and {no_challenge} challenges')
        print(f'The top student is {fastest_student} with an average time of {fastest_time} minutes')
    
    def read_students(self, file):
        """
        Read the students from the given file and save it to the students attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the students attribute.
        
        """
        with open(file, "r", encoding="utf-8") as file:
            # read the rest of the file
            for line in file:
                elements = [item.strip() for item in line.strip().split(",")]
                if len(elements) == 3:
                    print(elements)
                    student = Student.new_student(elements[2], elements[0], elements[1])
                    self.__students.append(student)
                else:
                    raise ValueError("Invalid student record")
    
    def find_student(self, student_id:students):
        """
        Find the student with the given ID.

        Input:
        - student_id (str): The ID of the student to find.

        Returns:
        - Student: The student object with the given ID.
        """
        for student in self.students:
            if student.id == student_id:
                return student
        return None
    
    def show_fastest_student(self) -> tuple:
        """
        Display the fastest student in the competition with their average time.

        Returns:
        - tuple: A tuple containing the fastest student object and their average time.
        """
        fastest_student = None
        fatest_average_time = 0
        # Since the latest result is alway the top of the list, we can access index 0 to get the latest result
        current_result = self.results[0]
        # Loop through the result to find the fastest student
        for i in range(1, len(current_result)): # Skip the first element because it is the header
            student_result = current_result[i]
            # Loop through the student result to find the fastest student
            average_time = 0
            valid_result = 0 # Count the number of valid result
            for j in range(1, len(student_result)): # Skip the first element because it is the student ID
                if not student_result[j] in ['--', '', None] :
                    average_time += float(student_result[j])
                    valid_result += 1
            # Calculate the average time
            if valid_result == 0:
                average_time = average_time / (len(student_result) - 1)
            # Check if the current student is the fastest student
                if average_time > fatest_average_time:
                    fatest_average_time = average_time
                fastest_student = student_result[0]
        # Return the fastest student and their average time
        return fastest_student, round(fatest_average_time)
            
    def read_challenge(self, file):
        """
        Read the challenges from the given file and save it to the challenges attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the challenges attribute.
        
        """
        with open(file, "r", encoding="utf-8") as file:
            for line in file:
                elements = [item.strip() for item in line.strip().split(",")]
                if len(elements) == 4:
                    challenge = Challenge(elements[0], elements[1], elements[2], elements[3])
                    self.__challenges.append(challenge)
                else:
                    raise ValueError("Invalid challenge record")
    
    def find_challenge(self, challenge_id):
        """
        Find the challenge with the given ID.

        Input:
        - challenge_id (str): The ID of the challenge to find.

        Returns:
        - Challenge: The challenge object with the given ID.
        """
        for challenge in self.__challenges:
            if challenge.id == challenge_id:
                return challenge
        return None
                
    def read_all(self, studen_file, result_file, challenge_file):
        """
        Read all the data from the given files and save it to the appropriate attributes.

        Input:
        - studen_file (str): The path to the file to read. If None exit the program and print the error message.
        - result_file (str): The path to the file to read. If None exit the progra and print the error message.
        - challenge_file (str): The path to the file to read. If None exit the program and print the error message.
        
        """
        if studen_file is None:
            sys.exit('No students are available for the competition')
        self.read_students(studen_file)
        if result_file is None:
            sys.exit('No results are available for the competition')
        self.read_results(result_file)
        if challenge_file is None:
            sys.exit('No challenges are available for the competition')
        self.read_challenges(challenge_file)
        
    def read_challenges(self, file):
        """
        Read the challenges from the given file and save it to the challenges attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the challenges attribute.
        
        """
        if file is None:
            sys.exit('No challenges are available for the competition')
        with open(file, "r", encoding="utf-8") as file:
            for line in file:
                elements = [item.strip() for item in line.strip().split(",")]
                if len(elements) == 4:
                    challenge = Challenge(elements[0], elements[1], elements[2], elements[3])
                    self.__challenges.append(challenge)
                else:
                    raise ValueError("Invalid challenge record")
    def display_challenges(self):
        """
        Display the challenges in the challenges attribute.
        """
        pass


    @staticmethod
    def read_command_line():
        """
        This function will read the command line and return the result file, student file and challenge file.
        """
        if len(sys.argv) == 2:
            return sys.argv[1], None, None
        elif len(sys.argv) == 3:
            return sys.argv[1], sys.argv[2], None
        elif len(sys.argv) == 4:
            return sys.argv[1], sys.argv[2], sys.argv[3]
        else:
            print()
            print('[Usage:] python my_competition.py <result file> <student file> <challenge file>')
            print('<result file> is required, <student file> and <challenge file> are optional')
            sys.exit(0)

if __name__ == "__main__":
    # test code
    competition = Competition()
    files = competition.read_command_line()
    competition.read_results(files[0])
    competition.read_students(files[1])
    print(competition.results[0])
    print(competition.show_fastest_student())
    competition.display_results()
    