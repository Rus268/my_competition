class Challenge():
    def __init__(self, id, type, weight):
        self.__id = id
        self.__type = type
        self.__weight = weight
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, new_id):
        self.__id = new_id
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, new_type: 'M' or 'S'):
        if not new_type in ["M","S"]:
            raise ValueError("Invalid type")
        self.__type = new_type
    
    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, new_weight):
        self.__weight = float(new_weight)
    def __str__(self):
        return "Team object"  # Placeholder implementation
  
if __name__ == "__main__":
    Challenge()