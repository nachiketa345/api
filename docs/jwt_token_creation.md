# JWT Token Creation in Python

## Steps to Create a JWT Token

1. **Install Required Libraries**
   - Ensure you have the necessary libraries installed:
     ```bash
     pip install python-jose passlib
     ```

2. **Import Required Modules**
   - Import the necessary modules in your Python file:
     ```python
     from datetime import datetime, timedelta
     from jose import jwt
     from passlib.context import CryptContext
     ```

3. **Set Up Configuration Constants**
   - Define your secret key, algorithm, and token expiration time:
     ```python
     SECRET_KEY = "your-secret-key-change-in-production"
     ALGORITHM = "HS256"
     ACCESS_TOKEN_EXPIRE_MINUTES = 30
     ```

4. **Create Password Hashing Context**
   - Set up the password hashing context using Passlib:
     ```python
     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
     ```

5. **Define the Token Creation Function**
   - Create a function to generate the JWT token:
     ```python
     def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
         to_encode = data.copy()
         if expires_delta:
             expire = datetime.utcnow() + expires_delta
         else:
             expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
         to_encode.update({"exp": expire})
         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
         return encoded_jwt
     ```

6. **Using the Token Creation Function**
   - Call the function to create a token:
     ```python
     token_data = {"sub": "user@example.com"}
     token = create_access_token(token_data)
     ```

7. **Token Structure**
   - The generated token will have three parts: Header, Payload, and Signature.

8. **Decoding the Token**
   - To decode and verify the token:
     ```python
     decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
     ```

9. **Error Handling**
   - Handle exceptions for token validation:
     ```python
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
     except JWTError:
         # Handle token errors
     ```

## Conclusion
This document outlines the steps to create and manage JWT tokens in Python, ensuring secure authentication for your application.







## OAuth2 vs JWT

### OAuth2
- **OAuth2** is an **authorization framework** (a protocol/standard).
- It defines *how* tokens are issued, used, and validated for accessing resources.
- OAuth2 itself does **not specify the format** of the token (it could be a random string, a JWT, etc.).
- In FastAPI, `OAuth2PasswordBearer` is a tool that helps you implement OAuth2’s "password flow" (user provides username/password, gets a token).

### JWT (JSON Web Token)
- **JWT** is a **token format**—a way to encode data (like user info and expiration) into a signed string.
- JWTs are often used as the *access tokens* in OAuth2 implementations, but they can be used elsewhere too.
- JWTs are self-contained: they carry all the info needed for authentication/authorization.

### How They Work Together in Your Code

- **OAuth2PasswordBearer**:  
  Handles the process of getting a token from the user (usually via `/login` endpoint).
- **JWT**:  
  The actual token you issue and validate. It contains user info and is signed so it can’t be tampered with.

**In summary:**  
- **OAuth2** is the protocol (the rules for how authentication/authorization works).
- **JWT** is the format of the token you use within that protocol.

**You are using OAuth2 to manage authentication flow, and JWT as the token format.**  
This is a very common and secure approach in modern APIs!

## Conclusion
This document outlines the steps to create and manage JWT tokens in Python, ensuring secure authentication for your application, and explains how OAuth2 and JWT work together for robust API security.