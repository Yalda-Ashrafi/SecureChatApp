from app.crypto import key_manager

def test_key_manager():
    key = key_manager.generate_key(5)
    assert key_manager.validate_key(key, 5)
