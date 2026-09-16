# SecureChatApp

SecureChatApp is a small Flask educational application demonstrating user
authentication, encrypted-message workflows, and three classical algorithms.
It is not a replacement for a modern end-to-end encrypted messenger.

## Run locally

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app\main.py
```

Open <http://127.0.0.1:5000>, register an account, and log in. The database is
created at `instance\chat.db` when the application first uses it. To create
tables explicitly, run `python -m app.database.db_setup`.

`python app\main.py` is supported deliberately; the entry point adds the
repository root to `sys.path` when run as a script.

## Algorithms

* **Vigenère** transforms ASCII letters, preserves case and punctuation, and
  advances the key only for letters. Its key must contain ASCII letters.
* **Vernam** XORs UTF-8 message bytes with a key of exactly the same byte
  length. The result is displayed as Base64 in the web UI.
* **OTP** is the same strict byte-oriented XOR operation with a fresh
  cryptographically random key. Never reuse a one-time-pad key.

Invalid key lengths and malformed keys produce a clear validation error rather
than silently truncating a message.

## Sender and receiver workflow

The authenticated chat page supports both sides of the classroom workflow:

1. The sender enters plaintext, chooses an algorithm, enters a key, and saves
   the resulting ciphertext.
2. The receiver selects the same algorithm, pastes the ciphertext, enters the
   shared key, and decrypts the message.
3. Vernam and OTP ciphertexts are represented as Base64 because XOR output is
   arbitrary bytes.

The application never stores encryption keys. A sender and receiver must share
the key through a separate secure channel.

## Security notes

Passwords use Werkzeug's adaptive password hashing. Sessions use HTTP-only,
`SameSite=Lax` cookies, and the secret key can be supplied with
`SECURECHAT_SECRET_KEY`. Set `SESSION_COOKIE_SECURE=True` behind HTTPS.
Messages in this demo are stored as ciphertext, but key management and
transport are intentionally left to the learner. This is an educational
demonstration, not a production messenger: classical Vigenere is vulnerable to
cryptanalysis, OTP security depends on one-time secret keys, HTTPS and
deployment infrastructure must be configured by the operator, and production
CSRF protection/rate limiting should be added before public deployment.

The project deliberately does not claim modern end-to-end encryption. Replacing
the classical algorithms with an authenticated modern protocol would be a
different project and would not satisfy the classical-cryptography learning
objective.

## Tests

```powershell
pytest -q
```
