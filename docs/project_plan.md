# FastAPI Banking Application: Project Plan & Documentation

This document serves as a comprehensive plan and technical reference for the development of the banking application.

## 1. Core Architecture

The project is built on a modern, high-performance stack:
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy for database interaction.
- **Data Validation:** Pydantic for robust data validation at the API boundary.
- **Frontend:** React (to be developed).

## 2. Database Schema (`models.py`)

The database consists of three main tables: `User`, `Account`, and `Transaction`, linked by relationships. This structure is solid and provides a good foundation.

## 3. Pydantic Schemas (`schemas.py`)

Pydantic schemas are used to define the shape of data for API requests (inputs) and responses (outputs). This ensures that only valid data enters the system.

### Key Concepts in Schemas

#### Custom Validated Types (`Annotated`)

To ensure data integrity for fields like MPINs, mobile numbers, and Aadhar numbers, we use `Annotated` from Python's `typing` library combined with Pydantic's `Field`.

**Example:**
```python
from typing import Annotated
from pydantic import Field

MobileNumber = Annotated[str, Field(min_length=10, max_length=10, pattern=r'^[0-9]{10}$')]
```
- **Why use this?** It creates a reusable, self-documenting type (`MobileNumber`) that automatically validates the data format. This is more robust and readable than just using `str`.

#### Pydantic V1 vs. V2: `orm_mode` vs. `from_attributes`

You asked about the difference between `orm_mode` and `from_attributes`. They do the same thing, but one is old and one is new.

- **`class Config: orm_mode = True`**: This is the **old syntax from Pydantic V1**.
- **`model_config = ConfigDict(from_attributes=True)`**: This is the **new, recommended syntax for Pydantic V2**.

**Function:** Both settings allow a Pydantic model to be created directly from a SQLAlchemy object (or any object with attributes). This is crucial for converting your database models into response schemas. We use the modern V2 syntax as it's the current best practice.

## 4. Development Roadmap

### Phase 1: Core Backend (In Progress)

1.  **Finalize Schemas (`schemas.py`)**: **(✓ Complete)** We have created robust schemas for users and accounts, including input validation and safe output models.
2.  **Implement Authentication (`auth.py`)**: **(Next Step)**
    - **Password Hashing:** Use `passlib` to hash passwords on registration and verify them on login. **Never store plain-text passwords.**
    - **JWT for Sessions:** Use JWT (JSON Web Tokens) to manage user sessions. A user gets a token on login, which they must provide for all protected actions.
3.  **Build API Endpoints (`main.py` or Routers)**:
    Here is a detailed breakdown of the API endpoints. It's a good practice to group these into different `APIRouter` files (e.g., `routers/users.py`, `routers/accounts.py`).

    **Note**: `(Authenticated)` means the endpoint requires a valid JWT token.

    ---
    #### **User Endpoints (`/users`)**
    - **`POST /users/register`**: Create a new user.
      - **Request Body**: `UserCreateSchema`.
      - **Response**: `UserDisplaySchema`.
    - **`POST /users/login`**: Authenticate a user and receive a JWT.
      - **Request Body**: `UserLoginSchema`.
      - **Response**: `{ "access_token": "...", "token_type": "bearer" }`.
    - **`GET /users/me`**: `(Authenticated)` Get the profile of the currently logged-in user.
      - **Response**: `UserDisplaySchema`.
    - **`PATCH /users/me`**: `(Authenticated)` Update the current user's information (e.g., name, password).
      - **Request Body**: A schema with optional fields for updating.
      - **Response**: `UserDisplaySchema`.

    ---
    #### **Account Endpoints (`/accounts`)**
    - **`POST /accounts`**: `(Authenticated)` Create a new bank account for the logged-in user.
      - **Request Body**: `AccountCreateSchema`.
      - **Response**: `AccountDisplaySchema`.
    - **`GET /accounts/my-accounts`**: `(Authenticated)` Get a list of all bank accounts owned by the current user.
      - **Response**: `List[AccountDisplaySchema]`.
    - **`GET /accounts/{account_id}`**: `(Authenticated)` Get details for a specific bank account.
      - **Response**: `AccountDisplaySchema`.
    - **`DELETE /accounts/{account_id}`**: `(Authenticated)` Close a specific bank account.
      - **Response**: `{ "message": "Account closed successfully" }`.

    ---
    #### **Transaction Endpoints (`/transactions`)**
    - **`POST /transactions/deposit/{account_id}`**: `(Authenticated)` Deposit funds into an account.
      - **Request Body**: `{ "amount": float, "description": str }`.
      - **Response**: `{ "message": "Deposit successful", "new_balance": float }`.
    - **`POST /transactions/withdraw/{account_id}`**: `(Authenticated)` Withdraw funds from an account.
      - **Request Body**: `{ "amount": float, "description": str }`.
      - **Response**: `{ "message": "Withdrawal successful", "new_balance": float }`.
    - **`GET /transactions/{account_id}`**: `(Authenticated)` Get the transaction history for a specific account.
      - **Response**: `List[TransactionDisplaySchema]`.
    - **`POST /transactions/transfer`**: `(Authenticated)` Transfer funds from one of the user's accounts to another account.
      - **Request Body**: `{ "from_account_id": int, "to_account_number": str, "amount": float, "description": str }`.
      - **Response**: `{ "message": "Transfer successful" }`.

### Phase 2: Transaction Logic
1.  **Implement Business Logic**: Write the functions that handle the core logic for deposits, withdrawals, and transfers. Ensure all database operations are atomic (they either all succeed or all fail together) to prevent data corruption.
2.  **Transaction History**: Implement the logic to fetch and return a list of all transactions for a given account.
3.  **Database Integrity**: Ensure that balance updates and transaction creation happen in a single, atomic database transaction to prevent errors.

### Phase 3: Frontend Development

1.  **Connect to Backend**: Use a library like `axios` in your React application to make requests to your FastAPI backend.
2.  **Build UI Components**: Create React components for registration, login, account dashboard, and transaction forms.
3.  **State Management**: Use a state management library (like Redux or Zustand) to handle user authentication state and data fetching.

This plan provides a clear path forward. Your project is off to an excellent start.
