import pytest
import hashlib
from brute import Brute
from unittest.mock import Mock

def test_empty_string():
    brute = Brute("")
    assert brute.target == hashlib.sha512(b"").hexdigest()

def test_too_big_string():
    secret = "a" * 9
    brute = Brute(secret)
    assert brute.target == hashlib.sha512(bytes(secret, "utf-8")).hexdigest()

def test_brute_once_correct():
    secret = "123456"
    brute = Brute(secret)
    assert brute.bruteOnce(secret) == True

def test_brute_once_incorrect():
    secret = "abcdef"
    brute = Brute(secret)
    assert brute.bruteOnce("wrongpass") == False

def test_brute_once_edge_cases():
    brute = Brute("a")
    assert brute.bruteOnce("a") == True
    assert brute.bruteOnce("b") == False

    brute = Brute("abcdefgh")
    assert brute.bruteOnce("abcdefgh") == True
    assert brute.bruteOnce("abcdefg") == False

def test_brute_many_success():
    secret = "a"
    brute = Brute(secret)
    result = brute.bruteMany(1000)
    assert result >= 0

def test_brute_many_failure(monkeypatch):
    secret = "notfound"
    brute = Brute(secret)
    assert brute.bruteMany(1000) == -1

def test_brute_many_success_with_mock():
    secret = "test123"
    brute = Brute(secret)
    
    brute.randomGuess = Mock(return_value=secret)
    
    result = brute.bruteMany(100)
    assert result >= 0
    assert isinstance(result, float)
    brute.randomGuess.assert_called()

def test_brute_many_failure_with_mock():
    secret = "correct"
    brute = Brute(secret)
    
    brute.randomGuess = Mock(return_value="wrong")
    
    result = brute.bruteMany(10)
    assert result == -1
    assert brute.randomGuess.call_count == 10

def test_random_guess_length():
    brute = Brute("dummy")
    for _ in range(100):
        guess = brute.randomGuess()
        assert 1 <= len(guess) <= 8

