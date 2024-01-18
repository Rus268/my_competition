"""
This is the misc.py file that contains the misc functions
"""

# Import required librarys
import sys
import datetime

class Table():
    """Table class"""
    @staticmethod
    def create_format_table(title:str, table_2d_list:list, col_widths = None, width_space= 8, header_width_space = 5, header_align = '^', row_align = '<') -> str:
        """
        Print a table with the given title and table_2d_list.

        Input:
        - title (str): The title of the table.
        - table_2d_list (list): A 2D list of the table content. Ex: [['Header 1', 'Header 2'], ['Value 1', 'Value 2']]
        - col_wishs (list): A list of the column widths. If None, the column width will be calculated automatically.
        - width_space (int): The number of spaces between each column. Default is 8.
        - header_width_space (int): The number of spaces between the first column and the second column. Default is 5.
        - header_align (str): The alignment of the header. Default is '^' (center), '<' (left) and '>' (right) are also available.
        - row_align (str): The alignment of the row. Default is '<' (left), '^' (center) and '>' (right) are also available.

        Output:

        Title
        +--------------+--------------+
        |   Header 1   |   Header 2   |
        +--------------+--------------+
        |   Value 1    |   Value 2    |
        +--------------+--------------+

        """
        # Replace None values with an empty string
        table_2d_list = [[col if col is not None else '' for col in row] for row in table_2d_list]

        # Calculate the columns width if not given
        if col_widths is None: # Use zip to transpose the table_2d_list [1] “Built-in functions,” Python documentation, https://docs.python.org/3/library/functions.html#zip (accessed Jan. 17, 2024). 
            widths = [(max(map(len, str(col))) + width_space) for col in zip(*table_2d_list)]
        else:
            widths = col_widths
        widths[0] += header_width_space

        # Create the row template
        row_template = '|'+'|'.join(f"{{:{row_align}{width}}}" for width in widths) +'|'
        # Create the separator
        separator = '+'+'+'.join('-'* w for w in widths)+'+'

        # Create the table in string format
        table =  '\n' + title + '\n' + separator + '\n'

        # Add the header to the table
        header_template = '|'+'|'.join(f"{{:{header_align}{width}}}" for width in widths) +'|'
        table += header_template.format(*table_2d_list[0], *widths) + '\n' + separator + '\n'

        # Print table content
        for row in table_2d_list[1:]:
            table += row_template.format(*row, *widths) + '\n'
        table += separator

        return table
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

class Control:
    """Control class for interacting with the user"""
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

class TextEditor():
    """TextEditor class"""
    @staticmethod
    def add_to_file(file, new_content):
        """This function add new content to the beginning of the file
        
        Input:
        - file (str): The path to the file to add the content to.
        - new_content (str): The content to add to the file.
        """
        current_date ='\n' + 'REPORT UPDATE ON: ' + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n' # Get the current date
        try:
            with open(file, "r+", encoding="utf-8") as file:
                content = file.read() # Read the content of the file
                file.seek(0, 0)
                file.write(current_date + new_content + '\n' + content)
        except FileNotFoundError:
            # As we are not allow to use the os module, we will cath the FileNotFoundError exception to create the file
            with open(file, "w", encoding="utf-8") as file:
                file.write(current_date + new_content + '\n')
        except IOError as e:
            # If there is an error while writing to the file, we will print the error and exit the program to prevent further error
            print(f'An error occurred while writing to the file: {e}')
            print('Please check the file before try again')
            sys.exit(0)