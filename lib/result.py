"""
This result file contain all relevant structure to handle the result class
"""

# Import required librarys
import sys

class Result():
    """ This is the result class"""
    def __init__(self, n_finish, n_going, average_time):
        self.__n_finish = n_finish
        self.__n_going = n_going
        self.__average_time = average_time

    @property
    def n_finish(self):
        """ Returns the number of students who finished the competition."""
        return self.__n_finish
    
    @n_finish.setter
    def n_finish(self, new_n_finish):
        self.__n_finish = new_n_finish
    
    @property
    def n_going(self):
        """ Returns the number of students who are still going."""
        return self.__n_going
    
    @n_going.setter
    def n_going(self, new_n_going):
        self.__n_going = new_n_going

    @property
    def average_time(self):
        """ Returns the average time of the students who finished the competition."""
        return self.__average_time
    
    @average_time.setter
    def average_time(self, new_average_time):
        self.__average_time = new_average_time

if __name__ == "__main__":
    print("This is the result.py file that contains the result class")
    print("This file is not meant to be executed")
    sys.exit()