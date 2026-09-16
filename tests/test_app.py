import pytest
import base64

from app import create_app, db
from app.crypto import otp, vernam


@pytest.fixture()
def client():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        db.create_all()
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.drop_all()


def test_registration_login_and_authenticated_chat(client):
    response = client.post(
        "/register",
        data={
            "username": "alice",
            "password": "correct horse battery",
            "confirm_password": "correct horse battery",
        },
    )
    assert response.status_code == 302
    assert client.post("/login", data={"username": "alice", "password": "wrong"}).status_code == 200
    assert client.post("/login", data={"username": "alice", "password": "correct horse battery"}).status_code == 302

    response = client.post(
        "/chat",
        data={"plaintext": "Hello!", "key": "KEY", "algorithm": "vigenere"},
    )
    assert response.status_code == 200
    assert b"Rijvs!" in response.data


def test_chat_requires_login_and_otp_demo_is_public(client):
    assert client.get("/chat").status_code == 302
    response = client.post("/otp-demo", data={"plaintext": "hello"})
    assert response.status_code == 200
    assert b"Ciphertext" in response.data


def login(client):
    client.post(
        "/register",
        data={
            "username": "receiver",
            "password": "correct horse battery",
            "confirm_password": "correct horse battery",
        },
    )
    client.post("/login", data={"username": "receiver", "password": "correct horse battery"})


def test_chat_receiver_can_decrypt_vigenere(client):
    login(client)
    response = client.post(
        "/chat",
        data={
            "action": "decrypt",
            "decrypt_algorithm": "vigenere",
            "decrypt_ciphertext": "Rijvs!",
            "decrypt_key": "KEY",
        },
    )
    assert response.status_code == 200
    assert b"Hello!" in response.data


@pytest.mark.parametrize("algorithm", ["vernam", "otp"])
def test_chat_receiver_can_decrypt_base64_byte_ciphers(client, algorithm):
    login(client)
    plaintext = "Hello!"
    key = b"XMCKL!" if algorithm == "vernam" else otp.generate_key(len(plaintext))
    cipher = (vernam if algorithm == "vernam" else otp).encrypt(plaintext, key)
    response = client.post(
        "/chat",
        data={
            "action": "decrypt",
            "decrypt_algorithm": algorithm,
            "decrypt_ciphertext": base64.b64encode(cipher).decode(),
            "decrypt_key": base64.b64encode(key).decode() if algorithm == "otp" else key.decode(),
        },
    )
    assert response.status_code == 200
    assert b"Hello!" in response.data


def test_chat_receiver_rejects_invalid_ciphertext(client):
    login(client)
    response = client.post(
        "/chat",
        data={
            "action": "decrypt",
            "decrypt_algorithm": "otp",
            "decrypt_ciphertext": "not-base64",
            "decrypt_key": "short-key",
        },
    )
    assert response.status_code == 200
    assert b"Ciphertext must be valid Base64" in response.data
