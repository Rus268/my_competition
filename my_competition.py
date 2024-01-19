""" 
This is the submission file for the final coding challenge for Programming Fundamentals.

Name: Quang Ba Hai Dang
Student ID: s3676330

Highest level attempted: HD

Date: 19/1/2024

Short description:
The most challenging part of this assignment was to figure out the logic of the class and ensure that the logic is encapsulated and the class is easy to use.
A lot of time I end up with a class that is too complicated and hard to use. I have to refactor the code a lot of times to make it easier to use as well as break the code into smaller functions.
One of the most challenging part of the program as well was to figure out how to format the table in the report without using any external library. 
This is because the table is not a fixed size and the size of the table depends on the data. I have to use a lot of string manipulation to format the table as well as creating multiple variable to increase the function flexibility.

If there is more time I would like to refactor the code to make the function more distinct and encapsulated. There also a lot of code that can be reused into a separate function but I end up leaving as it is because of the time constraint. 

References:
[1] saba javadsaba javad - 1322 bronze badges, “Using map and zip return an empty array,” Stack Overflow, https://stackoverflow.com/questions/58682900/using-map-and-zip-return-an-empty-array (accessed Jan. 10, 2024). 
[2] K. Chris, “Lambda sorted in python – how to lambda sort a list,” freeCodeCamp.org, https://www.freecodecamp.org/news/lambda-sort-list-in-python/ (accessed Jan. 19, 2024). 
"""

# Import required librarys

from lib.misc import Control
from lib.competition import Competition

def main():
    """ This is the main function of the program"""
    competition = Competition() # Create the competition object
    competition.read_all_files_on_command() # Read the requirement files from the command line arguments
    competition.report_all() # Display the report to the user and save it to the file name competition_report.txt

if __name__ == "__main__":
    main()
