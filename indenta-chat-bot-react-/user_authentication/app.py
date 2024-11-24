# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime, timedelta
# import sqlite3

# # Create FastAPI instance
# app = FastAPI()

# # CORS setup
# origins = [
#     "http://localhost:3000",
#     # Add other origins if needed
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=['*'],  # Include OPTIONS
#     allow_headers=['*'],
# )

# # SQLite connection setup
# conn = sqlite3.connect('taxpert.db')
# conn.row_factory = sqlite3.Row  # To access row data by column name
# c = conn.cursor()

# # Security
# SECRET_KEY = "a85e51fed8ba58eaeedaaffd819023ba0191f4b9b0490ae62032aa8a735045a9"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # User model
# class User(BaseModel):
#     username: str
#     email: str
#     hashed_password: str

# # Function to verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # Function to get user from database
# def get_user(username: str):
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     user_row = c.fetchone()
#     if user_row:
#         return User(username=user_row['username'], email=user_row['email'], hashed_password=user_row['hashed_password'])

# # Function to authenticate user
# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# # Function to create access token
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Signup endpoint
# # Signup endpoint
# @app.post("/signup/")
# async def signup(user: User):
#     try:
#         # Hash the password before inserting into the database
#         hashed_password = pwd_context.hash(user.hashed_password)
#         # Remove password from user as it's not needed in the request body
#         user_dict = user.dict()
#         del user_dict['password']  # Corrected this line
#         # Insert user into the database with hashed password
#         with conn:
#             conn.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)", (user.username, user.email, hashed_password))
#         return {"message": "User created successfully"}
#     except sqlite3.IntegrityError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this username or email already exists",
#         )



# # Login endpoint
# @app.post("/login/")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# # Error handling
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return {"message": exc.detail}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app)




from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import sqlite3

# Create FastAPI instance
app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],  # Include OPTIONS
    allow_headers=['*'],
)

# SQLite connection setup
conn = sqlite3.connect('taxpert.db')
conn.row_factory = sqlite3.Row  # To access row data by column name
c = conn.cursor()

# Security
SECRET_KEY = "a85e51fed8ba58eaeedaaffd819023ba0191f4b9b0490ae62032aa8a735045a9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Model for signup request body
class SignupUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user from database
def get_user(username: str):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user_row = c.fetchone()
    if user_row:
        return User(username=user_row['username'], email=user_row['email'], hashed_password=user_row['hashed_password'])

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Signup endpoint
@app.post("/signup/")
async def signup(user: SignupUser):
    try:
        # Hash the password before inserting into the database
        hashed_password = pwd_context.hash(user.password)
        # Insert user into the database with hashed password
        with conn:
            conn.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)", (user.username, user.email, hashed_password))
        return {"message": "User created successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists",
        )

@app.post("/login/")
async def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
# Login endpoint
# @app.post("/login/")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"message": exc.detail}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
