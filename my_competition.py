""" 
This is the submission file for the final coding challenge for Programming Fundamentals.

Name: Quang Ba Hai Dang
Student ID: s3676330

Highest level attempted: DI

Date: 18/1/2024

Short description:
Outline any problem or requirement that we have not implemented in the code her.
"""

# Import required librarys

from lib.misc import Control
from lib.competition import Competition

def main():
    """ This is the main function of the program"""
    competition = Competition() # Create the competition object
    competition.read_all_files_on_command() # Read the requirement files from the command line arguments
    competition.report_all('competition_report.txt') # Display the report to the user and save it to the file

if __name__ == "__main__":
    main()
