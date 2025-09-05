import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception) as exception:
        question.add_choice('a'*200, False)
    assert str(exception.value) == "Text cannot be longer than 100 characters"
    with pytest.raises(Exception) as exception:
        question.add_choice('', False)
    assert str(exception.value) == "Text cannot be empty"

def test_create_question_with_invalid_points():
    with pytest.raises(Exception) as exception:
        question = Question(title='q1', points=-1)
    assert str(exception.value) == 'Points must be between 1 and 100'
    with pytest.raises(Exception) as exception:
        question = Question(title='q1', points=101)
    assert str(exception.value) == 'Points must be between 1 and 100'

def test_remove_invalid_choice():
    question = Question(title='q1')
    with pytest.raises(Exception) as exception:
        question.remove_choice_by_id(1)
    assert str(exception.value) == 'Invalid choice id 1'
    
def test_search_removed_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.remove_choice_by_id(1)
    with pytest.raises(Exception) as exception:
        choice = question._find_choice_by_id(1)
    assert str(exception.value) == 'Invalid choice id 1'
    
def test_changing_choice_status():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.set_correct_choices([1])

    choice = question.choices[0]
    assert choice.is_correct

def test_list_empty_choice_list():
    question = Question(title='q1')
    assert question._list_choice_ids() == []

def test_selecting_over_max_selections():
    question = Question(title='q1')
    question.add_choice('a', True)
    question.add_choice('b', True)
    with pytest.raises(Exception) as exception:
        question.correct_selected_choices([1,2])
    assert str(exception.value) == f'Cannot select more than {question.max_selections} choices'   

def test_clearing_empty_choice_list():
    question = Question(title='q1')
    question.remove_all_choices()
    assert question.choices == []

def test_adding_same_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('a', False)

    choice = question.choices[0]
    choice2 = question.choices[1]
    assert len(question.choices) == 2
    assert choice.text == choice2.text
    assert choice.is_correct == choice2.is_correct

def test_checking_invalid_choice_id():
    question = Question(title='q1')
    with pytest.raises(Exception) as exception:
        question._check_valid_choice_id(1)
    assert str(exception.value) == f'Invalid choice id 1'  