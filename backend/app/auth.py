from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Field Office Types
class FieldOffice(str, Enum):
    SFO = "sfo"  # Senior Field Office
    LFO = "lfo"  # Local Field Office
    JFO = "jfo"  # Junior Field Office

# User Role
class UserRole(str, Enum):
    ADMIN = "admin"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    VIEWER = "viewer"

# User Model
class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    full_name: str
    field_office: FieldOffice
    role: UserRole = UserRole.RESEARCHER
    is_active: bool = True
    created_at: Optional[datetime] = None

# Login Request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Token Response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

# Mock user database (in production, use a real database)
USERS_DB = {
    "sfo@example.com": {
        "id": 1,
        "email": "sfo@example.com",
        "full_name": "Senior Field Officer",
        "field_office": FieldOffice.SFO,
        "role": UserRole.ADMIN,
        "password": "sfo123"  # In production, use hashed passwords
    },
    "lfo@example.com": {
        "id": 2,
        "email": "lfo@example.com",
        "full_name": "Local Field Officer",
        "field_office": FieldOffice.LFO,
        "role": UserRole.RESEARCHER,
        "password": "lfo123"
    },
    "jfo@example.com": {
        "id": 3,
        "email": "jfo@example.com",
        "full_name": "Junior Field Officer",
        "field_office": FieldOffice.JFO,
        "role": UserRole.ANALYST,
        "password": "jfo123"
    }
}

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user and return user object"""
    user_data = USERS_DB.get(email)
    if not user_data or user_data["password"] != password:
        return None
    
    # Return user without password
    user_dict = {k: v for k, v in user_data.items() if k != "password"}
    return User(**user_dict)

def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email"""
    user_data = USERS_DB.get(email)
    if not user_data:
        return None
    
    user_dict = {k: v for k, v in user_data.items() if k != "password"}
    return User(**user_dict)
