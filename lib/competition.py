"""
Competition class to store the competition data and process the data 

"""
import sys
from .student import StudentManager
from .challenge import ChallengeManager
from .result import Result
from .misc import Table, TextEditor

class Competition():
    """ Competition class to store the competition data and process the data
    
    Attributes:
        results (list): A list of results
        challenges (list): A list of challenges
        students (list): A list of students
    """
    def __init__(self):
        self.result = Result()
        self.student_manager = StudentManager()
        self.challenge_manager = ChallengeManager()

    def __str__(self):
        """Return a string representation of the competition object."""
        return f'{self.__class__.__name__}()' # Use f-strings to create a string representation of the competition object for storage in txt file
    

    def read_results(self, result_file: str) -> None:
        """
        Read the results from the given file and save it to the results attribute.

        Input:
        - result_file (str): The path to the file to read.
            If None, use the value of the result_file attribute.
        """
        self.result.read_results_file(result_file)
    
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
        table = self.result # Get the result table
        no_student = table.return_no_students()
        no_challenge = table.return_no_challenges()
        fastest_student, fastest_time = table.fastest_student()
        table = Table.create_format_table("COMPETITION DASHBOARD", table.result_array, col_widths=None, width_space=8, header_width_space=5, header_align='^', row_align='^')
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
                
    def read_all_files_on_command(self):
        """
        Read all the data from the given files and save it to the appropriate attributes base on the command line arguments.

        The command line arguments are:
        - sys.argv[1]: The path to the file to read the results from.
        - sys.argv[2]: The path to the file to read the challenges from.
        - sys.argv[3]: The path to the file to read the students from.
        
        """
        if len(sys.argv) == 1:
            sys.exit('No results are available for the competition')
        elif len(sys.argv) == 2:
            self.read_results(sys.argv[1])
        elif len(sys.argv) == 3:
            self.read_results(sys.argv[1])
            self.read_challenges(sys.argv[2])
        elif len(sys.argv) == 4:
            self.read_results(sys.argv[1])
            self.read_challenges(sys.argv[2])
            self.read_students(sys.argv[3])
        else:
            sys.exit('Invalid number of files')

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
        result_table = self.result # Get the latest result
        most_difficult_challenge, most_difficult_average_time= result_table.return_hardest_challenge() # Get the most difficult challenge
        inversed_result_table = result_table.transpose() # Invert the result table so that we can get the number of finished and ongoing challenges
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
        result_table = self.result
        for student in self.student_manager.students:
            for row in result_table.result_array[1:]:
                if row[0] == student.id:
                    valid_result = [float(x) for x in row[1:] if x not in ['--', '', None]]
                    nfinish = len(valid_result)
                    nongoing = len([x for x in row if x == '--'])
                    if not student.meets_requirements():
                        student_name = '!'+student.name
                    if nfinish > 0:
                        average_time = round((sum(valid_result) / nfinish),2)
                    else:
                        average_time = None
                    table.append([student.id, student_name, student.type, nfinish, nongoing, average_time])
        table = Table.create_format_table("STUDENT INFORMATION", table, table_width, width_space=8, header_width_space=5, header_align='^', row_align='^')
        student_detail = self.student_manager.get_student(result_table.fastest_student()[0])
        footer = f'The student with the fatest average time is {student_detail} with an average time of {result_table.fastest_student()[1]:.2f} minutes.'
        table += '\n' + footer
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
        content = '' # Define content variable
        footer_message = f'Report {output_file} generated!'
        if len(sys.argv) == 2 : # Define output_file variable
            content += self.report_results(return_table, print_terminal)+'\n'
        elif len(sys.argv) == 3 :
            content += self.report_results(return_table, print_terminal)+'\n'
            content += self.report_challenges(return_table, print_terminal)+'\n'
        elif len(sys.argv) == 4:
            content += self.report_results(return_table, print_terminal)+'\n'
            content += self.report_challenges(return_table, print_terminal)+'\n'
            content += self.report_student(return_table, print_terminal)+'\n'
            
        content += f'{footer_message}\n'
        TextEditor.add_to_file(output_file, content)

        

if __name__ == "__main__":
    # Test code at pass level
    competition = Competition()
    competition.read_challenges('test\\challenges.txt')
    competition.read_results('test\\results.txt')
    competition.read_students('test\\students.txt')
    competition.report_all()  # Provide a value for the output_file argument
    