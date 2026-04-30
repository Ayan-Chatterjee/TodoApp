import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 2 != 3

def test_is_instance():
    assert isinstance("Hello", str)
    assert isinstance(123, int)

def test_boolean():
    assert True
    assert not False

def test_type():
    assert type('Hello' is str)
    assert type('World' is not int)

def test_greater_and_less_than():
    assert 7>3
    assert 5<10

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 3 in num_list
    assert 6 not in num_list
    assert not any(any_list)
    assert all(num_list)

class Student:
    def __init__(self, firstname: str, lastname: str, age: int):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age

@pytest.fixture
def default_student():
    return Student("John", "Doe", 20)

def test_student(default_student):
    assert default_student.firstname == "John", "Firstname should be John"
    assert default_student.lastname == "Doe", "Lastname should be Doe"
    assert default_student.age == 20, "Age should be 20"