from fastapi import APIRouter, HTTPException
from schemas.login_request_model import LoginRequestModel
from schemas.sign_up_request_model import SignupRequestModel
from schemas.forget_password_request_model import ForgetPasswordRequest
from schemas.user_model import UserModel
from dotenv import load_dotenv
from firebase_admin import firestore, credentials
import httpx
import os
import firebase_admin

load_dotenv()

# email router
email_auth_router = APIRouter()

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

# firebase web api key
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")


@email_auth_router.post("/login")
async def login_user(data: LoginRequestModel):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": data.email,
        "password": data.password,
        "returnSecureToken": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        result = response.json()
        return {
            "idToken": result["idToken"],
            "refreshToken": result["refreshToken"],
            "email": result["email"],
            "localId": result["localId"]
        }


# Sign Up with Email/Password
@email_auth_router.post("/email_password_sign_up")
async def email_password_sign_up_auth(data: SignupRequestModel):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": data.email,
        "password": data.password,
        "returnSecureToken": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            error_detail = response.json().get("error", {}).get("message", "Unknown error")
            raise HTTPException(status_code=400, detail=f"Sign up failed: {error_detail}")

        result = response.json()
        uid = result["localId"]
        email = result["email"]

        # Create the UserModel instance
        user_data = UserModel(username=data.username, email=email, uid=uid)

        # Store user data in Firestore
        user_ref = db.collection("traffic_police_users").document(uid)
        user_ref.set(user_data.dict())  # Using .dict() to convert Pydantic model to dict

        return {
            "message": "User created successfully",
            "email": email,
            "localId": uid,
            "idToken": result["idToken"]
        }


# Endpoint to send password reset link
@email_auth_router.post("/forget_password")
async def forget_password_send_link(data: ForgetPasswordRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": data.email
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

        if response.status_code != 200:
            error_detail = response.json().get("error", {}).get("message", "Failed to send reset link")
            raise HTTPException(status_code=400, detail=error_detail)

        return {"message": "Password reset link sent successfully to your email."}
