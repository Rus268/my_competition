"""
Competition class to store the competition data and process the data 

"""
import sys
from lib.student import StudentManager
from lib.challenge import ChallengeManager
from lib.misc import Table, TextEditor

class Competition():
    """ Competition class to store the competition data and process the data
    
    Attributes:
        results (list): A list of results
        challenges (list): A list of challenges
        students (list): A list of students
    """
    def __init__(self):
        self.__results = []
        self.student_manager = StudentManager()
        self.challenge_manager = ChallengeManager()

    def __str__(self):
        """Return a string representation of the competition object."""
        return f'{self.__class__.__name__}()' # Use f-strings to create a string representation of the competition object for storage in txt file

    @property
    def results(self):
        """Return a list of results with the latest result at beginning of the list [index 0]]"""
        return self.__results
    
    @staticmethod
    def resuls_table_process(value) -> str:
        """Process the value in the result table to remove the leading and trailing whitespace 
        and replace the empty string with "Results" and replace the value of -1 with an empty string"""
        value = value.strip() # Remove the leading and trailing whitespace
        if value == "":
            return "Results"
        if value in '-1':
            return ''
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
    
    def report_results(self, return_table = False, print_terminal = True) -> str:
        """
        Display the latest results in a table and the fatest student with their average time.

        Table:
        +--------------+--------------+
        |   Results    | Challenge ID |
        +--------------+--------------+
        | Student ID 1 |     Time     |
        | Student ID 2 |     Time     |
        +--------------+--------------+

        Input:
        - return_table (bool): Return the table as a format string of the report if True.
        """
        table = self.results[0] # Get the latest result
        no_student = len(table) - 1
        no_challenge = len(table[0]) - 1
        fastest_student, fastest_time = self.show_fastest_student()
        table = Table.create_format_table("COMPETITION DASHBOARD", table, col_widths=None, width_space=8, header_width_space=5, header_align='^', row_align='^')
        footer = f'There are {no_student} students and {no_challenge} challenges.\n' \
                f'The top student is {fastest_student} with an average time of {fastest_time} minutes.'
        table += '\n' + footer
        if print_terminal:
            print(table)
        if return_table:
            return table
        
    def read_students(self, file):
        """
        Read the students from the given file and save it to the students attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the students attribute.
        
        """
        self.student_manager.read_student_file(file)
    
    def find_student(self, student_id: str):
        """
        Find the student with the given ID.

        Input:
        - student_id (str): The ID of the student to find.

        Returns:
        - Student: The student object with the given ID.
        """
        return self.student_manager.get_student(student_id)
    
    def average_time(self, student_id: str) -> float:
        """
        Calculate the average time for the student with the given ID.
        
        Input:
        - student_id (str): The ID of the student to find.
        
        Returns:
        - float: The average time for the student with the given ID.
        """
        current_result = self.results[0]
        for i in range(1, len(current_result)):
            if current_result[i][0] == student_id:
                times = [float(x) for x in current_result[i][1:] if x not in ['--', '', None]]
                valid_times = len(times)
                return round(float(sum(times) / valid_times), 2) if valid_times else None

    def show_fastest_student(self) -> tuple:
        """
        Display the fastest student in the latest result record with their average time.

        Returns:
        - tuple: A tuple containing the fastest student object and their average time.
        """
        # Since the latest result is always the top of the list, we can access index 0 to get the latest result
        student_average_times = {}
        for student_result in self.results[0][1:]:
            student_id = student_result[0]
            student_average_times[student_id] = self.average_time(student_id)
        fastest_student = min(student_average_times, key=student_average_times.get)
        return fastest_student , student_average_times[fastest_student]
    def read_challenge(self, file):
        """
        Read the challenges from the given file and save it to the challenges attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the challenges attribute.
        
        """
        self.challenge_manager.read_challenge_file(file)
    
    def find_challenge(self, challenge_id):
        """
        Find the challenge with the given ID.

        Input:
        - challenge_id (str): The ID of the challenge to find.

        Returns:
        - Challenge: The challenge object with the given ID.
        """
        return self.challenge_manager.get_challenge(challenge_id)
                
    def read_all_files(self, result_file, challenge_file, studen_file):
        """
        Read all the data from the given files and save it to the appropriate attributes.

        Input:
        - studen_file (str): The path to the file to read. If None exit the program and print the error message.
        - result_file (str): The path to the file to read. If None exit the progra and print the error message.
        - challenge_file (str): The path to the file to read. If None exit the program and print the error message.
        
        """
        # Read the data from the given files
        if result_file is None:
            sys.exit('No results are available for the competition')
        self.read_results(result_file)

        # Read the data from the given files
        if challenge_file is not None:
            self.read_challenges(challenge_file)
        
        # Read the data from the given files
        if studen_file is not None:
            self.read_students(studen_file)       

    def read_challenges(self, file):
        """
        Read the challenges from the given file and save it to the challenges attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the challenges attribute.
        
        """
        self.challenge_manager.read_challenge_file(file)
    def report_challenges(self, return_table = False, print_terminal = True) -> str:
        """
        Print the report table of the competition to the console.

        Table:

        +----------------+-----------+----------+----------+----------+-------------+
        |    Challenge   |   Name    |  Weight  | Nfinish  | Nongoing | AverageTime |
        +----------------+-----------+----------+----------+----------+-------------+
        | Challenge ID 1 |   Name 1  |    #.#   |    #     |     #    |    #.##     | 
        | Challenge ID 2 |   Name 2  |    #.#   |    #     |     #    |    #.##     | 
        +----------------+-----------+----------+----------+----------+-------------+


        Input:
        - return_table (bool): Return the table as a format string of the report if True.
        """
        table =  [['Challenge', 'Name', 'Type', 'Weight', 'Nfinish', 'Nongoing', 'AverageTime']]
        table_width = [10, 25, 10, 10, 10, 10, 15]
        result_table = self.results[0] # Get the latest result
        most_difficult_challenge = None
        most_difficult_average_time = None
        average_time = None
        inversed_result_table = [list(row) for row in zip(*result_table)] # Invert the result table so that we can get the number of finished and ongoing challenges
        for challenge in self.challenge_manager.challenges:
            for row in inversed_result_table[1:]:
                if row[0] == challenge.id:
                    valid_result = [float(x) for x in row[1:] if x not in ['--', '', None]]
                    nfinish = len(valid_result) # Get the number of finished challenges
                    nongoing = len([x for x in row if x == '--']) # Get the number of ongoing challenges
                    if nfinish > 0:
                        average_time = round((sum(valid_result) / nfinish),2) # Calculate the average time and round to 2 decimal places
                    else:
                        average_time = None
                    table.append([challenge.id, str(challenge), challenge.type, f'{challenge.weight:.1f}', nfinish, nongoing, average_time])
                    if not most_difficult_average_time or average_time > most_difficult_average_time:
                        most_difficult_challenge = challenge.id
                        most_difficult_average_time = average_time
        table = Table.create_format_table("CHALLENGE INFORMATION", table, table_width, width_space=8, header_width_space=5, header_align='^', row_align='^')
        footer = f'The most difficult challenge is {most_difficult_challenge} with an average time of {average_time} minutes'
        table += '\n' + footer
        if print_terminal:
            print(table)
        if return_table:
            return table
    def report_student(self, return_table = False, print_terminal = True) -> str:
        """
        Print the report table of the student result to the console.

        Table:

        +----------------+-----------+----------+----------+----------+-------------+
        |    Student     |   Name    |  Type    | Nfinish  | Nongoing | AverageTime |
        +----------------+-----------+----------+----------+----------+-------------+
        | Student ID 1   |   Name 1  |    U     |    #     |     #    |    #.##     |
        | Student ID 2   |   Name 2  |    P     |    #     |     #    |    #.##     |
        +----------------+-----------+----------+----------+----------+-------------+


        Input:
        - return_table (bool): Return the table as a format string of the report if True
        - print_terminal (bool): Print the table to the console if True
        """
        table =  [['Student', 'Name', 'Type', 'Nfinish', 'Nongoing', 'AverageTime']]
        table_width = [10, 25, 10, 10, 10, 15]
        result_table = self.results[0]
        for student in self.student_manager.students:
            for row in result_table[1:]:
                if row[0] == student.id:
                    valid_result = [float(x) for x in row[1:] if x not in ['--', '', None]]
                    nfinish = len(valid_result)
                    nongoing = len([x for x in row if x == '--'])
                    if nfinish > 0:
                        average_time = round((sum(valid_result) / nfinish),2)
                    else:
                        average_time = None
                    table.append([student.id, str(student), student.type, nfinish, nongoing, average_time])
        table = Table.create_format_table("STUDENT INFORMATION", table, table_width, width_space=8, header_width_space=5, header_align='^', row_align='^')
        if print_terminal:
            print(table)
        if return_table:
            return table

    def report_all(self, output_file = 'competition_report.txt'):
        """
        Print the report of the competition to the given file.

        Input:
        - output_file (str): The path to the file to write. Default is 'competition_report.txt'
        
        Output:
        - A report of the competition to the given file 
            or only print to the console if the output_file is None.
        """
        print_terminal = True # Define print_terminal variable
        return_table = True # Define return_table variable
        if output_file is not None: # Define output_file variable
            footer_message = f'Report {output_file} generated!'
            content = self.report_results(return_table, print_terminal)+'\n' \
                + self.report_challenges(return_table, print_terminal)+'\n' \
                + self.report_student(return_table, print_terminal)+'\n' \
                + f'{footer_message}'
            TextEditor.add_to_file(output_file, content)
        else:
            return_table = False
            footer_message = 'No output file is provided, the report will be printed to the console only'
            self.report_results(return_table, print_terminal)
            self.report_challenges(return_table, print_terminal)
            self.report_student(return_table, print_terminal)
            print(footer_message)
        

if __name__ == "__main__":
    # Test code at pass level
    competition = Competition()
    competition.read_challenges('test\challenges.txt')
    competition.read_results('test\\results.txt')
    competition.read_students('test\students.txt')
    competition.report_all()  # Provide a value for the output_file argument
    