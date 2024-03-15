import pytest

def test_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance('test', str)
    assert not isinstance('10', int)

def test_bool():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello') is str
    assert type('World') is not int

def test_greater_and_less_than():
 assert 7 > 3
 assert 4 < 10

def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert any(num_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def student_default():
    return Student('John', 'Doe', 'Computer Science', 3)

def test_person_initialzation(student_default):
    assert student_default.first_name == 'John', 'First name should be John'
    assert student_default.last_name == 'Doe', 'Last name should be Doe'
    assert student_default.major == 'Computer Science'
    assert student_default.years == 3
