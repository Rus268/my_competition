"""
This result file contain all relevant structure to handle the result class
"""

# Import required librarys

class Result():
    """ This is the result class"""
    def __init__(self, result_array = None):
        self.result_array = result_array if result_array else []

    def transpose(self):
        """ Transpose the result table"""
        return list(map(list, zip(*self.result_array)))
    
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
        if value in '-1':
            return ''
        if value in ["444", 'TBA', 'tba']:
            return "--"
        return value

    def read_results_file(self, file_name):
        """ Read the result file"""
        result_array = []  # Define result_array variable
        # open the file with explicit encoding
        with open(file_name, "r", encoding="utf-8") as file:
            # read the rest of the file
            for line in file:
                row = []
                cells = line.strip().split(",")
                for cell in cells:
                    cell = Result.result_table_process(cell)  # Define self variable
                    row.append(cell)
                result_array.append(row)
        self.result_array = result_array

    def return_student_result(self, student_id):
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

    def fastest_student(self) -> tuple:
        """
        Display the fastest student in the latest result record with their average time.

        Returns:
        - tuple: A tuple containing the fastest student object and their average time.
        """
        # Since the latest result is always the top of the list, we can access index 0 to get the latest result
        student_average_times = {}
        for student in self.result_array[1:]:
            student_average_times[student[0]] = self.student_average_time(student[0])
        fastest_student = min(student_average_times, key=student_average_times.get)
        return (fastest_student, student_average_times[fastest_student])
        
if __name__ == "__main__":
    result = Result()
    result.read_results_file("test\\results.txt")
    print(result.result_array)
    print(result.student_average_time("S001"))
    print(result.fastest_student())