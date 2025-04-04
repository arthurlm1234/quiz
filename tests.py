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

def test_remove_choice_by_id():
    question = Question(title="Test Remove")
    choice = question.add_choice("Choice 1", False)
    assert choice in question.choices
    question.remove_choice_by_id(choice.id)
    assert choice not in question.choices

def test_remove_all_choices():
    question = Question(title="Test Remove All")
    question.add_choice("Choice 1", False)
    question.add_choice("Choice 2", True)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_choices_with_correct_answers():
    question = Question(title="Test Select", max_selections=2)
    c1 = question.add_choice("Choice 1", False)
    c2 = question.add_choice("Choice 2", True)
    c3 = question.add_choice("Choice 3", True)
    selected = question.select_choices([c2.id, c3.id])
    assert set(selected) == {c2.id, c3.id}

def test_select_choices_excludes_incorrect():
    question = Question(title="Test Exclude Incorrect", max_selections=2)
    c1 = question.add_choice("Choice 1", False)
    c2 = question.add_choice("Choice 2", True)
    selected = question.select_choices([c1.id, c2.id])
    assert selected == [c2.id]

def test_select_choices_exceeding_max_selections():
    question = Question(title="Test Exceed", max_selections=1)
    c1 = question.add_choice("Choice 1", True)
    c2 = question.add_choice("Choice 2", True)
    with pytest.raises(Exception) as excinfo:
        question.select_choices([c1.id, c2.id])
    assert "Cannot select more than" in str(excinfo.value)

def test_set_correct_choices():
    question = Question(title="Test Set Correct")
    c1 = question.add_choice("Choice 1", False)
    c2 = question.add_choice("Choice 2", False)
    question.set_correct_choices([c2.id])
    assert not c1.is_correct
    assert c2.is_correct

def test_choice_ids_increment():
    question = Question(title="Test ID Increment")
    c1 = question.add_choice("Choice 1", False)
    c2 = question.add_choice("Choice 2", False)
    assert c2.id == c1.id + 1

def test_invalid_choice_removal():
    question = Question(title="Test Invalid Removal")
    question.add_choice("Choice 1", False)
    with pytest.raises(Exception) as excinfo:
        question.remove_choice_by_id(999)
    assert "Invalid choice id" in str(excinfo.value)

def test_choice_text_length_validation():
    question = Question(title="Test Choice Text")
    with pytest.raises(Exception) as excinfo:
        question.add_choice("") 
    assert "Text cannot be empty" in str(excinfo.value)

def test_add_choice_after_removal_all():
    question = Question(title="Test Add After Removal")
    question.add_choice("Choice 1", False)
    question.add_choice("Choice 2", False)
    question.remove_all_choices()
    new_choice = question.add_choice("New Choice", True)
    assert new_choice.id == 1