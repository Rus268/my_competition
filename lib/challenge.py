"""
Challenge class
"""

class Challenge():
    """
    Challenge class

    Attributes:
        id (str): The ID of the challenge. Must start with 'C'.
        type (str): The type of the challenge ('M' for Mandatory, 'S' for Special).
        name (str): The name of the challenge.
        weight (float): The weight of the challenge.
    
    """
    def __init__(self, id:str, name:str):
        self.__id = id
        self.__name = name
    
    def __str__(self):
        """ Returns a string representation of the challenge."""
        return f'Default Challenge Object, Name: {self.name}, ID: {self.id}' # Use f-strings to create a string representation of the challenge for storage in txt file
    
    @property
    def id(self):
        """ Returns the ID of the challenge."""
        return self.__id
    
    @id.setter
    def id(self, new_id):
        self.__id = str(new_id)
    
    @property
    def type(self):
        """ Returns the type of the challenge."""
        return self.__type
    
    @type.setter
    def type(self, new_type:str):
        if not new_type in ["M","S"]:
            raise ValueError("Invalid type")
        self.__type = new_type
    
    @property
    def name(self):
        """ Returns the name of the challenge."""
        return self.__name
    
    @name.setter
    def name(self, new_name:str):
        self.__name = str(new_name)

    @property
    def weight(self):
        """ Returns the weight of the challenge."""
        return self.__weight
    
    @weight.setter
    def weight(self, new_weight):
        self.__weight = float(new_weight)

class MandatoryChallenge(Challenge):
    """ 
    Mandatory challenge class
     
      Attributes:
        id (str): The ID of the challenge. Must start with 'C'.
        type (str): The type of the challenge. Default for mandatory challenges is 'M'.
        name (str): The name of the challenge.
        weight (float): The weight of the challenge. Default for mandatory challenges is 1.0.
    """
    weight = 1.0 # Mandatory challenges always have a weight of 1.0

    def __init__(self, id, name):
        super().__init__(id, name)
        self.__type = 'M'

    @property
    def type(self):
        """ Returns the type of the challenge."""
        return self.__type
    
    def __str__(self):
        return f'{self.name}(M)'
    
    def __repr__(self):
        return f'{self.id}, {self.type}, {self.name}, {self.weight}'
    
    @classmethod
    def set_weight(cls, new_weight):
        """ Sets the weight of the challenge."""
        cls.weight = float(new_weight)

class SpecialChallenge(Challenge):
    """
    Special challenge class
    
    Attributes:
    
        id (str): The ID of the challenge. Must start with 'C'.
        type (str): The type of the challenge. Default for special challenges is 'S'.
        name (str): The name of the challenge.
        weight (float): The weight of the challenge. Must be larger than 1.0.
    """
    def __init__(self, id, name, weight):
        super().__init__(id, name)  # Remove the 'type' argument from the super().__init__() method call
        self.__type = 'S'
        self.set_weight(weight)  # Use the set_weight() method to set the weight of the challenge
    
    def __str__(self):
        """ Returns a string representation of the challenge."""
        return f'{self.name}(M)'

    def __repr__(self):
        return f'{self.id}, {self.type}, {self.name}, {self.weight}'

    @property
    def type(self):
        """ Returns the type of the challenge."""
        return self.__type

    @property
    def weight(self):
        """ Returns the weight of the challenge."""
        return self.__weight

    def set_weight(self, new_weight):
        """ Returns the weight of the challenge."""
        if float(new_weight) < 1.0:
            raise ValueError("Invalid weight. Special challenges must have a weight of at least 1.0.")
        self.__weight = float(new_weight)

class ChallengeFactory():
    """
    Challenge factory class. Responsible for creating challenge objects.
    """
    @staticmethod
    def create_challenge(id:str, challenge_type:str, name:str, weight = 1.0) -> Challenge or SpecialChallenge:
        """
        Create a challenge object based on the given parameters.

        Args:
            id (int): The ID of the challenge.
            type (str): The type of the challenge. Must be either "M" for regular challenge or "S" for special challenge.
            name (str): The name of the challenge.
            weight (float): The weight of the challenge.

        Returns:
            Challenge or SpecialChallenge: The created challenge object.

        Raises:
            ValueError: If an invalid challenge type is provided.
        """
        # Validate id
        if not isinstance(id, str):
            raise ValueError("id must be an integer")

        # Validate challenge_type
        if challenge_type not in ["M", "S"]:
            raise ValueError("challenge_type must be 'M' or 'S'")

        # Validate name
        if not isinstance(name, str):
            raise ValueError("name must be a string")

        # Validate weight
        weight = float(weight)
        if not isinstance(weight, (int, float)) or weight < 1.0:
            raise ValueError("weight must be a number greater than or equal to 1.0")

        # Create the challenge object
        if challenge_type == "M":
            return MandatoryChallenge(id, name)
        elif challenge_type == "S":
            return SpecialChallenge(id, name, weight)
        else:
            raise ValueError("Invalid type")

class ChallengeManager():
    """ This class is responsible for managing challenges."""
    def __init__(self):
        self.__challenges = []

    @property
    def challenges(self)-> list:
        """ Returns the list of challenges."""
        return self.__challenges
    
    def list_challenge_id(self) -> list:
        """
        Returns the challenges associated with this object.

        Returns:
            list: A list of challenges id
        """
        return [challenge.id for challenge in self.__challenges]
    
    def add_challenge(self, challenge_id, challenge_type, name, weight = 1.0) -> None:
        """ Adds a challenge to the list of challenges."""
        new_challenge = ChallengeFactory.create_challenge(challenge_id, challenge_type, name, weight)
        self.__challenges.append(new_challenge)
    
    def remove_challenge(self, challenge):
        """ Removes a challenge from the list of challenges."""
        self.__challenges.remove(challenge)
    
    def get_challenge(self, challenge_id):
        """ Returns a challenge with the given ID."""
        for ch in self.__challenges:
            if ch.id == challenge_id:
                return ch
        return None
    
    def read_challenge_file(self, file_name):
        """
        Read the challenges from the given file and save it to the challenges attribute.

        Input:
        - file (str): The path to the file to read. If None, use the value of the challenges attribute.
        
        """
        if file_name is None:
            raise ValueError(f"Missing challenge file {file_name}")
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                elements = [item.strip() for item in line.strip().split(",")]
                if len(elements) == 4:
                    challenge_obj = ChallengeFactory.create_challenge(elements[0], elements[1], elements[2], elements[3])
                    self.__challenges.append(challenge_obj)
                else:
                    raise ValueError("Invalid challenge record")


if __name__ == "__main__":
    challenge = Challenge('C1', 'Test')
    mandatory_challenge = ChallengeFactory.create_challenge('C2', 'M', 'Mandatory')  # Pass the weight argument with a default value of 1.0
    special_challenge = ChallengeFactory.create_challenge('C3', 'S', 'Test', 2.0)
    print(challenge)
    print(mandatory_challenge)
    print(special_challenge)

