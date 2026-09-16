from app.crypto import vernam

def test_vernam():
    text = "HELLO"
    key = "XMCKL"
    cipher = vernam.encrypt(text, key)
    assert vernam.decrypt(cipher, key) == text


def test_vernam_requires_exact_utf8_key_length():
    import pytest
    with pytest.raises(ValueError):
        vernam.encrypt("hello", b"tiny")
