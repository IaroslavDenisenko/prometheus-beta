import pytest
from src.palindrome_validator import is_palindrome

def test_simple_palindrome():
    """Test basic palindrome strings"""
    assert is_palindrome("racecar") == True
    assert is_palindrome("madam") == True

def test_punctuated_palindrome():
    """Test palindromes with punctuation and spaces"""
    assert is_palindrome("A man, a plan, a canal: Panama") == True
    assert is_palindrome("race a car") == False

def test_case_insensitive():
    """Test that palindrome check is case-insensitive"""
    assert is_palindrome("Racecar") == True
    assert is_palindrome("Madam") == True

def test_empty_and_single_char():
    """Test empty string and single character"""
    assert is_palindrome("") == True
    assert is_palindrome("a") == True

def test_non_palindrome():
    """Test non-palindrome strings"""
    assert is_palindrome("hello") == False
    assert is_palindrome("python") == False

def test_invalid_input():
    """Test handling of invalid input types"""
    with pytest.raises(TypeError):
        is_palindrome(123)
    with pytest.raises(TypeError):
        is_palindrome(None)
    with pytest.raises(TypeError):
        is_palindrome(["not", "a", "string"])