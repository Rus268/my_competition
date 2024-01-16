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
    def __init__(self, id, type, name, weight):
        self.__id = id
        self.__type = type
        self.__name = name
        self.__weight = weight
    
    def __str__(self):
        return f'{self.id}, {self.type}, {self.name}, {self.weight}'  # Placeholder implementation
    
    @property
    def id(self):
        """ Returns the ID of the challenge."""
        return self.__id
    
    @id.setter
    def id(self, new_id):
        self.__id = str(new_id)
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, new_type:str):
        if not new_type in ["M","S"]:
            raise ValueError("Invalid type")
        self.__type = new_type
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name:str):
        self.__name = str(new_name)

    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, new_weight):
        self.__weight = float(new_weight)
  
if __name__ == "__main__":
    # test code
    challenge = Challenge("C1","M","Challenge 1", 0.5)
    print(challenge)
