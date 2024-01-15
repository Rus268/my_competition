import unittest
from lib.student import Student

class TestStudent(unittest.TestCase):
    def test_new_student_undergraduate(self):
        # Arrange
        student_type = 'U'
        student_id = 1
        student_name = 'John Doe'
        
        # Act
        student = Student.new_student(student_type, student_id, student_name)
        
        # Assert
        self.assertEqual(student.id, student_id)
        self.assertEqual(student.name, student_name)
        self.assertEqual(student.__class__.__name__, 'Undergraduate')
    
    def test_new_student_postgraduate(self):
        # Arrange
        student_type = 'P'
        student_id = 2
        student_name = 'Jane Smith'
        
        # Act
        student = Student.new_student(student_type, student_id, student_name)
        
        # Assert
        self.assertEqual(student.id, student_id)
        self.assertEqual(student.name, student_name)
        self.assertEqual(student.__class__.__name__, 'Postgraduate')

if __name__ == '__main__':
    unittest.main()