"""
This result file contain all relevant structure to handle the result class
"""

from .challenge import Challenge

class Result():
    """ This is the result class"""
    def __init__(self, result_array = None):
        self.result_array = result_array if result_array else []

    def transpose(self):
        """ Transpose the result table"""
        return list(map(list, zip(*self.result_array)))  # Base on a code idea from stack overflow [1]
    
    def return_challenge_result(self, challenge_id:str) -> list:
        """ Return the result of a challenge"""
        transpose_result = self.transpose() # Transpose the result table so that the challenge id is in the first column
        for row in transpose_result[1:]:
            if row[0] == challenge_id:
                return row
            return None
    
    def challenge_average_times(self, challenge_id: str) -> float:
        """
        Calculate the average time for the challenge with the given ID.
        
        Input:
        - challenge_id (str): The ID of the challenge to find.
        
        Returns:
        - float: The average time for the challenge with the given ID.
        """
        for i in range(1, len(self.result_array)):
            if self.result_array[i][0] == challenge_id:
                row = self.return_challenge_result(challenge_id)
                print(row)
                times = [float(x) for x in row[1:] if x not in ['--', '', None]]
                valid_times = len(times)
                return round(float(sum(times) / valid_times), 2)

    def return_hardest_challenge(self)-> tuple:
        """ Return a tuple of the hardest challenge and its average time"""
        challenge_average_times = {}
        for challenge_id in self.result_array[0][1:]:
            average_time = self.challenge_average_times(challenge_id)
            if average_time is not None:
                challenge_average_times[challenge_id] = average_time
        if challenge_average_times:
            hardest_challenge = max(challenge_average_times, key=challenge_average_times.get)
            return hardest_challenge, challenge_average_times[hardest_challenge]
        else:
            return None, None

    def return_no_challenges(self):
        """ Return the number of challenges"""
        return len(self.result_array[0]) - 1
    
    @staticmethod
    def result_table_process(value) -> str:
        """Process the value in the result table to remove the leading and trailing whitespace 
        and replace the empty string with "Results" and replace the value of -1 with an empty string"""
        value = value.strip() # Remove the leading and trailing whitespace
        if value == "":
            return "Results"
        if value.lower() in ["444", 'tba']: # If the value is 444 or tba or TBA then return "--"
            return "--"
        if value == '-1' or value.isalpha(): # If the value is -1 or a string except TBA or tba then return an empty string
            return ''
        return value

    def read_results_file(self, file_name):
        """ Read the result file"""
        result_array = []  # Define result_array variable
        # open the file with explicit encoding
        with open(file_name, "r", encoding="utf-8") as file:
            # read the rest of the file
            for line in file:
                if ',' not in line:
                    raise ValueError("Result record must be separated by comma")
                row = []
                cells = line.strip().split(",")
                if len(cells) != 6: # Check if the number of elements in the result record is equal to the number of challenges + 1 header
                    raise ValueError("Unexpected number of elements in result record or record is not separated by comma")
                for cell in cells:
                    cell = Result.result_table_process(cell)  # Define self variable
                    row.append(cell)
                result_array.append(row)
        if not result_array:
            raise ValueError("No result in the competition")
        self.result_array = result_array

    def return_student_result(self, student_id) -> list:
        """ Return the result of a student"""
        for row in self.result_array:
            if row[0] == student_id:
                return row
        return None
    
    def return_no_students(self):
        """ Return the number of students"""
        return len(self.result_array) - 1 # Exclude the header row

    def student_average_time(self, student_id: str) -> float:
        """
        Calculate the average time for the student with the given ID.
        
        Input:
        - student_id (str): The ID of the student to find.
        
        Returns:
        - float: The average time for the student with the given ID.
        """
        for i in range(1, len(self.result_array)):
            if self.result_array[i][0] == student_id:
                times = [float(x) for x in self.result_array[i][1:] if x not in ['--', '', None]]
                valid_times = len(times)
                return round(float(sum(times) / valid_times), 2) if valid_times else None
    
    def return_student_participation(self, student_id: str) -> dict:
        """
        This function return a dictionary of the challenge that indicate whether the student participated in the challenge or not.

        Input:
        - student_id (str): The ID of the student to find.

        Returns:
        - dict: A dictionary of the challenge that indicate whether the student participated in the challenge or not.
        The value of the dictionary is -1 if the student did not participate, 0 if the student participated but did not finish, 1 if the student participated and finished.
        """
        student_result = self.return_student_result(student_id)
        if student_result is None:
            return None
        student_participation = {}
        for i in range(1, len(student_result)):
            if student_result[i] in ['', None]: 
                student_participation[self.result_array[0][i]] = -1 # If the student did not participate
            elif student_result[i] in ['TBA', 'tba', '444', '--']: 
                student_participation[self.result_array[0][i]] = 0 # If the student participated but did not finish
            else:
                student_participation[self.result_array[0][i]] = 1 # If the student participated and finished
        return student_participation

    def fastest_student(self) -> tuple:
        """
        Display the fastest student in the latest result record with their average time.

        Returns:
        - tuple: A tuple containing the fastest student id and their average time.
        """
        # Since the latest result is always the top of the list, we can access index 0 to get the latest result
        student_average_times = {}
        for student in self.result_array[1:]:
            student_average_times[student[0]] = self.student_average_time(student[0])
        fastest_student = min(student_average_times, key=student_average_times.get)
        return (fastest_student, student_average_times[fastest_student])
    
    def highest_score_student(self, challenge_weights:dict = None) -> tuple:
        """
        Display the highest score student in the latest result record with their score.

        Returns:
        - tuple: A tuple containing the highest score student object and their score.
        """
        # Since the latest result is always the top of the list, we can access index 0 to get the latest result
        student_scores = {}
        for student in self.result_array[1:]:
            student_scores[student[0]] = self.return_student_score(student[0], challenge_weights)
        highest_score_student = max(student_scores, key=student_scores.get)
        return (highest_score_student, student_scores[highest_score_student])


    
    def return_challenge_rank(self, challenge_id: str) -> list:
        """ 
        Return a list of student id that participate in the challenge with the given id with their rank
        
        Input:
        - challenge_id (str): The ID of of the challenge to find.

        Returns:
        - list: A list of student id that participate in the challenge with the given id sort by their rank
        """
        challenge_index = self.result_array[0].index(challenge_id)
        student_results = {student[0]: float(student[challenge_index]) for student in self.result_array[1:] if student[challenge_index] not in ['', None, 'TBA', 'tba', '444', '--']}
        sorted_student_results = sorted(student_results.items(), key=lambda x: x[1])
        return [student_id for student_id, _ in sorted_student_results]  # Return a list of student id that participate in the challenge with the given id with their rank
            
    def return_student_score(self, student_id, challenge_weights: dict = None) -> int:
        """
        This function return the score of a student. Score is compute base on if student come first, second or last in each 

        Input:
        - student_id (str): The ID of the student to find.
        - challenge_weights (dict): A dictionary of the challenge id and their weight {challenge_id: weight}

        Returns:
        - int: The score of the student.
        """
        # Define the score of each place
        first_place_score = 3
        second_place_score = 2
        third_place_score = 1
        every_other_place_score = 0
        last_place_score = -1
        # Define the score of the student
        student_score = 0
        for challenge_id in self.result_array[0][1:]:
            challenge_rank_list = self.return_challenge_rank(challenge_id)
            if student_id in challenge_rank_list:
                student_rank = challenge_rank_list.index(student_id) + 1 # Get the index of the student in the challenge rank list and add 1 to it to get the rank of the student
                if challenge_weights is not None:
                    challenge_weight = challenge_weights[challenge_id]
                else:
                    challenge_weight = 1 # If the challenge weight is not provided then set it to 1
                if student_rank == 1:
                    student_score += first_place_score * challenge_weight
                elif student_rank == 2:
                    student_score += second_place_score * challenge_weight
                elif student_rank == 3:
                    student_score += third_place_score * challenge_weight
                elif student_rank == len(challenge_rank_list):
                    student_score += last_place_score * challenge_weight
                elif student_rank > 3:
                    student_score += every_other_place_score * challenge_weight
        return student_score

        
if __name__ == "__main__":
    result = Result()
    result.read_results_file("test\\results.txt")
    print(result.return_challenge_rank("C04"))
    print(result.return_student_score("S125"))