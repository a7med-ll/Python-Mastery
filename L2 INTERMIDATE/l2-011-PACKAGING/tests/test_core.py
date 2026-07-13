from textkit import word_count, is_palindrome


def test_word_count():
    assert word_count("hello world") == 2
    assert word_count("") == 0


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("hello") is False