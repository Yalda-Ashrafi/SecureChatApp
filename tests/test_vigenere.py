from app.crypto import vigenere

def test_vigenere():
    text = "HELLO"
    key = "KEY"
    cipher = vigenere.encrypt(text, key)
    assert vigenere.decrypt(cipher, key) == text


def test_vigenere_preserves_case_and_punctuation():
    text = "Hello, World!"
    cipher = vigenere.encrypt(text, "KEY")
    assert cipher == "Rijvs, Uyvjn!"
    assert vigenere.decrypt(cipher, "KEY") == text


def test_vigenere_rejects_invalid_key():
    import pytest
    with pytest.raises(ValueError):
        vigenere.encrypt("hello", "key 1")
