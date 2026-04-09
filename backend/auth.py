import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

try:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    FIREBASE_KEY_PATH = os.path.join(BASE_DIR, "firebase_key.json")

    if not os.path.exists(FIREBASE_KEY_PATH):
        raise FileNotFoundError("firebase_key.json not found")

    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)

    print("Firebase initialized successfully")

except Exception as e:
    print(f"Firebase initialization failed: {e}")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")