import sys

class Competition():
    def __init__(self):
        self.__results = []
        self.__challenges = []
        self.__students = []
    def __str__(self):
        return "Competition object"

    @staticmethod
    def resuls_table_process(value):
        if value == "":
            return "Results"
        if value in '-1' or isinstance(value, str):
            return " "
        if value in ["444",'TBA', 'tba']:
            return "--"
        else:
            return float(value)

    def read_results(self, result_file: str = None) -> None:
        """
        Read the results from the given file and save it to the results attribute.

        Input:
        - result_file (str): The path to the file to read. If None, use the value of the result_file attribute.
        
        """
        if result_file is None:
            sys.exit('No results are available for the competition')
        list_2d = []
        # open the file with explicit encoding
        with open(result_file, "r", encoding="utf-8") as file:
            # read the rest of the file
            for line in file:
                row = line.strip().split(",")
                for cell in row:
                    cell = self.resuls_table_process(cell)
                # split the line into a list and append it to the list_2d
                list_2d.append(row)
        self.__results.insert(list_2d)
    
    def display_results(self):
        """
        Display the results in the results attribute.
        """
        table = self.result_file
        widths = [max(map(len, col)) for col in zip(*table)]
        row_template = '|'.join(f"{{:{width}}}" for width in widths)
        no_student = len(table) - 1
        no_challenge = len(table[0]) - 1
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
        print(f'The top student is {} with an average time of {} minutes')
    
    def read_students(self, file):
        """
        Read the students from the given file and save it to the students attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the students attribute.
        
        """
        pass

        
    def read_challenges(self, file):
        """
        Read the challenges from the given file and save it to the challenges attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the challenges attribute.
        
        """
        pass
    def display_challenges(self):
        """
        Display the challenges in the challenges attribute.
        """
        pass


    @staticmethod
    def read_command_line():
        """This function allow the object to be used in the command line interface"""
        if len(sys.argv) == 1:
            return None
        elif len(sys.argv) == 2:
            return sys.argv[1]
        elif len(sys.argv) == 3:
            return sys.argv[1], sys.argv[2]
        elif len(sys.argv) == 4:
            return sys.argv[1], sys.argv[2], sys.argv[3]
        else:
            print('[Usage:] python my_competition.py <result file>')
            sys.exit(0)
        

if __name__ == "__main__":
    Competition()