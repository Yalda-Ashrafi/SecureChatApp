

# 🔐 SecureChatApp — Classical Cryptography Educational Messenger

SecureChatApp is a small **Flask educational application** demonstrating:  
-  User authentication  
-  Encrypted-message workflows  
-  Three classical cryptographic algorithms (Vigenère, Vernam, OTP)  

⚠️ This project is **not** a replacement for modern end-to-end encrypted messengers. It is designed for **learning and demonstration purposes**.

---

##  Features
- User registration and login with hashed passwords  
- Message encryption/decryption workflows  
- Clear error handling for invalid/malformed keys  
- Sender/receiver classroom workflow simulation  
- Algorithms implemented with strict validation rules  
- Database-backed message storage (`SQLite`)

  ![Model Results](https://github.com/Yalda-Ashrafi/SecureChatApp/blob/f77533be3e8c73cabe283194340751867b10bea4/Screenshot%202026-09-17%20044621.png)
  ![Model Results](https://github.com/Yalda-Ashrafi/SecureChatApp/blob/f77533be3e8c73cabe283194340751867b10bea4/Screenshot%202026-09-17%20023114.png
)
  ![Model Results](https://github.com/Yalda-Ashrafi/SecureChatApp/blob/f77533be3e8c73cabe283194340751867b10bea4/Screenshot%202026-09-17%20011550.png
)


 ![Model Results](https://github.com/Yalda-Ashrafi/SecureChatApp/blob/f77533be3e8c73cabe283194340751867b10bea4/Screenshot%202026-09-17%20010427.png)
  

---

##  Run Locally

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app\main.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), register an account, and log in.  

- The database is created at `instance\chat.db` when the application first uses it.  
- To create tables explicitly:  
  ```powershell
  python -m app.database.db_setup
  ```

> `python app\main.py` is supported deliberately; the entry point adds the repository root to `sys.path` when run as a script.

---

## 🔑 Algorithms

- **Vigenère**  
  - Transforms ASCII letters, preserves case/punctuation.  
  - Advances the key only for letters.  
  - Key must contain ASCII letters.  

- **Vernam**  
  - XORs UTF‑8 message bytes with a key of exactly the same byte length.  
  - Ciphertext displayed as Base64 in the web UI.  

- **One-Time Pad (OTP)**  
  - Strict byte-oriented XOR with a fresh cryptographically random key.  
  - Keys must never be reused.  

> Invalid key lengths and malformed keys produce clear validation errors rather than silently truncating a message.

---



##  Sender & Receiver Workflow

The authenticated chat page supports both sides of the classroom workflow:

1. Sender enters plaintext, chooses an algorithm, enters a key, and saves the resulting ciphertext.  
2. Receiver selects the same algorithm, pastes the ciphertext, enters the shared key, and decrypts the message.  
3. Vernam and OTP ciphertexts are represented as Base64 because XOR output is arbitrary bytes.  

🔒 Keys are **never stored**. Sender and receiver must share keys through a separate secure channel.

---
Visit the Live Web App: https://securechatapp-oopk.onrender.com/otp

##  Security Notes

- Passwords use **Werkzeug’s adaptive password hashing**.  
- Sessions use **HTTP-only, SameSite=Lax cookies**.  
- Secret key can be supplied with `SECURECHAT_SECRET_KEY`.  
- Set `SESSION_COOKIE_SECURE=True` behind HTTPS.  
- Messages are stored as ciphertext, but **key management and transport are left to the learner**.  

 This is an **educational demonstration**, not a production messenger:  
- Classical Vigenère is vulnerable to cryptanalysis.  
- OTP security depends on one-time secret keys.  
- HTTPS and deployment infrastructure must be configured manually.  
- Production CSRF protection and rate limiting should be added before public deployment.  

---

##  Tests

SecureChatApp includes automated unit tests to validate the correctness of the cryptographic algorithms and workflows.

Test Coverage:

Vigenère encryption/decryption

Vernam encryption/decryption

OTP encryption/decryption

Input validation and error handling

Database setup and message storage

Execution:  
Run all tests with:
pytest
Results:  
14 tests passed in approximately 1.45 seconds.
This confirms that all implemented algorithms and workflows behave consistently under different conditions and that error handling is robust.

---

##  References

This project is informed by academic research, including:  
- Anzari et al. (2026): Security and performance analysis of Caesar & Vigenère  
- Damanik et al. (2025): Modified Vigenère in web applications  
- Davlatov et al. (2025): Neural networks in Vigenère cryptanalysis  
- Deng et al. (2026): OTP transmission schemes  
- Kutsman (2025): Vernam cipher applications  
- Wati & Hasan (2025):  Neural cryptography for OTP generation  

