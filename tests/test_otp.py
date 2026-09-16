from app.crypto import otp

def test_otp():
    text = "HELLO"
    key = otp.generate_key(len(text))
    cipher = otp.encrypt(text, key)
    assert otp.decrypt(cipher, key) == text


def test_otp_counts_utf8_bytes_and_rejects_short_keys():
    import pytest
    text = "café"
    key = otp.generate_key(len(text.encode("utf-8")))
    assert otp.decrypt(otp.encrypt(text, key), key) == text
    with pytest.raises(ValueError):
        otp.encrypt(text, key[:-1])
